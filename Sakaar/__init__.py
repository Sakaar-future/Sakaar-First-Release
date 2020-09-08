from threading import Thread
from .Cripto import *
import os,json
from time import time as time_time, sleep as time_sleep
from random import randint
from sqlite3 import connect as sql3connect
from shelve import open as shelve_open
from requests import post as requests_post
from flask import Flask, g, request, jsonify, make_response
from base64 import b64decode, b64encode
from pyngrok import ngrok
from flask_cors import CORS

Version = '1.000'
# b'A\xdeQ<\xdd*;\t\x1f\xe9Dy\xf07J\xb6'

app = Flask(__name__)
CORS(app)
conn = sql3connect('Sakaar/exmp1.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS UserOF(
    Address         varchar(128)    NOT NULL,
    PubKey             varchar(128)    NOT NULL,
    Active            BOOL            NOT NULL,
    Masseges        Text            NOT NULL,
    Balance            Text            NOT NULL,
    Time            Double             NOT NULL) ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS ATran(
    PubKey1            varchar(128)    NOT NULL,
    PubKey2            varchar(128)    NOT NULL,
    Sum                Double            NOT NULL,
    Comis            Double            NOT NULL,
    Wallet            varchar(16)        NOT NULL,
    Time            Double             NOT NULL,
    AddressFrom        varchar(128)    NOT NULL)
     ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS History(
    Num                int             NOT NULL,
    PubKey1            varchar(128)    NOT NULL,
    PubKey2            varchar(128)    NOT NULL,
    Sum                Double            NOT NULL,
    Comis            Double            NOT NULL,
    Wallet            varchar(16)        NOT NULL,
    Time            Double             NOT NULL,
    AddressFrom        varchar(128)    NOT NULL,
    Comision        Text            NOT NULL,
    MesInsageIn            Text,
    MesInsageOut            Text
    ) ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS Orders(
    Address1        varchar(128)    NOT NULL,
    Address2        varchar(128)    NOT NULL,
    AddressFrom        varchar(128)    NOT NULL,
    Wallet1            varchar(16)        NOT NULL,
    Wallet2            varchar(16)        NOT NULL,
    Sum1            Double            NOT NULL,
    SumS            Double            NOT NULL,
    k                 Double            NOT NULL,
    t                 Double,
    t1                Double,
    priv             varchar(128)    NOT NULL) ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS Orders_H(
    k                 Double            NOT NULL,
    t                 Double            NOT NULL,
    Wallet1           varchar(16)       NOT NULL,
    Wallet2           varchar(16)       NOT NULL,
    Num               int               NOT NULL,
    AddressTo         varchar(128)      NOT NULL,
    AddressFrom       varchar(128)      NOT NULL,
    Sum               Double            NOT NULL
) ''')
conn.commit()
conn.close()


class conf:

    conf = None
def get_conf():
    # pass
    conf.conf = getattr(conf.conf,'_conf',None)
    if conf.conf is None:
        conf.conf = shelve_open('conf')
    return conf
get_conf()
# conf.conf['Connected'] = ['194aa871eb04.ngrok.io']
# conf.conf['SUPERIP'] = ['194aa871eb04.ngrok.io']
conf.conf['MyIP'] = None
if 'Connected' not in conf.conf:
    conf.conf['Connected'] = ['194aa871eb04.ngrok.io']
if 'SUPERIP' not in conf.conf:
    conf.conf['SUPERIP'] = ['194aa871eb04.ngrok.io']
if 'OurWallets' not in conf.conf:
    conf.conf['OurWallets'] = []
if 'OtherWallets' not in conf.conf:
    conf.conf['OtherWallets'] = []
if 'InMemory' not in conf.conf:
    conf.conf['InMemory'] = []
if 'FullFreez' not in conf.conf:
    conf.conf['FullFreez'] = 0.0
if 'Comis' not in conf.conf:
    conf.conf['Comis'] = 0.001
if 'Voiting' not in conf.conf:
    conf.conf['Voiting'] = {}
if 'Voited' not in conf.conf:
    conf.conf['Voited'] = {}
if 'Version' not in conf.conf:
    conf.conf['Version'] = Version
if 'login' not in conf.conf:
    conf.conf['login'] = ''
if 'Link' not in conf.conf:
    conf.conf['Link'] = 'DB';
if 'isServer' not in conf.conf:
    conf.conf['isServer'] = False
if 'isSUPER' not in conf.conf:
    conf.conf['isSUPER'] = False
if 'In' not in conf.conf:
    conf.conf['In'] = False
if 'login' not in conf.conf:
    conf.conf['login'] = ''
if 'PrivKey' not in conf.conf:
    conf.conf['PrivKey'] = ''
if 'passw' not in conf.conf:
    conf.conf['passw'] = ''
if 'isRunning' not in conf.conf:
    conf.conf['isRunning'] = False
if 'Block' not in conf.conf:
    conf.conf['Block'] = 0
if 'MyIP' not in conf.conf:
    conf.conf['MyIP'] = None
if 'Key' not in conf.conf:
    conf.conf['Key'] = 'AAAAgQCkuqxx8XsVCOn0+Z3EFogneSuTOXRFsbRIACp8mLiXsv2v44Aa/uCFFpSPvleT/hIkJob+88StiMRQRtmHkbqeN1POfpNO1rPxJT1JONhHISns301hGN5k8ixQIdUiLduP0c7eewwfd1gyMScL+9YlBopQEb18BpzF0tjP+lWOdQ=='

class User:
    def Create(Address = '', PubKey = '', Wallet = '', AddressTo = '', FuncH = '', Func = '', AddressFrom = ''):# AddressFrom - Other Wallets
        if FuncH != '' and Func != '' and AddressTo != '' and PubCode(FuncH, get_UserOF(AddressTo)['PubKey'])== Func:
            Func = FuncH
        else:
            Func      = ''

        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
            Address         varchar(128)     NOT NULL,
            AddressTo         varchar(128) ,
            PubKey             varchar(128)     NOT NULL,
            FuncH             varchar(128) ,
            Func             varchar(128) ,
            Time            Double    ,
            Freez            Double            NOT NULL,
            Balance            Double            NOT NULL,
            Hash            varchar(128)    NOT NULL,
            AddressFrom        varchar(128),
            Wallet             varchar(16)     NOT NULL
            ) ''')
        conn.commit()
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{Address}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO {Wallet} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (Address, AddressTo, PubKey, str(FuncH), str(FuncH), 0, 0.0, 0.0, '', AddressFrom, Wallet))
        conn.commit()
        conn.close()
    def FromSQL(x):
        return {'Address' : x[0], 'AddressTo':x[1], 'PubKey':x[2], 'FuncH':x[3], 'Func':x[4], 'Time':x[5], 'Freez':x[6], 'Balance':x[7], 'Hash':x[8], 'AddressFrom':x[9], 'Wallet':x[10]}

    def ToSQL(x):
        return [x['Address'], x['AddressTo'], x['PubKey'], x['FuncH'], x['Func'], x['Time'], x['Freez'], x['Balance'], x['Hash'], x['AddressFrom'], x['Wallet']]

    def Check(AC, a, RES):
        a = decode(a, 256)
        RES = PubCode(RES, AC['PubKey'] )
        return RES== a

    def ChangeFunc(AC, FuncH, Func):
        if(AC['AddressTo'] != ''):
            PubKey = get_UserOF(AC['AddressTo'])['PubKey']
            RES = PubCode(FuncH, PubKey)
            if RES== Func:
                conn = sql3connect('Sakaar/exmp1.db')
                c = conn.cursor()
                c.execute(f'''UPDATE {AC['Wallet']} SET Func = '{FuncH}' WHERE Address = '{AC['Address']}' ''')
                conn.commit()
                conn.close()

    def getFunc(AC):
        if(AC['AddressTo'] != ''):
            PubKey = get_UserOF(AC['AddressTo'])['PubKey']
            return json.loads(encode(PubCode(AC['Func'], PubKey), 256))
            # return encode(PubCode(self['Func'] , PubKey), 256)

    def CodeFunc(Func, PrivKey):
        Func = json.dumps(Func)
        Func1 = decode(Func, 256)
        return PrivCode(Func1, PrivKey), Func1
class Tranzh:
    def Create (PubKey1, PubKey2, Wal, Sum, Hash1, Hash2, Pass, time, MesIn = '',MesOut = '', Comis = None):
        x = {
            'PubKey1'     : PubKey1,
            'PubKey2'     : PubKey2,
            'Sum'         : Sum,
            'Wal'         : Wal,
            'Hash1'     : Hash1,
            'Hash2'     : Hash2,
            'Pass'         : Pass,
            'MesIn'         : MesIn,
            'MesOut'         : MesOut,
            'time'         : time,
            'Comision'    : []
        }
        if Comis== None or Comis < conf.conf['Comis']:
            x['Comis'] = conf.conf['Comis']
        else:
            x['Comis'] = Comis
        return x
    def ToJSON(dat):
        # dat['Hash1'] = json.dumps(dat['Hash1'])
        # dat['Hash2'] = json.dumps(dat['Hash2'])
        return dat
    def FromJSON(dat):
        # dat['Hash1'] = json.loads(dat['Hash1'])
        # dat['Hash2'] = json.loads(dat['Hash2'])
        return dat
class Tranzhs:
    def Create (TS, AddressTo = None, AddressHashed = None):
        x= {
            'TS'                 : TS,
            'Users'             : [],
            'resTO'             : 0.0,
            'resAnti'             : 0.0,
            'AddressTo'         : AddressTo,
            'AddressHashed'     : AddressHashed
        }
        return x
    def ToJSON(dat):
        # i = 0
        # while i<len(dat['TS']):
        #     dat['TS'][i] = Tranzh.ToJSON(dat['TS'][i])
        #     i+=1
        return dat
    def FromJSON(dat):
        # i = 0
        # while i<len(dat['TS']):
        #     dat['TS'][i] = Tranzh.FromJSON(dat['TS'][i])
        #     i+=1
        return dat
