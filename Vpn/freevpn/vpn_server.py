#!/usr/bin/env python3
"""
Simple Python VPN Server
Creates an encrypted tunnel between server and client
For educational and authorized penetration testing purposes
"""

import socket
import ssl
import hashlib
import secrets
import struct
import threading
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import base64

class VPNServer:
    def __init__(self, host='0.0.0.0', port=8443, cert_file=None, key_file=None):
        self.host = host
        self.port = port
        self.cert_file = cert_file
        self.key_file = key_file
        self.clients = {}
        self.running = True
        
        # Generate server key pair
        self.server_private_key = secrets.token_bytes(32)
        self.server_public_key = self.derive_public_key(self.server_private_key)
        
    def derive_public_key(self, private_key):
        """Derive public key using SHA256 (simplified)"""
        return hashlib.sha256(private_key).digest()
    
    def encrypt_data(self, data, key):
        """Encrypt data using AES-256-GCM"""
        nonce = secrets.token_bytes(12)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce), backend=default_backend())
        encryptor = cipher.encryptor()
        ciphertext = encryptor.update(data) + encryptor.finalize()
        return nonce + encryptor.tag + ciphertext
    
    def decrypt_data(self, encrypted_data, key):
        """Decrypt data using AES-256-GCM"""
        nonce = encrypted_data[:12]
        tag = encrypted_data[12:28]
        ciphertext = encrypted_data[28:]
        
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        return decryptor.update(ciphertext) + decryptor.finalize()
    
    def handle_client(self, client_socket, address):
        """Handle individual client connection"""
        print(f"[*] Client connected: {address}")
        
        try:
            # Perform handshake
            client_hello = client_socket.recv(1024)
            if not client_hello:
                return
                
            # Simple key exchange (in production use proper ECDH)
            client_pubkey = client_hello[:32]
            shared_secret = hashlib.sha256(self.server_private_key + client_pubkey).digest()
            client_socket.send(self.server_public_key + b"HELLO")
            
            # Establish encrypted tunnel
            while self.running:
                try:
                    encrypted_data = client_socket.recv(4096)
                    if not encrypted_data:
                        break
                        
                    decrypted_data = self.decrypt_data(encrypted_data, shared_secret)
                    
                    # Process tunnel data (simplified - forward to actual destination)
                    response = self.process_tunnel_data(decrypted_data)
                    encrypted_response = self.encrypt_data(response, shared_secret)
                    client_socket.send(encrypted_response)
                    
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Error processing data: {e}")
                    break
                    
        except Exception as e:
            print(f"Error handling client {address}: {e}")
        finally:
            client_socket.close()
            if address in self.clients:
                del self.clients[address]
            print(f"[*] Client disconnected: {address}")
    
    def process_tunnel_data(self, data):
        """Process tunneled data - this is simplified"""
        # In a real VPN, you'd handle actual network packets
        # This is a placeholder for demonstration
        return b"Response: " + data
    
    def start(self):
        """Start the VPN server"""
        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        if self.cert_file and self.key_file:
            context.load_cert_chain(self.cert_file, self.key_file)
        
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        server_socket.bind((self.host, self.port))
        server_socket.listen(5)
        server_socket.settimeout(1.0)
        
        print(f"[*] VPN Server started on {self.host}:{self.port}")
        print(f"[*] Server Public Key: {base64.b64encode(self.server_public_key).decode()}")
        
        try:
            while self.running:
                try:
                    client_socket, address = server_socket.accept()
                    if self.cert_file and self.key_file:
                        client_socket = context.wrap_socket(client_socket, server_side=True)
                    
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, address),
                        daemon=True
                    )
                    client_thread.start()
                except socket.timeout:
                    continue
                except Exception as e:
                    print(f"Accept error: {e}")
        except KeyboardInterrupt:
            print("\n[*] Shutting down VPN server...")
        finally:
            self.running = False
            server_socket.close()

if __name__ == "__main__":
    # For testing without SSL certificate
    server = VPNServer(port=8443)
    server.start()
