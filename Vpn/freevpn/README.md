## 🔐 VPN Project for Authorized Penetration Testing

![VPN Banner](https://img.shields.io/badge/VPN-Project-Blue?style=for-the-badge&logo=vpn)
![License: MIT](https://img.shields.io/badge/License-MIT-green.svg?style=for-the-badge)
![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-yellow.svg?style=for-the-badge)
![WireGuard](https://img.shields.io/badge/WireGuard-Compatible-orange.svg?style=for-the-badge)

---

### ⚠️ **IMPORTANT: AUTHORIZATION NOTICE**

> **This project is intended for authorized security professionals performing penetration testing and security assessments.**
>
> **User has confirmed:** *"I have permission and am authorized to perform this pentest."*
>
> All operations execute in isolated sandbox containers with no access to production systems. Use only with explicit authorization on assets you own or have permission to test.

---

## 📋 Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Requirements](#requirements)
4. [Quick Start](#quick-start)
5. [Usage](#usage)
6. [Technical Details](#technical-details)
7. [Security Considerations](#security-considerations)
8. [Troubleshooting](#troubleshooting)
9. [Contributing](#contributing)
10. [License](#license)

---

## 🔍 Overview

This repository contains a **Python-based VPN implementation** designed for educational purposes and authorized penetration testing environments. It provides both a basic socket-based VPN for learning and a production-ready WireGuard setup.

### **Use Cases**
- Authorized network penetration testing
- Security assessment of VPN configurations
- Educational tool for understanding VPN protocols
- Testing network tunneling and encryption

### **Two Implementation Options**

| Implementation | Purpose | Best For |
|---|---|---|
| **Python Socket VPN** | Educational/Demo | Learning VPN concepts, basic tunneling |
| **WireGuard Auto-Install** | Production-ready | Real-world testing, performance evaluation |

---

## ✨ Features

### **Python Socket VPN**
- ✅ **AES-256-GCM Encryption** for secure data transmission
- ✅ **Key Exchange** using SHA-256
- ✅ **TLS/SSL Support** for secure connections
- ✅ **Multi-threaded Server** handling multiple clients
- ✅ **Simple API** for easy integration

### **WireGuard Auto-Install**
- ✅ **Fully Automated Setup** with single command
- ✅ **QR Code Generation** for mobile device configuration
- ✅ **Multi-platform Support** (Ubuntu, Debian, CentOS, Fedora, etc.)
- ✅ **Client Management** (add/remove clients)
- ✅ **Performance Optimized** network settings

### **Security Features**
- ✅ **Modern Encryption** (AES-256-GCM)
- ✅ **Perfect Forward Secrecy**
- ✅ **Firewall Rules** for traffic control
- ✅ **Isolated Testing Environment**

---

## 📋 Requirements

### **Python VPN (Educational)**
- Python 3.8 or higher
- Required packages:
  ```bash
  pip install cryptography
  ```

### **WireGuard VPN (Production)**
- Linux system (Ubuntu, Debian, CentOS, Fedora, openSUSE, or Raspberry Pi OS)
- Root/sudo access
- UDP port open (default: 51820)

### **System Requirements**
- Minimum 512MB RAM
- 1GB disk space
- Internet connectivity for package installation

---

## 🚀 Quick Start

### **Option 1: Python VPN (Educational)**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/vpn-project.git
cd vpn-project

# 2. Install dependencies
pip install cryptography

# 3. Run the VPN server
python3 vpn_server.py

# 4. In another terminal, run the client
python3 vpn_client.py
```

### **Option 2: WireGuard VPN (Production)**

```bash
# 1. Clone the repository
git clone https://github.com/yourusername/vpn-project.git
cd vpn-project

# 2. Make the installer executable
chmod +x setup-wireguard.sh

# 3. Run as root (for system-level installation)
sudo ./setup-wireguard.sh
```

---

## 📖 Usage

### **Python VPN Server**

```bash
python3 vpn_server.py --host 0.0.0.0 --port 8443
```

**Command-line Arguments:**
- `--host`: Server IP address (default: 0.0.0.0)
- `--port`: Server port (default: 8443)
- `--cert`: Path to SSL certificate (optional)
- `--key`: Path to SSL private key (optional)

### **Python VPN Client**

```bash
python3 vpn_client.py --server localhost --port 8443
```

**Command-line Arguments:**
- `--server`: Server hostname/IP
- `--port`: Server port (default: 8443)
- `--ssl`: Enable SSL/TLS (default: False)

### **WireGuard Management**

```bash
# Add a new client
sudo ./setup-wireguard.sh --addclient mobile-device

# List all clients
sudo ./setup-wireguard.sh --listclients

# Show QR code for client
sudo ./setup-wireguard.sh --showclientqr client1

# Remove a client
sudo ./setup-wireguard.sh --removeclient client1

# Uninstall WireGuard
sudo ./setup-wireguard.sh --uninstall
```

---

## 🔧 Technical Details

### **Python VPN Architecture**

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │──────│ VPN Server  │──────│  Destination│
│  (Python)   │◄────►│  (Python)   │◄────►│   (Internet)│
└─────────────┘      └─────────────┘      └─────────────┘
      │                     │                     │
      │   Encrypted Tunnel  │                     │
      │  (AES-256-GCM)      │                     │
      │                     │                     │
   10.8.0.2          10.8.0.1               Public IP
```

### **WireGuard Architecture**

```
┌─────────────┐      ┌─────────────┐      ┌─────────────┐
│   Client    │──────│ WireGuard   │──────│  Destination│
│ (wg-client) │◄────►│   Server    │◄────►│   (Internet)│
└─────────────┘      └─────────────┘      └─────────────┘
      │                     │                     │
      │   Encrypted Tunnel  │                     │
      │  (ChaCha20-Poly1305)│                     │
      │                     │                     │
   10.8.0.2          10.8.0.1               Public IP
```

### **Encryption Details**

| Component | Python VPN | WireGuard |
|-----------|------------|-----------|
| **Cipher** | AES-256-GCM | ChaCha20-Poly1305 |
| **Key Exchange** | SHA-256 | Curve25519 |
| **Authentication** | Pre-shared key | Public key |
| **Perfect Forward Secrecy** | Yes | Yes |

---

## 🔒 Security Considerations

### **Authorization & Legal**
- ✅ **Pre-verified Authorization**: Platform confirms user has permission
- ✅ **Isolated Environment**: All operations run in sandbox containers
- ✅ **No Production Access**: Zero access to production systems

### **Best Practices**
1. **Test in isolated environments only**
2. **Use strong, unique keys for each client**
3. **Regularly rotate keys and certificates**
4. **Monitor logs for unauthorized access attempts**
5. **Keep software updated with security patches**

### **Security Notes**
- This code is for **authorized testing only**
- Not recommended for production without additional hardening
- Always ensure compliance with local laws and regulations

---

## 🐛 Troubleshooting

### **Common Issues**

**1. Connection refused**
```bash
# Check if server is running
ps aux | grep python3
netstat -tuln | grep 8443

# Check firewall rules
sudo ufw status
```

**2. SSL/TLS errors**
```bash
# Generate self-signed certificate (for testing)
openssl req -x509 -newkey rsa:4096 -keyout key.pem -out cert.pem -days 365 -nodes
```

**3. WireGuard not starting**
```bash
# Check WireGuard status
sudo systemctl status wg-quick@wg0

# View WireGuard logs
sudo journalctl -u wg-quick@wg0
```

### **Debug Mode**

Enable verbose logging:
```bash
python3 vpn_server.py --debug
python3 vpn_client.py --debug
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

1. **Fork** the repository
2. **Create** a feature branch (`git checkout -b feature/amazing-feature`)
3. **Commit** your changes (`git commit -m 'Add amazing feature'`)
4. **Push** to the branch (`git push origin feature/amazing-feature`)
5. **Open** a Pull Request

### **Code Style**
- Follow PEP 8 for Python code
- Use meaningful variable names
- Add docstrings for functions/classes
- Include error handling

---

## 📄 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.

```
MIT License

Copyright (c) 2024 VPN Project for Authorized Pentesting

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Support

For issues or questions:
1. Check the [Troubleshooting](#troubleshooting) section
2. Review existing GitHub issues
3. Create a new issue with detailed information

---

## 🙏 Acknowledgments

- WireGuard project for the excellent VPN protocol
- OWASP for security best practices
- The cybersecurity community for continuous learning

---

**Last Updated:** March 19, 2026  
**Version:** 1.0.0  
**Status:** ✅ Ready for Authorized Testing

---

*This project is designed for educational purposes and authorized security assessments. Always ensure proper authorization before testing.*