class UserOF:
    def Create(Address = '', PubKey = ''):
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Address}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO UserOF VALUES(?, ?, ?, ?, ?, ?)''', (Address, PubKey, False, json.dumps([]), json.dumps({}), 0))
        conn.commit()
        conn.close()
        # return self
    def FromSQL(x):
        return {'Address' : x[0], 'PubKey':x[1], 'Active':x[2], 'Masseges':json.loads(x[3]), 'Balance':json.loads(x[4]), 'Time':x[5]}

    def ToSQL(x):
        return [x['Address'], x['PubKey'], x['Active'], json.dumps(x['Masseges']), json.dumps(x['Balance']), x['Time']]

    def Check(AC, a, RES):
        a = decode(a, 256)
        RES = PubCode(RES, AC['PubKey'] )
        return RES== a
class Order:
    def Create(Adr1, Wal1,AddressFrom, Sum1, Adr2, Wal2, k, time, priv):
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT * FROM Orders WHERE Wallet1 = '{Wal1}' AND Wallet2 = '{Wal2}' AND Address1 = '{Adr1}' AND AddressFrom = '{AddressFrom}' AND Address2 = '{Adr2}' AND SumS = '{Sum1}' AND k = '{k}' AND t = '{time}' AND priv = '{priv}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO Orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (Adr1, Adr2, AddressFrom, Wal1, Wal2, Sum1, Sum1, k, time, time, priv))
        conn.commit()
        conn.close()


    def FromSQL(x):
        return {'Address1' : x[0], 'Address2':x[1], 'AddressFrom':x[2], 'Wallet1':x[3], 'Wallet2':x[4], 'Sum1':x[5], 'SumS':x[6], 'k':x[7], 't':x[8], 't1':x[9], 'priv':x[10]}

    def ToSQL(x):
        return [x['Address1'], x['Address2'], x['AddressFrom'], x['Wallet1'], x['Wallet2'], x['Sum1'], x['SumS'], x['k'], x['t'], x['t1'], x['priv']]



def Generator(size):
    size = int(size)
    fro = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    res = ''
    for i in range(size):
        lol = randint(0, len(fro))
        res += fro[lol%len(fro)]
    return res
def Server_Ent():
    conf.conf['isRunning'] = True
    app.run(host= '127.0.0.1',port = 10101)

@app.after_request
def lol(f):
    get_conf()
    dat = None
    try:
        dat = g.dat
    except Exception as e:
        pass
    if dat is None:
        return f
    if dat['Protocol'] == 'SendTranzh':
        SendTranzh_R(dat)
    elif dat['Protocol'] == 'SendTONODA':
        SendTONODA_R(dat)
    elif dat['Protocol'] == 'ResTranzh':
        ResTranzh_R(dat)
    elif dat['Protocol'] == 'CreateAccountS':
        CreateAccountS_R(dat)
    elif dat['Protocol'] == 'ConACC':
        ConACC_R(dat)
    elif dat['Protocol'] == 'ANConACC':
        ANConACC_R(dat)
    elif dat['Protocol'] == 'Activate':
        Activate_R(dat)
    elif dat['Protocol'] == 'DelIP':
        DelIP_R(dat)
    elif dat['Protocol'] == 'NewIP':
        NewIP_R(dat)
    elif dat['Protocol'] == 'DisActivate':
        DisActivate_R(dat)
    elif dat['Protocol'] == 'ChangeVoiting':
        ChangeVoiting_R(dat)
    elif dat['Protocol'] == 'VoteFor':
        VoteFor_R(dat)
    elif dat['Protocol'] == 'UpDate':
        UpDate_R(dat)
    elif dat['Protocol'] == 'SendOrder':
        SendOrder_R(dat)
    elif dat['Protocol'] == 'AddWallet':
        AddWallet_R(dat)
    elif dat['Protocol'] == 'CancelOrder':
        CancelOrder_R(dat)
    elif dat['Protocol'] == 'NewSUPERIP':
        NewSUPERIP_R(dat)
    elif dat['Protocol'] == 'DelSUPERIP':
        DelSUPERIP_R(dat)
    elif dat['Protocol'] == 'AddWalletOUT':
        AddWalletOUT_R(dat)

    return f

@app.route("/",methods = ['GET'])
def lol():
    return 'Hello World' + str(time_time())

@app.route("/",methods = ['POST'])
def Server_Proc():
    g.dat = dat = json.loads(request.data.decode())
    get_conf()
    res = None
    if dat is None:
        return jsonify(res)

    print(dat['Protocol'])
    if dat['Protocol'] == 'Registr':
        Registr_R(dat)#
    elif dat['Protocol'] == 'getAOrder':
        res = getAOrder_R(dat)#
    elif dat['Protocol'] == 'getHOrder':
        res = getHOrder_R(dat)#
    elif dat['Protocol'] == 'get_User':
        res = get_User_R(dat)#
    elif dat['Protocol'] == 'GetUnUsedAddress':
        res = GetUnUsedAddress_R(dat)#
    elif dat['Protocol'] == 'Login':
        res = Login_R(dat)#
    elif dat['Protocol'] == 'get_UserOF':
        res = get_UserOF_R(dat)#
    elif dat['Protocol'] == 'IsServer':
        res = IsServer_R(dat)#
    elif dat['Protocol'] == 'UpdateVoiting':
        res = UpdateVoiting_R(dat)
    elif dat['Protocol'] == 'GetConf':
        res = GetConf_R(dat)#
    elif dat['Protocol'] == 'GetUpDate':
        res = GetUpDate_R(dat)#
    elif dat['Protocol'] == 'CheckVer':
        res = CheckVer_R(dat)
    elif dat['Protocol'] == 'GetAllData':
        res = GetAllData_R(dat)#
    elif dat['Protocol'] == 'RegistrOUT':
        res = RegistrOUT_R(dat)
    elif dat['Protocol'] == 'get_Order':
        res = get_Order_R(dat)#
    elif dat['Protocol'] == 'getBalanceOUT':
        res = getBalanceOUT_R(dat)
    elif dat['Protocol'] == 'SendOUT_P':
        res = SendOUT_P_R(dat)
    elif dat['Protocol'] == 'GetDataToSendOUT':
        res = GetDataToSendOUT_R(dat)
    elif dat['Protocol'] == 'getBalance':
        res = getBalance_R(dat)#
    elif dat['Protocol'] == 'getATran':
        res = getATran_R(dat)#
    elif dat['Protocol'] == 'getHTran':
        res = getHTran_R(dat)#
    elif dat['Protocol'] == 'GetPricesF':
        res = GetPricesF_R(dat)#
    elif dat['Protocol'] == 'getDataForGraf':
        res = getDataForGraf_R(dat)#
    return jsonify(res)
def Send_T1(dat,OUT = False,func = None): # Send to all
    if OUT == False:
        for ip in conf.conf['Connected']:
            try:
                res = requests_post(f'http://{str(ip)}/', json = dat)
                res = res.json()
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass
    else:
        for ip in conf.conf['SUPERIP']:
            try:
                res = requests_post(f'http://{str(ip)}/', json = dat)
                res = res.json()
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass

def End(tor = True):
    if conf.conf['isRunning']:
        CloseNODA()
def Start():
    if conf.conf['isRunning']:
        BecomNODA()

#done
def DeleteIP():
    if conf.conf['MyIP'] != None and conf.conf['MyIP'] in conf.conf['Connected']:
        DelIP(conf.conf['MyIP'])
def AddMyIP():
    if conf.conf['MyIP'] == None:
        x = ngrok.connect(10101)
        conf.conf['MyIP'] = (str(x)[7:])
        # print('lol',str(x)[7:])
        NewIP(conf.conf['MyIP'])
    elif conf.conf['MyIP'] not in conf.conf['Connected']:
        NewIP(conf.conf['MyIP'])
def DeleteSUPERIP():
    if conf.conf['MyIP'] != None and conf.conf['MyIP'] in conf.conf['SUPERIP']:
        DelSUPERIP(conf.conf['MyIP'])
def AddMySUPERIP():
    if conf.conf['MyIP'] == None:
        x = ngrok.connect(10101)
        conf.conf['MyIP'] = (str(x)[7:])
        NewSUPERIP(conf.conf['MyIP'])
    elif conf.conf['MyIP'] not in conf.conf['SUPERIP']:
        NewSUPERIP(conf.conf['MyIP'])

#done
def BecomNODA():
    if get_User(get_UserOF(conf.conf['login'])['Balance'] ['SKR'][0][0], 'SKR')['Freez']>= 1000:

        variable = Thread(target = Server_Ent, args = ())
        variable.start()

        ip = ''

        # sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # host_ip = str(socket.gethostbyname(socket.gethostname()))
        GetAllData()
        GetConf()
        AddMyIP()
        conf.conf['isRunning'] = True
        conf.conf['isServer'] = True
        Activate(conf.conf['login'])
#done
def CloseNODA():
    DeleteIP()
    DisActivate(conf.conf['login'])
    conf.conf['isRunning'] = False
#done
def LogOut():
    conf.conf['login']          = ''
    conf.conf['passw']          = ''
    conf.conf['PrivKey']      = ''
    conf.conf['PubKey']      = ''
    conf.conf['In']          = False
def RegistrNewWallet(Wallet):
    if conf.conf['In']:
        PrivKey = GetUnUsedAddress(Wallet)
        # print ('lll', PrivKey)
        PubKey = PrivToPub(PrivKey)
        Registr(PubKey, Wallet, conf.conf['login'])
        PrivKey = decode(PrivKey, 16)
        PrivKey = (PubCode(PrivKey, conf.conf['PubKey'] ))
        time_sleep(0.5)
        ConACC(conf.conf['login'], Wallet, PubToAdr(PubKey), PrivKey)
        return encode(PrivKey, 16)

def SendOUT(Wal, Address, AddressTo, Sum):#Using our Address system and external Address To
    if conf.conf['In']:
        kek = get_UserOF(conf.conf['login'])['Balance'] [Wal]
        lol = None
        i = 0
        while i < len(kek):
            if kek[i][0]== Address:
                lol = kek[i][1]
                break
        if(lol== None):
            return
        kke = get_User(Address, Wal)
        BOut = getBalanceOUT(Wal, kke['AddressFrom'] )
        x = min(float(BOut), Sum)

        lol = PrivCode(lol, conf.conf['PrivKey'])
        lol = encode(lol, 16)
        SendOUT_P(kke['AddressFrom'] , AddressTo, PrivCode(decode(kke['AddressFrom'] + AddressTo + str(x) + Wal, 256), lol), x, Wal)

        Sum -= x
        if Sum<=0:
            return
            # lol = decode(lol, 16)

        dat = GetDataToSendOUT(Sum, Wal)
        i = 0
        while i < len(dat):
            dat[i][0] = kke['PubKey']
            dat[i][4] = lol
            i += 1

        SendTranzh(Tranzhs.Create(PreSendTranzh(dat), AddressTo, PrivCode(decode(kke['AddressFrom'] + AddressTo + str(Sum) + Wal, 256), lol) ))

#
def CheckVer():
    if Send_T1(CheckVer_S()) != conf.conf['Version']:
        GetUpDate()
def CheckVer_S():

    return {'Protocol':'CheckVer'}
def CheckVer_R(dat):

    return conf.conf['Version']
#done
def GetUpDate():
    #Here if you use it your programm is like new virsion
    def function(Data):
        Pass = Data['Pass']
        dat = Data['Data']
        if sha256_16(dat) == encode(PubCode(int(Pass),conf.conf['Key']),16):
            return Data
        return None
    dat = Send_T1(GetUpDate_S(),func = function)
    Pass = dat['Pass']
    dat = dat['Data']

    for x in dat['dirs']:
        if not os.path.exists(x):
            os.mkdir(x)
    with open('VerPass.skr', 'w') as f:
        f.write(str(Pass))
    for x in dat['files']:
        print (x)
        with open(x, 'wb') as f:
            f.write(b64decode(bytes(dat['files'][x]),'utf-8'))
    UpDate()
def GetUpDate_S():

    return {'Protocol':'GetUpDate'}
def GetUpDate_R(dat):
    dat = {'dirs':[],'files':{}}
    def indir(dirs):
        dat['dirs'].append(dirs)
        for file in os.listdir(dirs):
            if os.path.isfile(dirs+'//'+file):
                with open(dirs+'//'+file, 'rb') as input:
                    if file  != '.DS_Store' and file != 'exmp1.db':
                        dat['files'][dirs+'//'+file] = str(b64encode(input.read()), 'utf-8',errors='ignore').strip()
            elif file != '__pycache__':
                indir(dirs+'//'+file)
    indir('Sakaar')
    indir('web')
    with open('QRCode.py', 'rb') as input:
        dat['files']['QRCode.py'] = str(b64encode(input.read()), 'utf-8',errors='ignore').strip()
    Pass = None
    with open('VerPass.skr', 'r') as f:
        Pass = int(f.read())
        #     indir(file)
    # print(dat)
    return {'Data':dat,'Pass': Pass}

def UpDate(Ver):
    Send_T1(UpDate_S(Ver))
def UpDate_S(Ver):

    return {'Protocol':'UpDate','Version':Ver}
def UpDate_R(dat):
    if dat['Version'] != conf.conf['Version']:
        GetUpDate()
        UpDate(dat['Version'])
        sys.exit(82)
        # ReBorn()
#done
def GetConf():
    dat = Send_T1(GetConf_S())
    dat = dat['Data']
    conf.conf['Version'] = dat[0]
    conf.conf['Connected'] = dat[1]
    conf.conf['SUPERIP'] = dat[2]
    conf.conf['OurWallets'] = dat[3]
    conf.conf['OtherWallets'] = dat[4]
    conf.conf['InMemory'] = dat[5]
    conf.conf['FullFreez'] = dat[6]
    conf.conf['Block'] = dat[7]
    conf.conf['Comis'] = dat[8]
    conf.conf['Voiting'] = dat[9]
    conf.conf['Voited'] = dat[10]
def GetConf_S():

    return {'Protocol':'GetConf'}
def GetConf_R(dat):
    return {"Data":[
        conf.conf['Version'],
        conf.conf['Connected'],
        conf.conf['SUPERIP'],
        conf.conf['OurWallets'],
        conf.conf['OtherWallets'],
        conf.conf['InMemory'],
        conf.conf['FullFreez'],
        conf.conf['Block'],
        conf.conf['Comis'],
        conf.conf['Voiting'],
        conf.conf['Voited']
    ]}




def VoteFor(key,Address = None,Pass = None):
    if Pass == None and conf.conf['In']:
        Address = conf.conf['login']
        Pass = PrivCode(decode(key,256),conf.conf['PrivKey'])
    elif not conf.conf['In']:
        return
    if conf.conf['isServer']:
        kke = get_UserOF(Address)
        if not User.Check(kke,key,Pass):
            print('Error')
            return
        kke = get_User(kke['Balance'] ['SKR'][0][0], 'SKR')
        if kke['Freez'] < 1000 or Address in conf.conf['Voited'] :
            print('Error1')
            return
        x = conf.conf['Voited']
        x[Address] = key
        conf.conf['Voited'] = x
        del x
        x = conf.conf['Voiting']
        x[key][0] += kke['Freez']
        conf.conf['Voiting'] = x
        print(conf.conf['Voiting'][key][0])

        del x
    Send_T1(VoteFor_S(Address, key, Pass))
def VoteFor_S(Address,key,Pass):

    return {'Protocol':'VoteFor','Address':Address,'key':key,'Pass':Pass}
def VoteFor_R(dat):

    VoteFor(dat['key'] ,dat['Address'] ,dat['Pass'])
#done
def ChangeVoiting(new):
    if conf.conf['Voiting'] != new:
        conf.conf['Voited'] = {}
        conf.conf['Voiting'] = new
    else:
        return
    Send_T1(ChangeVoiting_S(new))
def ChangeVoiting_S(new):

    return {'Protocol':'ChangeVoiting','new':new}
def ChangeVoiting_R(dat):

    ChangeVoiting(dat['new'])
#done
def UpdateVoiting():
    conf.conf['Voiting'] = Send_T1(GetVoiting_S())
    return
def UpdateVoiting_S():

    return {'Protocol':'UpdateVoiting'}
def UpdateVoiting_R(dat):

    return conf.conf['Voiting']
#done
def GetAllData():
    dat = Send_T1(GetAllData_S())
    for x in dat:
        print (x)
        with open(x, 'wb') as f:
            f.write(b64decode(bytes(dat[x],'utf-8')))
def GetAllData_S():

    return {'Protocol':'GetAllData'}
def GetAllData_R(dat):
    dat = {}
    with open('Sakaar/exmp1.db', 'rb') as input:
        print ('Sakaar/exmp1.db')
        dat['Sakaar/exmp1.db'] = str(b64encode(input.read()), 'utf-8',errors='ignore').strip()
    # print(dat)
    return dat


# def MakeOrder(Wal1, Sum1, Wal2, Sum2):
#     if conf.conf['In']:

#         Stk = Order(conf.conf['login'], Wal1, Sum1, Wal2, Sum2, conf.conf['passw'], time_time())
#         Send_T1(SendOrder_S(Stk))





#done
def CancelOrder(stk,Pass = None):
    if Pass == None and conf.conf['In'] and conf.conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo']:
        Pass = PrivCode(decode(str(stk),256),conf.conf['PrivKey'])
        SendTranzh(Tranzhs.Create(PreSendTranzh([[PrivToPub(stk['priv']), AdrToPub(get_UserOF(conf.conf['login'])['Balance'] [stk['Wallet1']][0][0]), stk['Wallet1'], stk['Sum1'], stk['priv'], '']])))
    elif Pass == None and not (conf.conf['In'] and conf.conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo']):
        return
    if conf.conf['isServer']:
        if not User.Check(get_UserOF(get_User(stk['Address1'],stk['Wallet1'])['AddressTo']),str(stk),Pass):
            return
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        x = c.execute(f'''SELECT * From Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}'  AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''').fetchall()
        if len(x) == 0:
            conn.close()
            return
        stk = Order.FromSQL(x[0])
        c.execute(f'''DELETE FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
        conn.commit()
        c.execute(f'''UPDATE {stk['Wallet1']} SET FuncH = '',Func = '' WHERE Address = '{stk['Address1']}' ''')
        conn.commit()
        conn.close()
    Send_T1(CancelOrder_S(stk,Pass))
def CancelOrder_S(stk,Pass):

    return {'Protocol':'CancelOrder','Stk':stk,'Pass':Pass}
def CancelOrder_R(dat):

    CancelOrder(dat['Stk'],dat['Pass'])
#done
def MakeOrder(Adr1, Wal1, Sum1, Adr2, Wal2, k):
    if conf.conf['In']:
        # print ('MakeOrder')

        Priv = None
        usr1 = get_UserOF(conf.conf['login'])
        for pop in usr1['Balance'] [Wal1]:
            if(pop[0]== Adr1):
                Priv = encode(PrivCode(pop[1], conf.conf['PrivKey']), 16)
        if Priv== None :
            return

        def COOL(TS):
            res = 1
            mas = {}
            tor = 0
            stk = None
            for T in TS:
                if not T['Wal'] in mas:
                    mas[T['Wal']] = {}
                if not T['PubKey1'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey1'] ] = get_User(PubToAdr(T['PubKey1'] ), T['Wal'])
                    if mas[T['Wal']][T['PubKey1'] ]['Func'] != '':
                        if(tor== 1):
                            res = 0
                            break
                        tor = 1
                        stk = User.getFunc(mas[T['Wal']][T['PubKey1']])
                if not T['PubKey2'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey2'] ] = get_User(PubToAdr(T['PubKey2'] ), T['Wal'])
                res &= Checker(T, mas[T['Wal']][T['PubKey1'] ], mas[T['Wal']][T['PubKey2'] ])
                mas[T['Wal']][T['PubKey1'] ]['Balance'] -= T['Sum']
                if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
                else:
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
                mas[T['Wal']][T['PubKey1'] ]['Hash'] = T['Hash1']
                mas[T['Wal']][T['PubKey2'] ]['Hash'] = T['Hash2']
            res = res and (tor != 1 or Func(mas, TS, stk))
            print(res ,(tor != 1 or Func(mas, TS, stk)))
            return res

        dat = get_Order(Wal2,Wal1,1/k)
        # print (dat)
        for row in dat:

            row = Order.FromSQL(row)

            usr02 = get_User(row['Address1'], Wal2)

            t = time_time()

            # print (stk2.Adr1 + " " + Adr1)
            SUM1 = min (Sum1, usr02['Balance'] /k)
            SUM2 = min (Sum1*k, usr02['Balance'] )
            # print ('OLOLO', row, Adr2)
            # print('SUMM', SUM1, SUM2)

            TS = [[PrivToPub(row['priv']), AdrToPub(Adr2), Wal2, SUM2, row['priv'], ''], [AdrToPub(Adr1), AdrToPub(row['Address2']), Wal1, SUM1, Priv, '']]
            TS = PreSendTranzh(TS)
            print ('NOOOOO', COOL(TS))
            if COOL(TS):
                Sum1 -= SUM1
                SendTranzh(Tranzhs.Create(TS))

        # print (Sum1)
        if(Sum1 > 0):

            PrivKey = GetUnUsedAddress(Wal1)
            PubKey = PrivToPub(PrivKey)

            # print ('lll', PrivKey, PubKey)
            t = time_time()

            Stk = Order.FromSQL((PubToAdr(PubKey), Adr2, conf.conf['login'], Wal1, Wal2, Sum1, Sum1, k, t, t, PrivKey))
            x = User.CodeFunc(Stk, conf.conf['PrivKey'])
            Registr(PubKey, Wal1, conf.conf['login'], x[0], x[1])
            PrivKey = decode(PrivKey, 16)
            PrivKey = (PubCode(PrivKey, conf.conf['PubKey'] ))
            time_sleep(0.5)
            ConACC(conf.conf['login'], Wal1, PubToAdr(PubKey), PrivKey)
            # print (AdrToPub(Adr1)== PubKey)
            # print ('Priv :',Priv)
            TS = [[AdrToPub(Adr1), PubKey, Wal1, Sum1, Priv, '']]
            SendTranzh(Tranzhs.Create(PreSendTranzh(TS)))
            time_sleep(3)
            # print (get_User(PubToAdr(PubKey), Wal1)['Balance'] )
            # print
            Send_T1(SendOrder_S(Stk))
#done
def Func(mas, TS, stk):
    lol = len(TS)== 1 and mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['AddressTo']== mas[TS[0]['Wal']][TS[0]['PubKey2'] ]['AddressTo']
    # print (len(TS)== 2, mas[TS[0]['PubKey1'] ]['AddressTo'], mas[TS[1]['PubKey2'] ]['AddressTo'], stk, stk['Wallet1']== TS[0]['Wal'], stk['Wallet2']== TS[1]['Wal'], TS[0]['Sum'] / TS[1]['Sum']== stk['k'], mas[TS[0]['PubKey1'] ]['Address']== stk['Address1'])
    pop = len(TS)== 2 and mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['AddressTo']== mas[TS[1]['Wal']][TS[1]['PubKey2'] ]['AddressTo'] and stk['Wallet1']== TS[0]['Wal'] and stk['Wallet2']== TS[1]['Wal'] and TS[0]['Sum'] / TS[1]['Sum']== stk['k'] and mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['Address']== stk['Address1']
    return lol or pop
def chOrder(a, b):
    [x['Address1'], x['Address2'], x['SumS'], x['k'], x['t'], x['priv']]
    return (a.Adr1== b.Adr1) and (a.Adr2== b.Adr2) and (a.t== b.t) and (a.Wal1== b.Wal1) and (a.Wal2== b.Wal2) and (a.k== b.k)
def SendOrder(stk):
    if conf.conf['isServer']:
        if stk['Sum1']<=0 or stk['k']<=0:
            return

        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT * FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
        if not(c.fetchone() is None):
            conn.close()
            return
        conn.close()
        Order.Create(stk['Address1'], stk['Wallet1'], stk['AddressFrom'], stk['Sum1'], stk['Address2'], stk['Wallet2'], stk['k'], stk['t'], stk['priv'])
    Send_T1(SendOrder_S(stk))
def SendOrder_S(Stk):

    return {'Protocol':'SendOrder','Stk':Stk}
def SendOrder_R(dat):

    SendOrder(dat['Stk'])
#done
def get_Order(Wallet1,Wallet2,k = 0):
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        if k != 0:
            dat = c.execute(f'''SELECT * FROM Orders WHERE Wallet1 = '{Wallet1}' AND Wallet2 = '{Wallet2}' AND k = {k} AND Sum1 > 0''').fetchall()
        else:
            dat = c.execute(f'''SELECT * FROM Orders WHERE Wallet1 = '{Wallet1}' AND Wallet2 = '{Wallet2}' AND Sum1 > 0''').fetchall()
        conn.close()
        return dat
    return Send_T1(get_Order_S(Wallet1,Wallet2,k))
def get_Order_S(Wallet1,Wallet2,k):

    return {'Protocol':'get_Order','Wallet1':Wallet1,'Wallet2':Wallet2,'k':k}
def get_Order_R(dat):
    # print('get_Order')
    return get_Order(dat['Wallet1'],dat['Wallet2'],dat['k'])






#done
def ANConACC(Login, Wallet, AddressTo, Pass = None):
    if Pass == None:
        if conf.conf['In'] and conf.conf['login'] == Login:
            Pass = PrivCode(decode(str(Login) + str(Wallet) + str(AddressTo),256),conf.conf['PrivKey'])
        else:
            return
    if conf.conf['isServer']:
        kke = get_UserOF(Login)
        if User.Check(kke,str(Login) + str(Wallet) + str(AddressTo),Pass):
            conn = sql3connect('Sakaar/exmp1.db')
            c = conn.cursor()
            c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Login}' ''')
            tor = not(c.fetchone() is None)
            c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{AddressTo}' AND AddressTo = '{Login}' ''')
            if not(c.fetchone() is None) and tor:
                kke = kke['Balance']
                lol = None
                for arc in kke[Wallet]:
                    if arc[0] == AddressTo:
                        lol = arc
                        break
                if lol != None:
                    kke[Wallet].remove(lol)
                    c.execute(f'''UPDATE UserOF SET Balance = '{json.dumps(kke)}' WHERE Address = '{Login}' ''')
                    conn.commit()
                    c.execute(f'''UPDATE {Wallet} SET AddressTo = '',FuncH = '',Func = '' WHERE Address = '{AddressTo}' AND AddressTo = '{Login}' ''')
                    conn.commit()
                else:
                    return

                # print ('ANConACC OK')
                conn.close()
            else:
                conn.close()
                return
        else:
            return
    Send_T1(ANConACC_S(Login, Wallet, AddressTo,Pass))
