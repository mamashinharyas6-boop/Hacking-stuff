# 🛡️ Project: Net-Sec & Bot Research
A collection of documentation, scripts, and findings regarding Discord API security, network protocols, and IP forensics.

## 🤖 Discord Bot Security
Understanding how bots interact with the Discord API is crucial for both development and defense. My research focuses on:

* **Token Security:** How to prevent token leakage and the risks of hardcoding credentials.
* **Permission Escalation:** Analyzing how poorly configured `Administrator` flags can lead to server "nukes."
* **Webhooks:** The mechanics of using webhooks for data exfiltration or automated logging.
* **Rate Limiting:** Understanding Discord’s global and local rate limits to prevent API bans.

## 🌐 Network & IP Intelligence
Exploring how data moves across the web and how identities are mapped digitally.

| Category | Concepts Covered |
| :--- | :--- |
| **Discovery** | Public vs. Private IP addresses, DHCP, and Static assignments. |
| **Geolocating** | Using database lookups (like MaxMind) to estimate physical location. |
| **OSINT** | Correlating IP data with DNS records and open ports (Nmap/Shodan). |
| **Protection** | The role of VPNs, Proxies, and Tor in masking network footprints. |

## ⚠️ Disclaimer
> "Knowledge is a tool, not a weapon."
> 
> This repository is for **educational and ethical security research only**. Unauthorized access to systems or accounts is illegal and unethical. Always practice "White Hat" principles.

---

### 🛠️ Tools Used
* **Language:** Python (discord.py / hikari)
* **Analysis:** Wireshark, Nmap
* **Platform:** Linux / Termux
