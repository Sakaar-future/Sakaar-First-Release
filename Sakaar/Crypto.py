from CryptoCore.PublicKey import RSA
import hashlib

systems = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    33: 'abcdefghijklmnopqrstuvwxyz2345670',
    64: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
    256: ''.join([chr(x) for x in range(256)])
}


def encode(val: int, base: int, minlen: int = 0) -> str:
    val = int(val)
    base, minlen = int(base), int(minlen)
    code_string = get_code_string(base)
    result = ''
    while val > 0:
        result = code_string[val % base] + result
        val //= base
    return code_string[0] * max(minlen - len(result), 0) + result


def decode(string: str, base: int) -> int:
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


def C16_256(str1: str) -> str:
    if len(str1) % 2 == 1:
        str1 = '0' + str1
    code_16 = get_code_string(16)
    code_256 = get_code_string(256)

    res = ''
    i = 0
    while i < len(str1):
        x = code_16.find(str1[i]) * 16 + code_16.find(str1[i + 1])
        res += code_256[x]
        i += 2
    return res


def C256_16(str1: str) -> str:
    code_16 = get_code_string(16)
    code_256 = get_code_string(256)

    res = ''
    for i in str1:
        x = code_256.find(i)
        res += '' + code_16[x // 16] + code_16[x % 16]
    return res


def get_code_string(base: int) -> object:
    if base in systems:
        return systems[base]
    else:
        raise ValueError("Invalid base!")


def sha256_16(arc: str) -> str:
    return hashlib.sha256(str(arc).encode()).hexdigest()


def generate_Private(password: str, bits: int = 1024) -> object:
    salt = sha256_16(password)  # replace with random salt if you can store one
    master_key = sha256_16(password + salt)  # bigger count = better

    def my_rand(n):
        my_rand.counter += 1
        x = b''
        y = ""
        while (len(x) < n):
            y = sha256_16(y[32::] + master_key + str(my_rand.counter))
            j = 0
            while (j < len(y) and len(x) < n):
                k = decode(y[j] + y[j + 1], '16')
                x += bytes(k.to_bytes((k.bit_length() + 7) // 8, 'big'))
                j += 2;
        return x[:n]

    my_rand.counter = 0

    RSA_key = RSA.generate(bits, randfunc=my_rand)
    return RSA_key


def get_Public(private_key: object) -> str:
    return private_key.publickey()


def get_string(key: object, format: str = 'PEM') -> str:
    return key.exportKey(format).decode()


def PrivToPub(password: str) -> str:
    priv = generate_Private(password)
    lol = get_string(get_Public(priv))
    return lol


def PubToAdr(Public: str) -> str:
    Public = str(Public).encode()
    public_key = RSA.importKey(Public)
    Adress = get_string(public_key, 'OpenSSH')
    return Adress


def AdrToPub(Adress: str) -> str:
    Adress = b'Sakaar: ' + str(Adress).encode()
    public_key = RSA.importKey(Adress)
    Public = get_string(public_key)
    return Public


def PubCode(message: int, public_key: str) -> int:
    message = int(message)
    public_key = str(public_key)
    public_key = RSA.importKey(public_key.encode())
    # return public_key.encrypt(message)
    return int(public_key.encrypt(message))


def PrivCode(ciphertext: int, private_key: str) -> int:
    ciphertext = int(ciphertext)
    private_key = generate_Private(private_key)
    ciphertext = str(ciphertext)
    # return private_key.decrypt(ciphertext)
    return int(private_key.decrypt(ciphertext))
