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