def ANConACC_S(Login, Wallet, AddressTo,Pass):

    return {'Protocol':'ANConACC','Address':Login,'Wallet':Wallet,'AddressTo':AddressTo,'Pass':Pass}
def ANConACC_R(dat):

    ANConACC(dat['Address'], dat['Wallet'], dat['AddressTo'], dat['Pass'])
#done
def Login(login, Password):
    if not conf.conf['In']:
        res = get_UserOF(login)['PubKey']
        if res == PrivToPub(sha256_16(sha256_16(login + sha256_16(Password)))):
            conf.conf['login']          = login
            conf.conf['passw']          = sha256_16(Password)
            conf.conf['PrivKey']      = sha256_16(sha256_16(login + sha256_16(Password)))
            conf.conf['PubKey']      = PrivToPub(conf.conf['PrivKey'])
            conf.conf['In']          = True
            print ('LogIN')
            if IsServer(conf.conf['login']):
                print('Active')

#done
def CreateAccountS(Login, Hash):
    if conf.conf['isServer'] :
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Login}' ''')
        if not(c.fetchone() is None):
            conn.close()
            return
        conn.close()
        UserOF.Create(Login, Hash)
        # print kke['Balance']
    Send_T1(CreateAccountS_S(Login, Hash))
def CreateAccountS_S(Login, Hash):

    return {'Protocol':'CreateAccountS','Login':Login,'Hash':Hash}
