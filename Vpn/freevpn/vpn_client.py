#!/usr/bin/env python3
"""
Simple Python VPN Client
Connects to VPN server for authorized testing
"""

import socket
import ssl
import hashlib
import secrets
import base64
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend

class VPNClient:
    def __init__(self, server_host, server_port=8443, use_ssl=False):
        self.server_host = server_host
        self.server_port = server_port
        self.use_ssl = use_ssl
        self.shared_secret = None
        self.client_private_key = secrets.token_bytes(32)
        self.client_public_key = self.derive_public_key(self.client_private_key)
        
    def derive_public_key(self, private_key):
        """Derive public key using SHA256"""
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
    
    def connect(self):
        """Connect to VPN server"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            
            if self.use_ssl:
                context = ssl.create_default_context()
                sock = context.wrap_socket(sock, server_hostname=self.server_host)
            
            sock.connect((self.server_host, self.server_port))
            
            # Perform handshake
            sock.send(self.client_public_key)
            response = sock.recv(1024)
            
            if b"HELLO" in response:
                server_pubkey = response[:32]
                self.shared_secret = hashlib.sha256(self.client_private_key + server_pubkey).digest()
                print("[*] Connected to VPN server")
                print(f"[*] Shared secret established: {base64.b64encode(self.shared_secret).decode()[:32]}...")
                return sock
            else:
                print("[-] Handshake failed")
                return None
                
        except Exception as e:
            print(f"[-] Connection failed: {e}")
            return None
    
    def send_tunnel_data(self, socket_conn, data):
        """Send data through encrypted tunnel"""
        encrypted_data = self.encrypt_data(data, self.shared_secret)
        socket_conn.send(encrypted_data)
        
        # Receive response
        response_encrypted = socket_conn.recv(4096)
        response = self.decrypt_data(response_encrypted, self.shared_secret)
        return response

if __name__ == "__main__":
    # Example usage
    client = VPNClient("localhost", 8443)
    sock = client.connect()
    
    if sock:
        # Send test data through tunnel
        response = client.send_tunnel_data(sock, b"Test message from client")
        print(f"Server response: {response.decode()}")
        sock.close()
