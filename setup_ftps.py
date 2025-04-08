# ftp || tls

import os
import shutil
import subprocess

CONFIG_PATH = "/etc/vsftpd.conf"
CERT_PATH = "/etc/ssl/private/vsftpd.pem"
anon_root = os.path.join(os.getcwd(), "ftp")
upload_dir = os.path.join(anon_root, "uploads")


def generate_ssl_certificate():
    print("[*] Generating self-signed SSL certificate...")
    os.makedirs(os.path.dirname(CERT_PATH), exist_ok=True)

    subprocess.run(
        [
            "openssl",
            "req",
            "-x509",
            "-nodes",
            "-days",
            "365",
            "-newkey",
            "rsa:2048",
            "-keyout",
            CERT_PATH,
            "-out",
            CERT_PATH,
            "-subj",
            "/C=US/ST=Denial/L=Nowhere/O=Dis/CN=ftpd.local",
        ],
        check=True,
    )
    os.chmod(CERT_PATH, 0o644)
    print(f"[+] SSL certificate created at {CERT_PATH}")


def cleanup_files():
    print("[*] Cleaning up config, cert, and FTP root...")
    if os.path.exists(CONFIG_PATH):
        os.remove(CONFIG_PATH)
    if os.path.exists(CERT_PATH):
        os.remove(CERT_PATH)
    if os.path.exists(anon_root):
        shutil.rmtree(anon_root)
    print("[+] Cleanup complete.")


def setup_ftp_dirs():
    os.makedirs(upload_dir, exist_ok=True)
    os.chmod(anon_root, 0o555)
    os.chmod(upload_dir, 0o777)


ftps_config = f"""
listen=YES
listen_ipv6=NO
anonymous_enable=YES
anon_root={anon_root}
anon_upload_enable=YES
anon_mkdir_write_enable=YES
write_enable=YES
local_enable=YES
allow_writeable_chroot=YES
anon_umask=022

allow_anon_ssl=YES
ssl_enable=YES
rsa_cert_file={CERT_PATH}
rsa_private_key_file={CERT_PATH}
ssl_tlsv1=YES
ssl_sslv2=NO
ssl_sslv3=NO
require_ssl_reuse=NO
ssl_ciphers=HIGH
"""


def create_and_apply_config():
    print("[*] Writing vsftpd config...")
    with open(CONFIG_PATH, "w") as f:
        f.write(ftps_config)

    print("[*] Restarting vsftpd service...")
    subprocess.run(["systemctl", "restart", "vsftpd"], check=True)

    # print("[*] Checking vsftpd status...")
    # subprocess.run(["systemctl", "status", "vsftpd"])
    # print("[*] Checking if port 21 is open...")
    # subprocess.run(["ss", "-tuln"])
    print("[+] FTPS server started.")


def delete_config_and_stop_server():
    print("[*] Stopping vsftpd service...")
    subprocess.run(["systemctl", "stop", "vsftpd"], check=True)
    print("[+] vsftpd service stopped.")
    cleanup_files()


def main():
    cleanup_files()
    generate_ssl_certificate()
    setup_ftp_dirs()
    create_and_apply_config()

    cmd = input(
        "\n📡 FTPS server running with demo config.\n🛑 Type 'STOP' to stop server and clean up: "
    )
    if cmd.strip().upper() == "STOP":
        delete_config_and_stop_server()


if __name__ == "__main__":
    if os.geteuid() != 0:
        print("❌ Please run this script as root (use sudo).")
    else:
        main()
