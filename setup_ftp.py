# ftp || ftp-data

import os
import shutil
import subprocess

CONFIG_PATH = "/etc/vsftpd.conf"
anon_root = os.path.join(os.getcwd(), "ftp")

if os.path.exists(anon_root):
    shutil.rmtree(anon_root)

if not os.path.exists(anon_root):
    os.makedirs(anon_root)
    os.chmod(anon_root, 0o555)  # Make the root read-only

upload_dir = os.path.join(anon_root, "uploads")
if not os.path.exists(upload_dir):
    os.makedirs(upload_dir, exist_ok=True)
    os.chmod(upload_dir, 0o777)  # uploads/ is writable


demo_config = f"""
anonymous_enable=YES
local_enable=YES
write_enable=YES
anon_root={anon_root}
allow_writeable_chroot=YES
anon_upload_enable=YES
anon_mkdir_write_enable=YES
anon_umask=022
"""


def create_and_apply_config():
    print("[*] Writing config...")
    with open(CONFIG_PATH, "w") as f:
        f.write(demo_config)

    print("[*] Restarting vsftpd service...")
    subprocess.run(["systemctl", "restart", "vsftpd"], check=True)
    print("[+] vsftpd started with demo config.")


def delete_config():
    if os.path.exists(CONFIG_PATH):
        print("[*] Deleting demo config...")
        os.remove(CONFIG_PATH)
    else:
        print("[!] Config file not found.")

    print("[*] Stopping vsftpd service...")
    subprocess.run(["systemctl", "stop", "vsftpd"], check=True)
    print("[+] vsftpd stopped and config deleted.")


def main():
    create_and_apply_config()
    cmd = input(
        "\n📡 FTP server running with demo config.\n🛑 Type 'STOP' and press Enter to stop the server and delete the config : "
    )
    if cmd.strip().upper() == "STOP":
        delete_config()


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("❌ Run this script as root (use sudo).")
    else:
        main()
