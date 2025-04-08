
```markdown
# 📡 FTP & FTPS Traffic Capture with Wireshark

This project demonstrates how to generate and capture **both insecure FTP and secure FTPS** traffic using a local server and Python scripts. It is intended for educational use — particularly for analyzing how sensitive data travels over the network using tools like **Wireshark**.

---

## 🛠 Prerequisites

- Arch Linux (or any Linux distro)
- Python 3
- `vsftpd` (Very Secure FTP Daemon)
- `openssl` (for generating SSL certificates)
- Wireshark

---

## 🐧 Setting Up Local FTP/FTPS Servers

### 1. Install `vsftpd`:
```bash
sudo pacman -S vsftpd
```

---

### 2. Set Up Insecure FTP Server:
```bash
sudo python3 setup_ftp.py
```

📌 This will:
- Overwrite `/etc/vsftpd.conf` with a demo config
- Enable anonymous login with write access
- Create `ftp/` with a read-only root and writable `uploads/` directory
- Start `vsftpd`
- Wait for you to type `STOP` to shut down and clean up

---

### 3. Set Up Secure FTPS Server:
```bash
sudo python3 setup_ftps.py
```

📌 This will:
- Generate a self-signed SSL certificate at `/etc/ssl/private/vsftpd.pem`
- Configure FTPS (TLS over FTP) via `/etc/vsftpd.conf`
- Enable anonymous login with SSL encryption
- Start `vsftpd`
- Wait for you to type `STOP` to shut down and clean up

---

## 👤 Create a Test File

Create a plaintext file with sensitive-looking content:
```bash
echo "This is confidential data for Wireshark demo." > secret.txt
```

---

## 🐍 FTP Client Script: `demo_ftp.py`

```python
from ftplib import FTP

ftp = FTP("127.0.0.1")
ftp.login("anonymous", "12345")

with open("secret.txt", "rb") as f:
    ftp.storbinary("STOR uploads/secret.txt", f)

with open("downloaded.txt", "wb") as f:
    ftp.retrbinary("RETR uploads/secret.txt", f.write)

ftp.quit()
```

Run:
```bash
python3 demo_ftp.py
```

---

## 🐍 FTPS Client Script: `demo_ftps.py`

```python
from ftplib import FTP_TLS

ftp = FTP_TLS("127.0.0.1")
ftp.login("anonymous", "12345")
ftp.prot_p()  # Enable encrypted data transfer

with open("secret.txt", "rb") as f:
    ftp.storbinary("STOR uploads/secret.txt", f)

with open("downloaded.txt", "wb") as f:
    ftp.retrbinary("RETR uploads/secret.txt", f.write)

ftp.quit()
```

Run:
```bash
python3 demo_ftps.py
```

---

## 📡 Capture Traffic with Wireshark

1. Open Wireshark (`sudo wireshark`)
2. Start capture on your network interface (`lo` for localhost)
3. Apply one of the following capture filters:

   - For **FTP (insecure)**:
     ```
     ftp || ftp-data
     ```
     Observe plaintext credentials and file content.

   - For **FTPS (secure)**:
     ```
     tls
     ```
     Observe encrypted traffic — FTP commands and data are not visible.
4. Run the FTP or FTPS demo script while capturing
5. Observe:
   - `USER anonymous` and password (for FTP)
   - `STOR` / `RETR` commands
   - File contents in plaintext (only for FTP)
   - Encrypted payloads (for FTPS)

---

## 🔐 Observed Security Risk (FTP)

- FTP sends usernames, passwords, and files in **plaintext**
- Anyone monitoring the network can intercept and read the data
- FTPS encrypts all communication, making eavesdropping ineffective

---

## 🛡 Recommendations

- Avoid FTP in production
- Prefer **SFTP** (over SSH) or **FTPS**
- Use **firewalls** and **VPNs** to isolate FTP/FTPS access
- Regularly audit exposed services and ports

---

## 📸 Reporting Tips

For academic reports or security analysis:
- Take **screenshots of packet captures**
- Highlight plaintext credentials or file data in FTP
- Compare with encrypted payloads in FTPS
- Include **mitigation strategies**

---

## ✅ Done!

You've successfully built a working lab to demonstrate both insecure and secure FTP traffic. Use it to understand network protocol behavior and security implications in real time using Wireshark.

---