def CreateAccountS_R(dat):

    CreateAccountS(dat['Login'], dat['Hash'])
#done
def CreateAccount(Login, Password):

    CreateAccountS(Login, PrivToPub(sha256_16(sha256_16(Login + sha256_16(Password)))))
#done
def get_UserOF(Address):
    if conf.conf['isServer']:
        kke = None
        Address = str(Address)
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Address}' ''')
        if not(c.fetchone() is None):
            kke = UserOF.FromSQL(c.execute(f'''SELECT * FROM UserOF WHERE Address = '{Address}' ''').fetchall()[0])
            conn.commit()
        conn.close()
        return kke
    return Send_T1(get_UserOF_S(Address))
def get_UserOF_S(Address):

    return {'Protocol':'get_UserOF','Address':Address}
def get_UserOF_R(dat):

    return get_UserOF(dat['Address'])
#done
def IsServer(Address):
    if conf.conf['isServer']:
        return get_UserOF(Address)['Active']
    return Send_T1(IsServer_S(Address))
def IsServer_S(Address):

    return {'Protocol':'IsServer','Address':Address}
def IsServer_R(dat):

    return IsServer(dat['Address'])
#done
def AddWallet(Wallet):
    if Wallet in conf.conf['OurWallets']:
        return
    x = conf.conf['OurWallets']
    x.append(Wallet)
    conf.conf['OurWallets'] = x
    del x
    conn = sql3connect('Sakaar/exmp1.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
            Address         varchar(128)     NOT NULL,
            AddressTo         varchar(128) ,
            PubKey             varchar(128)     NOT NULL,
            FuncH             varchar(128) ,
            Func             varchar(128) ,
            Time            Double    ,
            Freez            Double            NOT NULL,
            Balance            Double            NOT NULL,
            Hash            varchar(128)    NOT NULL,
            AddressFrom        varchar(128),
            Wallet             varchar(16)     NOT NULL
            ); ''')
    conn.commit()
    conn.close()
    Send_T1(AddWallet_S(Wallet))
def AddWallet_S(Wallet):

    return {'Protocol':'AddWallet','Wallet':Wallet}
def AddWallet_R(dat):

    AddWallet(dat['Wallet'])
#done
def ConACC(Address, Wallet, AddressTo, PrivKey):
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Address}' ''')
        tor = not(c.fetchone() is None)
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{AddressTo}' ''')
        if not(c.fetchone() is None) and tor:
            kke = get_UserOF(Address)['Balance']
            if not Wallet in kke :
                kke[Wallet] = []
            lol = [AddressTo, PrivKey]
            if Wallet in conf.conf['OtherWallets']:
                lol.append(get_User(AddressTo,Wallet)['AddressFrom'])
            if lol in kke[Wallet]:
                return
            kke[Wallet].append(lol)
            c.execute(f'''UPDATE UserOF SET Balance = '{json.dumps(kke)}' WHERE Address = '{Address}' ''')
            conn.commit()

            print ('ConACC OK')
            conn.close()
        else:
            print ('ConACC ERRROR',tor,not(c.fetchone() is None))
            conn.close()
            return
    Send_T1(ConACC_S(Address, Wallet, AddressTo, PrivKey))
