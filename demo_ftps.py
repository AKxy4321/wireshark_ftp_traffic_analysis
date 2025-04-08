# ftp || tls

from ftplib import FTP_TLS

ftp = FTP_TLS("127.0.0.1")
ftp.login("anonymous", "12345")
ftp.prot_p()  # Enable data encryption

with open("secret.txt", "rb") as f:
    ftp.storbinary("STOR uploads/secret.txt", f)

with open("downloaded.txt", "wb") as f:
    ftp.retrbinary("RETR uploads/secret.txt", f.write)

ftp.quit()
