# Navigator Cryptography
from cryptography.fernet import Fernet
import os,base64,json


# CREATE NEW KEY -> ENCODE B64 -> WRITE TO FILE
def createKey(filename):
    if filename is None: fName = 'Key.txt'
    else: fName = filename
    with open(fName, 'wb') as file: file.write(base64.b64encode(Fernet.generate_key()))


# WRITE ENCRYPTED RECORDS DATA
def encryptData(dataPath,keyPath):
    if keyPath is None: kPath = 'Key.txt'
    else: kPath = keyPath
    with open(kPath, 'rb') as file: key = base64.b64decode(file.read())

    if dataPath is None: dPath = 'Data.txt'
    else: dPath = dataPath

    try:
        with open (dPath,'rb') as file: data = json.load(file)
        encrypted = Fernet(key).encrypt(json.dumps(data).encode())
        with open('Encrypted'+dPath,'wb') as file: file.write(encrypted)
    except Exception as e: print(f"No data to encrypt{e}")


# WRITE ENCRYPTED TOKEN
def encryptToken(tokenPath,keyPath):
    if keyPath is None: kPath = 'Key.txt'
    else: kPath = keyPath
    with open(kPath,'rb') as file: key = base64.b64decode(file.read())

    if tokenPath is None: tPath = 'Token.txt'
    else: tPath = tokenPath

    try:
        with open (tPath,'r') as file: data = file.read()
        encrypted = Fernet(key).encrypt(data.encode())
        with open('Encrypted'+tPath,'wb') as file: file.write(encrypted)
    except Exception as e:print(f"No token to encrypt {e}")


# READ ENCRYPTED RECORDS DATA
def decryptData(dataPath,keyPath):
    if keyPath is None: kPath = 'Key.txt'
    else: kPath = keyPath
    with open(kPath,'rb') as file: key = base64.b64decode(file.read())

    if dataPath is None: dPath = 'EncryptedData.txt'
    else: dPath = dataPath

    try:
        with open(dPath,'rb') as file: encrypted = file.read()
        decrypted = json.loads(Fernet(key).decrypt(encrypted))
        with open('Decrypted'+dPath,'wb') as file: file.write(decrypted)
    except Exception as e: print(f"No records to decrypt {e}")


# READ ENCRYPTED TOKEN
def decryptToken(tokenPath,keyPath):
    if keyPath is None: kPath = 'Key.txt'
    else: kPath = keyPath
    with open(kPath,'rb') as file: key = base64.b64decode(file.read())

    if tokenPath is None: tPath = 'EncryptedToken.txt'
    else: tPath = tokenPath

    try:
        with open (tPath,'rb') as file: token = file.read()
        try:
            decrypted=Fernet(key).decrypt(token.decode())
            with open('Decrypted'+tPath,'wb') as file: file.write(decrypted)
        except Exception as e: print(f"Failed to decrypt token {e}")
    except Exception as e: print(f"No token to decrypt {e}")





if __name__ == '__main__':
    createKey(None)
    encryptData(None,None)
    #decryptData(None,None)
    encryptToken(None,None)
    #decryptToken(None,None)