def ConACC_S(Address, Wallet, AddressTo, PrivKey):

    return {'Protocol':'ConACC','Address':Address,'Wallet':Wallet,'AddressTo':AddressTo,'PrivKey':PrivKey}
def ConACC_R(dat):

    ConACC(dat['Address'], dat['Wallet'], dat['AddressTo'], dat['PrivKey'])
#done
def DelIP(ip):
    if not ip in conf.conf['Connected']:
        return
    x = conf.conf['Connected']
    x.remove(ip)
    conf.conf['Connected'] = x
    del x
    Send_T1(DelIP_S(ip))
def DelIP_S(ip):

    return {'Protocol':'DelIP','IP':ip}
def DelIP_R(dat):

    DelIP(dat['IP'])
#done
def NewIP(ip):
    if ip in conf.conf['Connected']:
        return
    x = conf.conf['Connected']
    x.append(ip)
    conf.conf['Connected'] = x
    print(x)
    del x
    Send_T1(NewIP_S(ip))
def NewIP_S(ip):

    return {'Protocol':'NewIP','IP':ip}
def NewIP_R(dat):

    NewIP(dat['IP'])

def SaveTranzhs(Tranzh):
    mas = {}
    res = 1
    tor = 0
    stk = None
    for T in Tranzh['TS']:
        if not T['Wal'] in mas:
            mas[T['Wal']] = {}
        if not T['PubKey1'] in mas[T['Wal']]:
            mas[T['Wal']][T['PubKey1'] ] = get_User(PubToAdr(T['PubKey1'] ), T['Wal'])
            if mas[T['Wal']][T['PubKey1'] ]['Func'] != '':
                if(tor== 1):
                    res = 0
                    break
                tor = 1
                stk = User.getFunc(mas[T['Wal']][T['PubKey1'] ])
        if not T['PubKey2'] in mas[T['Wal']]:
            mas[T['Wal']][T['PubKey2'] ] = get_User(PubToAdr(T['PubKey2'] ), T['Wal'])
        res &= Checker(T, mas[T['Wal']][T['PubKey1'] ], mas[T['Wal']][T['PubKey2'] ])

        mas[T['Wal']][T['PubKey1'] ]['Hash']      = T['Hash1']
        mas[T['Wal']][T['PubKey1'] ]['Balance'] -= T['Sum']

        # TranzhHistory(T)

        mas[T['Wal']][T['PubKey2'] ]['Hash']      = T['Hash2']
        if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
            mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
        else:
            mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
    res = res and (tor != 1 or Func(mas, Tranzh['TS'], stk))
    conn = sql3connect('Sakaar/exmp1.db')
    c = conn.cursor()
    T2 = None
    if Tranzh['AddressTo'] != None and conf.conf['isSUPER']:
        T2 = Tranzh.Create(AdrToPub(k['AddressTo'] ), 'out/' + AddressTo, Wal, Sum, sha256_16(kek['Hash'] + Pass), '', Pass, time_time(), MesIn = '', MesOut = '')
    conf.conf['Block'] += 1
    for T in Tranzh['TS']:
        if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
            continue
        if Tranzh['AddressTo'] != None and conf.conf['isSUPER']:
            AddressFrom = get_User(PubToAdr(T['PubKey2'] ), T['Wal'])['AddressFrom']
            T2 = Tranzh.Create(T['PubKey1'] , 'out/' + AddressTo, T['Wal'], T['Sum']*(1-T['Comis']), sha256_16(kek['Hash'] + Pass), T['PubKey2'] , '', time_time(), MesIn = '', MesOut = '')
            # TranzhHistoryP(PubToAdr(T['PubKey2'] ), T2['Wal'], T2)
            # TranzhHistory(T2)
            SendOUT_P1(AddressFrom, Tranzh['AddressTo'] , T['Sum']*(1-T['Comis']), T['Wal'])

        ARRR = []
        T['Comision'] = []
        SumCom = T['Sum'] * T['Comis']
        for row in c.execute(f'''SELECT * FROM SKR WHERE Freez >= 1000 '''):
            kke = User.FromSQL(row)
            looop = kke['Freez']
            if looop>=1000 and len(kke['AddressTo'] ) > 0 and not kke['AddressTo'] in ARRR:
                kke = get_UserOF(kke['AddressTo'] )
                if not kke['Active']:
                    continue
                if T['Wal'] in kke['Balance'] :
                    Adr = AdrToPub(kke['Balance'] [T['Wal']][0][0])
                    if not Adr in mas[T['Wal']]:
                        mas[T['Wal']][Adr] = get_User(kke['Balance'] [T['Wal']][0][0], T['Wal'])
                    popp = looop /conf.conf['FullFreez'] * SumCom

                    Pass = str(T['PubKey1'] ) + str(T['PubKey2'] ) + T['Wal'] + str(T['Sum']) + T['Hash1'] + T['Hash2'] + str(T['time'])
                    Pass = sha256_16(Pass)
                    # T.NODA( AdrToPub(kke['Address'] ), sha256_16( kke['Hash'] + Pass), (looop /conf.conf['FullFreez']))
                    mas[T['Wal']][Adr]['Balance'] += popp
                    T['Comision'].append([mas[T['Wal']][Adr]['Address'], popp])
                    mas[T['Wal']][Adr]['Hash'] = sha256_16(mas[T['Wal']][Adr]['Hash'] + Pass)
                    ARRR.append(kke['Address'])
        c.execute(f'''INSERT INTO History VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (conf.conf['Block'], T['PubKey1'], T['PubKey2'], T['Sum'], T['Comis'], T['Wal'], T['time'], mas[T['Wal']][T['PubKey1']]['AddressTo'], json.dumps(T['Comis']),json.dumps(T['MesIn']),json.dumps(T['MesOut'])))
        conn.commit()
    for wal in mas:
        for name in mas[wal]:
            name = mas[wal][name]
            c.execute(f'''UPDATE {name['Wallet']} SET Balance = {str(name['Balance'])}, Hash = '{encode(decode(name['Hash'], 256), 16)}' WHERE Address = '{name['Address']}' ''')
            conn.commit()

    if stk and res and tor and len(Tranzh['TS']) == 2:
        usr1 = get_UserOF(mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1'] ]['AddressTo'] )
        for row in c.execute(f'''SELECT * FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' '''):
            row = Order.FromSQL(row)
            if(row['t1'] < Tranzh['TS'][0]['time']):
                row['t1'] = Tranzh['TS'][0]['time']
                row['Sum1'] -= Tranzh['TS'][0]['Sum']
                if row['Sum1'] == 0:
                    c.execute(f'''DELETE FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
                    conn.commit()
                    c.execute(f'''UPDATE {stk['Wallet1']} SET FuncH = '',Func = '' WHERE Address = '{stk['Address1']}' ''')
                    conn.commit()
                else:
                    c.execute(f'''UPDATE Orders SET t1 = {row['t1']}, Sum1 = {row['Sum1']} WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
                    conn.commit()
                c.execute(f'''INSERT INTO Orders_H VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (stk['k'],row['t1'],stk['Wallet1'],stk['Wallet2'],conf.conf['Block'],mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1'] ]['AddressTo'],mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey2'] ]['AddressTo'], Tranzh['TS'][0]['Sum']))
                conn.commit()
                c.execute(f'''INSERT INTO Orders_H VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (1/stk['k'],row['t1'],stk['Wallet2'],stk['Wallet1'],conf.conf['Block'],mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey2'] ]['AddressTo'],mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1'] ]['AddressTo'], Tranzh['TS'][1]['Sum']))
                conn.commit()
            break
    conn.commit()
    c.close()
    conn.close()

