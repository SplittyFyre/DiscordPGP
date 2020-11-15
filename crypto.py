import gnupg

recipient = None

gpg = gnupg.GPG()

def encrypt(msg : str):
    cipher = gpg.encrypt(msg, recipient, always_trust=True)
    if cipher.ok:
        return True, str(cipher)
    else:
        return False, cipher.status