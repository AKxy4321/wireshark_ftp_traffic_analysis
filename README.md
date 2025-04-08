Here’s your updated `README.md` with changes reflecting the automation done via `setup_ftp.py`, as well as the revised Python script (`demo_ftp.py`) which now uploads to and downloads from the `uploads/` directory inside the FTP root:

---

```markdown
# 📡 FTP Traffic Capture with Wireshark

This project demonstrates how to generate and capture insecure FTP traffic using a local FTP server and a Python script. The captured packets can be analyzed using Wireshark to observe sensitive data like usernames, passwords, and file contents transmitted in plaintext.

---

## 🛠 Prerequisites

- Arch Linux (or any Linux distro)
- Python 3
- `vsftpd` (Very Secure FTP Daemon)
- Wireshark

---

## 🐧 Setting Up a Local FTP Server on Arch Linux

### 1. Install `vsftpd`:
```bash
sudo pacman -S vsftpd
```

### 2. Run Demo Setup Script:
Use the `setup_ftp.py` script to automatically configure a temporary anonymous FTP server for demo purposes.

```bash
sudo python setup_ftp.py
```

⚠️ This script will:
- Overwrite `/etc/vsftpd.conf` with demo settings
- Enable anonymous login with write access
- Create a read-only FTP root and a writable `uploads/` directory
- Start the `vsftpd` service
- Wait for you to type `STOP` to shut it down and delete the config

---

## 👤 Create a Test File

Create a plaintext file with sensitive-looking content:
```bash
echo "This is confidential data for Wireshark demo." > secret.txt
```

---

## 🐍 Python Script: FTP File Upload & Download

Create a script called `demo_ftp.py` with the following content:

```python
from ftplib import FTP

ftp_host = "127.0.0.1"  # Use your IP if testing over LAN
ftp_user = "anonymous"
ftp_pass = "12345"

ftp = FTP(ftp_host)
ftp.login(user=ftp_user, passwd=ftp_pass)

with open("secret.txt", "rb") as file:
    ftp.storbinary("STOR uploads/secret.txt", file)

with open("downloaded.txt", "wb") as file:
    ftp.retrbinary("RETR uploads/secret.txt", file.write)

ftp.quit()
```

📝 This uses **anonymous login** with a dummy password and interacts with the `uploads/` subdirectory inside the FTP root.

Run the script:
```bash
python demo_ftp.py
```

---

## 📡 Capture Traffic with Wireshark

1. Open Wireshark. (sudo wireshark)
2. Start capture on your active network interface. (lo or loopback in this case)
3. Apply filter:
   ```
   ftp || ftp-data
   ```
4. Run the Python script while capture is ongoing.
5. Look for:
   - `USER anonymous` and password
   - FTP commands like `STOR uploads/secret.txt` and `RETR`
   - File contents in `ftp-data` packets

---

## 🔐 Observed Security Risk

- **FTP transmits data in plaintext**, including login and file contents.
- Anyone on the same network can intercept and read this data using packet sniffers like Wireshark.

---

## 🛡 Mitigation Recommendations

- Use **SFTP** (Secure FTP over SSH) instead of plain FTP.
- Implement **VPN** for secure tunneling.
- Disable FTP if not needed, or restrict access with a firewall.

---

## 📸 Reporting

For academic reports or security analysis:
- Take **screenshots of captured packets** showing sensitive data.
- Include **recommendations for mitigation**.
- Mention the use of your own local FTP server for testing.

---

## ✅ Done!

You've now created a complete, local FTP demo environment for capturing and analyzing insecure traffic using Wireshark.

---