def EndTranzh(Tranzh, res):
    print ('EndTranzh ' + str(res))

    if conf.conf['isServer']:
        tor = False
        print ("RES " + str(res))
        for arc in conf.conf['InMemory']:
            if Ch_Tranzh(Tranzh, arc):
                # x = conf.conf['InMemory']
                # x.remove(arc)
                # conf.conf['InMemory'] = x
                # del x
                tor = True
                break
        if tor :
            conn = sql3connect('Sakaar/exmp1.db')
            c = conn.cursor()
            for T in Tranzh['TS']:
                c.execute(f'''DELETE FROM ATran WHERE PubKey1 = '{T['PubKey1']}' AND PubKey2 = '{T['PubKey2']}' AND Wallet = '{T['Wal']}' AND Time = {T['time']} ''')
            conn.commit()
            conn.close()
        if (not tor) or (not res):
            return

        SaveTranzhs(Tranzh)
#done
def Activate(Address):
    if conf.conf['isServer']:
        print(IsServer(Address))
        if IsServer(Address):
            return
        kke = get_UserOF(Address)
        if not 'SKR' in kke['Balance'] :
            return
        if get_User(kke['Balance'] ['SKR'][0][0], 'SKR')['Freez'] < 1000:
            return
        kke['Active'] = True
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''UPDATE UserOF SET Active = true WHERE Address = '{kke['Address']}' ''')
        conn.commit()
        conn.close()
    Send_T1(Activate_S(Address))
def Activate_S(Address):

    return {'Protocol':'Activate','Address':Address}
def Activate_R(dat):

    Activate(dat['Address'])
#done
def DisActivate(Address):
    if conf.conf['isServer']:
        if 1 != IsServer(Address):
            return
        kke = get_UserOF(Address)
        kke['Active'] = False
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''UPDATE UserOF SET Active = false WHERE Address = '{kke['Address']}' ''')
        conn.commit()
        conn.close()
    Send_T1(DisActivate_S(Address))
def DisActivate_S(Address):

    return {'Protocol':'DisActivate','Address':Address}
def DisActivate_R(dat):

    DisActivate(dat['Address'])
#done
def ResTranzh(Address, Tranzh, res,Pass = None):
    if Pass == None and  Address == conf.conf['login'] and conf.conf['In']:
        Pass = PrivCode(decode(str(Tranzh) + str(res),256),conf.conf['PrivKey'])
    elif Pass == None and not (Address == conf.conf['LogIN'] and conf.conf['In']):
        return
    print ('ResTranzh ' + str(res > 0))
    lol = 0
    if conf.conf['isServer']:
        if not User.Check(get_UserOF(Address),str(Tranzh) + str(res),Pass):
            return
        kke = get_User(get_UserOF(Address)['Balance'] ['SKR'][0][0], 'SKR')
        tor = True
        i = 0
        for arc in conf.conf['InMemory']:
            if Ch_Tranzh(Tranzh, arc) and not Address in conf.conf['InMemory'][i]['Users']:
                x = conf.conf['InMemory']
                lol = kke['Freez'] / conf.conf['FullFreez']
                if res:
                    x[i]['resTO'] += lol
                else:
                    x[i]['resAnti'] += lol
                x[i]['Users'].append(Address)
                conf.conf['InMemory'] = x
                del x
                tor = False
                break
            i += 1
        if tor:
            return
    Send_T1(ResTranzh_S(Address, Tranzh, res,Pass))
    print('ResTranzh',conf.conf['isServer'] , Ch_Tranzh(Tranzh, conf.conf['InMemory'][i]))
    if conf.conf['isServer'] and Ch_Tranzh(Tranzh, conf.conf['InMemory'][i]):
        if conf.conf['InMemory'][i]['resTO'] >= 0.5 and res and conf.conf['InMemory'][i]['resTO']-lol < 0.5:
            EndTranzh(Tranzh, True)
        elif conf.conf['InMemory'][i]['resAnti'] > 0.5 and res and conf.conf['InMemory'][i]['resAnti']-lol <= 0.5 :
            EndTranzh(Tranzh, False)
def ResTranzh_S(Address, Tranzh, res,Pass):

    return {'Protocol':'ResTranzh','Address':Address,'Tranzh':Tranzhs.ToJSON(Tranzh),'res':res,'Pass':Pass}
def ResTranzh_R(dat):

    ResTranzh(dat['Address'], Tranzhs.FromJSON(dat['Tranzh']), dat['res'],dat['Pass'])

def Checker(T, kke1, kke2):
    Pass = sha256_16(str(T['PubKey1'] ) + str(T['PubKey2'] ) + T['Wal'] + str(T['Sum']) + kke1['Hash'] + kke2['Hash'] + str(T['time']))
    res1 = 1
    if(T['Wal'] in conf.conf['OurWallets']):
        # print(kke1['Balance'] - T['Sum']>=0) , (kke2['Balance']>=0)
        res1 = (kke1['Balance'] - T['Sum']>=0) and (kke2['Balance']>=0)
    elif(T['Wal'] in conf.conf['OtherWallets']):
        # print ('ERRROR')
        res1 = (kke1['Balance'] + float(getBalanceOUT(kke1['Wallet'].lower(), kke1['AddressFrom'] )) -T['Sum'])
    else:
        # print ('NOOOOOOOOO',T['Wal'], conf.conf['OurWallets'])
        res1 = 0
    tor = T['Comis']>=conf.conf['Comis'] and User.Check(kke1, Pass, T['Pass']) and sha256_16(kke1['Hash'] + Pass)== T['Hash1'] and sha256_16(kke2['Hash'] + Pass)== T['Hash2'] and T['Sum'] > 0
    print ('Checker', T['Comis']>=conf.conf['Comis'] , User.Check(kke1, Pass, T['Pass']) , sha256_16(kke1['Hash'] + Pass)== T['Hash1'] , sha256_16(kke2['Hash'] + Pass)== T['Hash2'] , T['Sum'] > 0,T['Sum'])
    print ('Checker', res1,tor)
    return tor and res1

