from CryptoCore.PublicKey import RSA
import hashlib
from CryptoCore.Protocol.KDF import PBKDF2
from base64 import b64decode, b64encode

systems = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    33: 'abcdefghijklmnopqrstuvwxyz2345670',
    64: '0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm/+',
    256: ''.join([chr(x) for x in range(256)])
}
def encode(val, base, minlen=0):
    val = int(val)
    base, minlen = int(base), int(minlen)
    code_string = get_code_string(base)
    result = ''
    while val > 0:
        result = code_string[val % base] + result
        val //= base
    return code_string[0] * max(minlen - len(result), 0) + result
def decode(string, base):
    string = str(string)
    base = int(base)
    code_string = get_code_string(base)
    result = 0
    if base == 16:
        string = string.lower()
    while len(string) > 0:
        result *= base
        result += code_string.find(string[0])
        string = string[1:]
    return int(result)
def get_code_string(base):
    if base in systems:
        return systems[base]
    else:
        raise ValueError("Invalid base!")
def sha256_16(arc):
    return hashlib.sha256(str(arc).encode()).hexdigest()
def generate_Private(password,bits = 1024): #class type
    salt = sha256_16(password)     # replace with random salt if you can store one
    master_key = sha256_16(password+salt)  # bigger count = better

    def my_rand(n):
        my_rand.counter += 1
        x = b''
        y = ""
        while(len(x)<n):
            y = sha256_16(y[32::]+master_key+str(my_rand.counter))
            j = 0
            while(j<len(y) and len(x)<n):
                k = decode(y[j]+y[j+1],'16')
                x += bytes(k.to_bytes((k.bit_length() + 7) // 8, 'big'))
                j+=2;
        return x[:n]
        # return PBKDF2(master_key, "my_rand:%d" % my_rand.counter, dkLen=n, count=1)
    my_rand.counter = 0

    RSA_key = RSA.generate(bits, randfunc=my_rand)
    return RSA_key
def get_Public(private_key): # class type
    return private_key.publickey()
def get_string(key, format = 'PEM'):
    return key.exportKey(format).decode()
def PrivToPub(password):
    priv = generate_Private(password)
    lol = get_string(get_Public(priv))
    return lol
def PubToAdr(Public):
    Public = str(Public).encode()
    public_key = RSA.importKey(Public)
    Adress = get_string(public_key,'OpenSSH')
    return Adress
def AdrToPub(Adress):
    Adress = b'Sakaar: ' + str(Adress).encode()
    public_key = RSA.importKey(Adress)
    Public = get_string(public_key)
    return Public
def PubCode(message, public_key):
    message = int(message)
    public_key = str(public_key)
    public_key = RSA.importKey(public_key.encode())
    # return public_key.encrypt(message)
    return int(public_key.encrypt(message))
def PrivCode(ciphertext, private_key):
    ciphertext = int(ciphertext)
    private_key = generate_Private(private_key)
    ciphertext = str ( ciphertext)
    # return private_key.decrypt(ciphertext)
    return int(private_key.decrypt(ciphertext))
