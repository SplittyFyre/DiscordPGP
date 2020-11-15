import gnupg
import base64

recipient = None

gpg = gnupg.GPG()

def encrypt(msg : str):
    cipher = gpg.encrypt(msg, recipient, always_trust=True, armor=False)
    if cipher.ok:
        return True, base64.b64encode(cipher.data).decode('ascii')
    else:
        return False, cipher.status

def decrypt(msg : str):
    plain = gpg.decrypt()