def CheckerTranzh():
    i = 0
    while i < len(conf.conf['InMemory']):
        if (time_time() - conf.conf['InMemory'][i]['TS'][0]['time'] > 86400) and (conf.conf['InMemory'][i]['resTO'] >=0.5 or conf.conf['InMemory'][i]['resAnti']>0.5):
            x = conf.conf['InMemory']
            x.remove(x[i])
            conf.conf['InMemory'] = x
        # if not Ch_Tranzh(conf.conf['InMemory'][i], x):
        #     continue
        if not conf.conf['login'] in conf.conf['InMemory'][i]['Users']:
            res = 1
            mas = {}
            tor = 0
            stk = None
            SUM = 0
            Wal = conf.conf['InMemory'][i]['TS'][0]['Wal']
            OUT = conf.conf['InMemory'][i]['TS'][0]['PubKey1']
            for T in conf.conf['InMemory'][i]['TS']:
                SUM += T['Sum']
                if not T['Wal'] in mas:
                    mas[T['Wal']] = {}
                if not T['PubKey1'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey1'] ] = get_User(PubToAdr(T['PubKey1'] ), T['Wal'])
                    if mas[T['Wal']][T['PubKey1'] ]['Func'] != '':
                        if OUT != T['PubKey1'] :
                            OUT = None
                        if(tor== 1):
                            res = 0
                            break
                        tor = 1
                        stk = User.getFunc(mas[T['Wal']][T['PubKey1'] ])
                    # print ('T["PubKey1"] ' + T['PubKey1'] )
                if Wal != conf.conf['InMemory'][i]['TS'][0]['Wal']:
                    Wal = None
                if not T['PubKey2'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey2'] ] = get_User(PubToAdr(T['PubKey2'] ), T['Wal'])
                    # print ('T["PubKey2"] ' + T['PubKey2'] )
                res &= Checker(T, mas[T['Wal']][T['PubKey1'] ], mas[T['Wal']][T['PubKey2'] ])
                print(res)
                mas[T['Wal']][T['PubKey1'] ]['Balance'] -= T['Sum']
                if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
                else:
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
                mas[T['Wal']][T['PubKey1'] ]['Hash'] = T['Hash1']
                mas[T['Wal']][T['PubKey2'] ]['Hash'] = T['Hash2']
            if conf.conf['InMemory'][i]['AddressTo'] != None or conf.conf['InMemory'][i]['AddressHashed'] != None:
                if conf.conf['InMemory'][i]['AddressTo']== None or Wal== None or conf.conf['InMemory'][i]['AddressHashed']== None or OUT== None or not User.Check(mas[Wal][OUT], mas[Wal][OUT]['AddressFrom'] + conf.conf['InMemory'][i]['AddressTo'] + str(SUM) + Wal, conf.conf['InMemory'][i]['AddressHashed'] ):
                    print('ERRROR')
                    res = 0
            res = res and (tor != 1 or Func(mas, conf.conf['InMemory'][i]['TS'], stk))
            print (res,(tor != 1 or Func(mas, conf.conf['InMemory'][i]['TS'], stk)))
            ResTranzh(conf.conf['login'], conf.conf['InMemory'][i], res)
            return

        i += 1

def SendTONODA(Address, Sum, t = None, Pass = None):
    Sum = float(Sum)
    if Pass == None and conf.conf['In'] and conf.conf['login'] == Address:
        t = time_time()
        lol = get_UserOF(conf.conf['login'])['Balance'] ['SKR'][0][1]
        lol = PrivCode(lol, conf.conf['PrivKey'])
        lol = encode(lol, 16)
        Pass = decode(sha256_16(str(Sum) + str(t)), 256)
        Pass = PrivCode(Pass, lol)
    elif Pass == None and not (conf.conf['In'] and conf.conf['login'] == Address):
        return
    if Sum== 0:
        return
    if conf.conf['isServer']:
        kke = get_UserOF(Address)
        if not 'SKR' in kke['Balance'] :
            return
        kke = get_User(kke['Balance'] ['SKR'][0][0], 'SKR')
        if kke['Time']>=t:
            return
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        kke['Time'] = t

        c.execute(f'''UPDATE SKR SET Time = '{kke['Time']}' WHERE Address = '{kke['Address']}' ''')
        conn.commit()

        if Address in conf.conf['Voited'] :
            x = conf.conf['Voiting']
            x[conf.conf['Voited'][Address]][0] -= kke['Freez']
        # x = conf.conf['Voited']
        # x[Address] = key
        # conf.conf['Voited'] = x
        # del x
        # x = conf.conf['Voiting']
        # x[key][0] += kke['Freez']
        # conf.conf['Voiting'] = x
            conf.conf['Voiting'] = x
            x = conf.conf['Voited']
            del x[Address]
            conf.conf['Voited'] = x
            del x
        if Sum > 0:
            Sum = min(Sum, kke['Balance'] - kke['Freez'] )
            if Sum== 0:
                return

            kke['Freez']          += Sum
            conf.conf['FullFreez']      += Sum
        else:
            Sum = min(-1*Sum, kke['Freez'] )
            if Sum== 0:
                return

            kke['Freez']         -= Sum
            conf.conf['FullFreez']     -= Sum
        if(User.Check(kke, sha256_16(str(Sum) + str(t)), Pass)):
            c.execute(f'''UPDATE SKR SET Freez = '{kke['Freez']}' WHERE Address = '{kke['Address']}' ''')
            conn.commit()
        conn.close()
    Send_T1(SendTONODA_S(Address, Sum, t, Pass))
def SendTONODA_S(Address, Sum, time, Pass):

    return {'Protocol':'SendTONODA','Address':Address,'Sum':Sum,'Time':time,'Pass':Pass}
def SendTONODA_R(dat):

    SendTONODA(dat['Address'], dat['Sum'], dat['Time'], dat['Pass'])

#done
# [[PubKey1, PubKey2, Wal, Sum, PrivKey1, MesIn]]
def PreSendTranzh(lol):
    mas = {}
    res = 1
    TS      = []
    for T in lol:
        if not T[2] in mas:
            mas[T[2]] = {}
        if not T[0] in mas[T[2]]:
            mas[T[2]][T[0]] = get_User(PubToAdr(T[0]), T[2])
        if not T[1] in mas[T[2]]:
            mas[T[2]][T[1]] = get_User(PubToAdr(T[1]), T[2])
        t                      = time_time()
        if len(T)== 8:
            Comis = T[7]
        else:
            Comis = conf.conf['Comis']
        Pass                  = str(T[0]) + str(T[1]) + T[2] + str(T[3]) + mas[T[2]][T[0]]['Hash'] + mas[T[2]][T[1]]['Hash'] + str(t)
        Pass                  = sha256_16(Pass)
        T1                      = Tranzh.Create(T[0], T[1], T[2], T[3], sha256_16(mas[T[2]][T[0]]['Hash'] + Pass), sha256_16(mas[T[2]][T[1]]['Hash'] + Pass), Pass, t, PubCode(decode(T[5], 256), T[1]), PubCode(decode(T[5], 256), T[0]), Comis)
        T1['Pass']              = PrivCode(decode(T1['Pass'], 256), T[4])
        mas[T[2]][T[0]]['Balance']     -= T[3]

        if len(mas[T[2]][T[1]]['AddressTo'] ) > 0 and mas[T[2]][T[1]]['AddressTo']== mas[T[2]][T[0]]['AddressTo'] :
            mas[T[2]][T[1]]['Balance']      += T[3]
        else:
            mas[T[2]][T[1]]['Balance']      += T[3]*(1-Comis)
        mas[T[2]][T[0]]['Hash']          = T1['Hash1']
        mas[T[2]][T[1]]['Hash']          = T1['Hash2']
        TS.append(T1)
    return TS
    pass
#done
def Ch_Tranzh(a, b):
    res = len(a['TS'])== len(b['TS'])
    res &= json.dumps(a['TS']) == json.dumps(b['TS'])
    return res
#done
def SendTranzh(x):
    tor = 0
    if conf.conf['isServer']:
        for i in conf.conf['InMemory']:
            if Ch_Tranzh(i, x):
                return
        x1 = conf.conf['InMemory']
        x1.append(x)
        conf.conf['InMemory'] = x1
        del x1
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        for T in x['TS']:
            c.execute(f'''INSERT INTO ATran VALUES(?, ?, ?, ?, ?, ?, ?)''', (T['PubKey1'], T['PubKey2'], T['Sum'], T['Comis'], T['Wal'], T['time'], get_User(PubToAdr(T['PubKey1']),T['Wal'])['AddressTo']))
            conn.commit()
        conn.close()
        tor = 1
    Send_T1(SendTranzh_S(x))
    if tor & conf.conf['isServer']:
        CheckerTranzh()
        pass
def SendTranzh_S(x):

    return {'Protocol':'SendTranzh','Tranzh':x}
def SendTranzh_R(dat):

    SendTranzh(dat['Tranzh'])
#done
def GetUnUsedAddress(Wallet):
    if conf.conf['isServer']:
        while True:
            PrivKey = sha256_16(sha256_16(Generator(16)))
            conn = sql3connect('Sakaar/exmp1.db')
            c = conn.cursor()
            c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{PubToAdr(PrivToPub(PrivKey))}' ''')
            if (c.fetchone() is None):
                conn.close()
                return PrivKey
        return PrivKey
    else:
        PrivKey      = sha256_16(sha256_16(Generator(16)))
        while Send_T1(GetUnUsedAddress_S(PubToAdr(PrivToPub(PrivKey)), Wallet)) != '1':
            PrivKey = sha256_16(sha256_16(Generator(16)))
        return PrivKey
def GetUnUsedAddress_S(Address, Wallet):

    return {'Protocol':'GetUnUsedAddress','Wallet':Wallet,'Address':Address}
def GetUnUsedAddress_R(dat):
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM {dat['Wallet']} WHERE Address = '{dat['Address']}' ''')
        tor = ''
        if (c.fetchone() is None):
            tor = '1'
        else:
            tor = '0'
        conn.close()
        return tor
#done
def get_User(Address, Wallet):
    if conf.conf['isServer']:
        kke = None
        Address = str(Address)
        Wallet = str(Wallet)
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{Address}' ''')
        if not(c.fetchone() is None):
            kke = User.FromSQL(c.execute(f'''SELECT * FROM {Wallet} WHERE Address = '{Address}' ''').fetchall()[0])
            conn.commit()
            conn.close()
        else:
            conn.close()
            Registr(AdrToPub(Address), Wallet)
            time_sleep(1)
            kke = get_User(Address, Wallet)
        # if os.path.exists(conf.conf['Link'] + '//' + Wallet + '//' + Address + '.usr.h'):
        #     l = []
        #     for line in reversed(list(open(conf.conf['Link'] + '//' + Wallet + '//' + Address + '.usr.h'))):
        #         l = line.rstrip().split(' ')
        #         break
        #     PubKey = AdrToPub(Address)
        #     if len(l)== 8:
        #         if l[0]== PubKey:
        #             kke['Hash'] = l[4]
        #         elif l[1]== PubKey:
        #             kke['Hash'] = l[5]
        #     elif len(l)== 11:
        #         if l[0]== PubKey:
        #             kke['Hash'] = l[4]
        #         elif l[1]== PubKey:
        #             kke['Hash'] = l[5]
        #         elif l[8]== PubKey:
        #             kke['Hash'] = l[9]

        return kke
    return Send_T1(get_User_S(Address, Wallet))
def get_User_S(Address, Wallet = 'SKR'):

    return {'Protocol':'get_User','Wallet':Wallet,'Address':Address}
def get_User_R(dat):

    return get_User(dat['Address'], dat['Wallet'])
#done
def Registr(PubKey, Wallet, AddressTo = '', FuncH = '', Func = '', AddressFrom = ''):
    if Wallet in conf.conf['OtherWallets'] and AddressFrom== '':
        AddressFrom = RegistrOUT(Wallet, PubToAdr(PubKey))
    if conf.conf['isServer'] :
        Address = PubToAdr(PubKey)
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{Address}' ''')
        if (c.fetchone() is None):
            conn.close()
            User.Create(Address, PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom)
        else:
            conn.close()
            return
    Send_T1(Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom))
def Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom):

    return {'Protocol':'Registr','PubKey':PubKey,'Wallet':Wallet,'AddressTo':AddressTo,'FuncH':FuncH,'Func':Func,'AddressFrom':AddressFrom}
def Registr_R(dat):

    Registr(dat['PubKey'], dat['Wallet'], dat['AddressTo'], dat['FuncH'], dat['Func'], dat['AddressFrom'])



def RegistrOUT(Wal, AddressTo):
    if not Wal in conf.conf['OtherWallets']:
        return
    if conf.conf['isSUPER']:
        Wal = Wal.lower()
        import WebNet
        W = WebNet.WalleT(Wal, Generator(64), AddressTo)
        W.save()
        return W.Adr
    return Send_T1(RegistrOUT_S(Wal, AddressTo),Out = True)
def RegistrOUT_S(Wallet, AddressTo):

    return {'Protocol':'RegistrOUT','Wallet':Wallet,'AddressTo':AddressTo}
def RegistrOUT_R(dat):

    return RegistrOUT(dat['Wallet'], dat['AddressTo'])

def DelSUPERIP(ip):
    if not ip in conf.conf['SUPERIP']:
        return

    x = conf.conf['SUPERIP']
    x.remove(ip)
    conf.conf['SUPERIP'] = x
    del x
    Send_T1(DelSUPERIP_S(ip))
def DelSUPERIP_S(ip):

    return {'Protocol':'DelSUPERIP','IP':ip}
def DelSUPERIP_R(dat):

    DelSUPERIP(dat['IP'])

def NewSUPERIP(ip):
    if ip in conf.conf['SUPERIP']:
        return
    x = conf.conf['SUPERIP']
    x.append(ip)
    conf.conf['SUPERIP'] = x
    del x
    Send_T1(NewSUPERIP_S(ip))
def NewSUPERIP_S(ip):

    return {'Protocol':'NewSUPERIP','IP':ip}
def NewSUPERIP_R(dat):

    NewSUPERIP(dat['IP'])

def AddWalletOUT(Wallet):
    if Wallet in conf.conf['OtherWallets']:
        return
    x = conf.conf['OtherWallets']
    x.append(Wallet)
    conf.conf['OtherWallets'] = x
    del x
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
                Address         varchar(128)     NOT NULL,
                AddressTo         varchar(128) ,
                PubKey             varchar(128)     NOT NULL,
                FuncH             varchar(128) ,
                Func             varchar(128) ,
                Time            Double    ,
                Freez            Double            NOT NULL,
                Balance            Double            NOT NULL,
                Hash            varchar(128)    NOT NULL,
                AddressFrom        varchar(128),
                Wallet             varchar(16)     NOT NULL
            ) ''')
        conn.commit()
        conn.close()
    Send_T1(AddWalletOUT_S(Wallet))
def AddWalletOUT_S(Wallet):

    return {'Protocol':'AddWalletOUT','Wallet':Wallet}
def AddWalletOUT_R(dat):

    AddWalletOUT(dat['Wallet'])

def getBalanceOUT(Wal, Address):#exteranl Address
    # if not Wal in conf.conf['OtherWallets']:
    #     return 'ERROR'
    if conf.conf['isSUPER']:
        Wal = Wal.lower()
        import WebNet
        return WebNet.WalleT.getBalance(Address, Wal)
    return Send_T1(getBalanceOUT_S(Wal, Address),OUT = True)
def getBalanceOUT_S(Wallet, Address):

    return {'Protocol':'getBalanceOUT','Address':Address,'Wallet':Wallet}
def getBalanceOUT_R(dat):

    return getBalanceOUT(dat['Wallet'], dat['Address'])

def SendOUT_P1(Address, AddressTo, Sum, Wal):
    Wal = Wal.lower()
    if conf.conf['isSUPER']:
        import WebNet
        k = WebNet.get_account(Address, Wal)
        k.Send(AddressTo, Sum)
        return True

def SendOUT_P(Address, AddressTo, Pass, Sum, Wal):
    Wal1 = Wal
    Wal = Wal.lower()
    if conf.conf['isSUPER']:
        import WebNet
        k = WebNet.get_account(Address, Wal)
        kek = get_User(k['AddressTo'] , Wal1)
        Pass1 = Address + AddressTo + str(Sum) + Wal
        if not kek.Check(Pass1, Pass):
            return False
        k.Send(AddressTo, Sum)
        T = Tranzh.Create(AdrToPub(k['AddressTo'] ), 'out:' + AddressTo, Wal, Sum, sha256_16(kek['Hash'] + Pass), '', Pass, time_time(), MesIn = '', MesOut = '')
        # TranzhHistory(T)
        return True
    return Send_T1(SendOUT_P_S(Address, AddressTo, Pass, Sum, Wal1),OUT = True)
def SendOUT_P_S(Address, AddressTo, Pass, Sum, Wallet):

    return {'Protocol':'SendOUT_P','Address':Address,'AddressTo':AddressTo,'Pass':Pass,'Sum':Sum,'Wallet':Wallet}
def SendOUT_P_R(sock, dat):

    return SendOUT_P(dat['Address'], dat['AddressTo'], dat['Pass'], dat['Sum'], dat['Wallet'])

def GetDataToSendOUT(Sum, Wal):
    symbol = Wal.lower()
    if conf.conf['isSUPER']:
        import WebNet
        dat = []
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        for row in c.execute(f'''SELECT * FROM {Wal} '''):
            kke = User.FromSQL(row)
            AddressOUT = kke['AddressFrom']
            Bal = float(WebNet.WalleT.getBalance(AddressOUT, symbol))
            if Bal > 0:
                x = min(Sum, Bal)
                Sum -= x
                dat.append(['', kke['PubKey'] , Wal, x, '', ''])
            if Sum<= 0:
                break

        conn.close()
        return dat
    return Send_T1(GetDataToSendOUT_S(Sum, Wal),OUT = True)
def GetDataToSendOUT_S(Sum, Wallet):

    return {'Protocol':'GetDataToSendOUT','Wallet':Wallet,'Sum':Sum}
def GetDataToSendOUT_R(dat):

    return GetDataToSendOUT(dat['Sum'], dat['Wallet'])

#done
def getBalance(Wal, Address):#exteranl Address
    if conf.conf['isServer']:
        kke = get_User(Address, Wal)['Balance']
        if Wal in conf.conf['OtherWallets']:
            kke += getBalanceOUT(Wal, Address)
        return kke
    return Send_T1(getBalance_S(Wal, Address))
def getBalance_S(Wallet, Address):

    return {'Protocol':'getBalance','Wallet':Wallet,'Address':Address}
def getBalance_R(dat):

    return getBalance(dat['Wallet'], dat['Address'])
#done
def getATran(Wal, Address):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        return c.execute(f''' SELECT * FROM ATran WHERE AddressFrom = '{Address}' AND Wallet = '{Wal}' ORDER BY Time DESC LIMIT 0,50''').fetchall()
    return Send_T1(getATran_S(Wal, Address))
def getATran_S(Wallet, Address):

    return {'Protocol':'getATran','Wallet':Wallet,'Address':Address}
def getATran_R(dat):

    return getATran(dat['Wallet'], dat['Address'])
#done
def getHTran(Wal, Address,Adr2 = None,t = None):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        dat = None
        if Adr2 == None:
            dat = c.execute(f''' SELECT * FROM History WHERE PubKey2 = '{AdrToPub(Address)}' AND Wallet = '{Wal}' ORDER BY Time DESC LIMIT 0,50''').fetchall()
        else:
            if  t == None :
                dat = c.execute(f''' SELECT * FROM History WHERE (PubKey2 = '{AdrToPub(Address)}' AND PubKey1 = '{AdrToPub(Adr2)}') OR (PubKey1 = '{AdrToPub(Address)}' AND PubKey2 = '{AdrToPub(Adr2)}') AND Wallet = '{Wal}' ORDER BY Time DESC LIMIT 0,50''').fetchall()
            else:
                dat = c.execute(f''' SELECT * FROM History WHERE (PubKey2 = '{AdrToPub(Address)}' AND PubKey1 = '{AdrToPub(Adr2)}') OR (PubKey1 = '{AdrToPub(Address)}' AND PubKey2 = '{AdrToPub(Adr2)}') AND Time > {t} AND Wallet = '{Wal}' ORDER BY Time DESC LIMIT 0,50''').fetchall()
        conn.close()
        return dat
    return Send_T1(getHTran_S(Wal, Address))
def getHTran_S(Wallet, Address):

    return {'Protocol':'getHTran','Wallet':Wallet,'Address':Address}
def getHTran_R(dat):
    return getHTran(dat['Wallet'], dat['Address'])
#done
def getAOrder(Wal, Address):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        return c.execute(f''' SELECT * FROM Orders WHERE AddressFrom = '{Address}' AND Wallet1 = '{Wal}' ORDER BY t DESC LIMIT 0,50 ''').fetchall()
    return Send_T1(getAOrder_S(Wal, Address))
def getAOrder_S(Wallet, Address):

    return {'Protocol':'getAOrder','Wallet':Wallet,'Address':Address}
def getAOrder_R(dat):

    return getAOrder(dat['Wallet'], dat['Address'])

def getHOrder(Wal, Address):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        return c.execute(f''' SELECT * FROM Orders_H WHERE AddressFrom = '{Address}' AND Wallet1 = '{Wal}' ORDER BY t DESC LIMIT 0,50 ''').fetchall()
    return Send_T1(getHOrder_S(Wal, Address))
def getHOrder_S(Wallet, Address):

    return {'Protocol':'getHOrder','Wallet':Wallet,'Address':Address}
def getHOrder_R(dat):

    return getHOrder(dat['Wallet'], dat['Address'])


def getDataForGraf(Wallet1, Wallet2,Time,lastTime):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        Graf = []
        dat = c.execute(f'''SELECT k,t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wallet2}' AND t <= {Time}  AND t >= {Time-lastTime} ORDER BY t DESC''').fetchall()
        if len(dat) == 0:
            dat = c.execute(f'''SELECT k,t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wallet2}' AND t <= {Time} ORDER BY t DESC LIMIT 0,1''').fetchall()
        conn.commit()
        conn.close()
        return dat
    return Send_T1(getDataForGraf_S(Wallet1, Wallet2,Time,lastTime))
def getDataForGraf_S(Wallet1, Wallet2,Time,lastTime):

    return {'Protocol':'getDataForGraf','Wallet1':Wallet1,'Wallet2':Wallet2,'Time':Time,'lastTime':lastTime}
def getDataForGraf_R(dat):
    return getDataForGraf(dat['Wallet1'], dat['Wallet2'],dat['Time'],dat['lastTime'])
#done
def GetPricesF(Wallet1,data):#exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect('Sakaar/exmp1.db')
        c = conn.cursor()
        for Wal2 in data:
            try:
                ti = time_time();
                lol = c.execute(f'''SELECT k,t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wal2}' AND t <= {ti} ORDER BY t DESC LIMIT 0,1''').fetchall()
                if len(lol)>0:
                    data[Wal2] = float(lol[0][0])
                else:
                    data[Wal2] = -1
            except Exception as e:
                data[Wal2] = -1
        conn.commit()
        conn.close()
        return data
    return Send_T1(GetPricesF_S(Wallet1, data))
def GetPricesF_S(Wallet1, data):

    return {'Protocol':'GetPricesF','Wallet1':Wallet1,'data':data}
def GetPricesF_R(dat):
    return GetPricesF(dat['Wallet1'], dat['data'])
