from threading import Thread
from Sakaar.Crypto import *
import os, json, io
from time import time as time_time, sleep as time_sleep
from random import randint
from sqlite3 import connect as sql3connect
from shelve import open as shelve_open
from requests import post as requests_post
from flask import Flask, g, request, jsonify, make_response, render_template, send_file
from base64 import b64decode, b64encode
from pyngrok import ngrok
from flask_cors import CORS
import Sakaar.WebNet

Path = os.path.dirname(__file__)
Version = '1.0.31'

app = Flask(__name__)
CORS(app)


def Generator(size):
    size = int(size)
    fro = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM'
    res = ''
    for i in range(size):
        lol = randint(0, len(fro))
        res += fro[lol % len(fro)]
    return res


def Send_TCP(str, sock):
    str = json.dumps(str)
    sock.send(encode(len(str), 64, 2).encode())
    sock.send(str.encode())


def Recv_TCP(sock):
    return json.loads(sock.recv(decode(sock.recv(2).decode(), 64)).decode())


def DeleteIP_TCP():
    if conf.conf['MyIP_TCP'] != None and conf.conf['MyIP_TCP'] in conf.conf['Connected_TCP'] and conf.conf['MyIP_TCP'][
        2] == conf.conf['login']:
        DelIP_TCP(conf.conf['MyIP_TCP'], PrivCode(
            decode(json.dumps(['DelIP', conf.conf['MyIP_TCP'][0], conf.conf['MyIP_TCP'][1], conf.conf['login']]), 256),
            conf.conf['PrivKey']))


def AddMyIP_TCP():
    if not (conf.conf['In']):
        return
    if 'MyIP_TCP' not in conf.conf or conf.conf['MyIP_TCP'] == None or conf.conf['MyIP_TCP'][2] != conf.conf['login']:
        ip = input("IP () : ")
        port = int(input("Port (1234) : "))
        conf.conf['MyIP_TCP'] = [ip, port, conf.conf['login']]
        NewIP_TCP(conf.conf['MyIP_TCP'],
                  PrivCode(decode(json.dumps(['NewIP', ip, port, conf.conf['login']]), 256), conf.conf['PrivKey']))
    elif conf.conf['MyIP_TCP'] not in conf.conf['Connected_TCP'] and conf.conf['MyIP_TCP'][2] == conf.conf['login']:
        NewIP_TCP(conf.conf['MyIP_TCP'], PrivCode(
            decode(json.dumps(['NewIP', conf.conf['MyIP_TCP'][0], conf.conf['MyIP_TCP'][1], conf.conf['login']]), 256),
            conf.conf['PrivKey']))


def DeleteIP():
    if conf.conf['MyIP'] != None and conf.conf['MyIP'] in conf.conf['Connected'] and conf.conf['MyIP'][1] == conf.conf[
        'login']:
        DelIP(conf.conf['MyIP'], PrivCode(decode(json.dumps(['DelIP', conf.conf['MyIP'][0], conf.conf['login']]), 256),
                                          conf.conf['PrivKey']))


def AddMyIP():
    if 'MyIP' not in conf.conf or conf.conf['MyIP'] == None or conf.conf['MyIP'][1] != conf.conf['login']:
        ip = input("IP () : ")
        conf.conf['MyIP'] = [ip, conf.conf['login']]
        NewIP(conf.conf['MyIP'],
              PrivCode(decode(json.dumps(['NewIP', ip, conf.conf['login']]), 256), conf.conf['PrivKey']))
    elif conf.conf['MyIP'] not in conf.conf['Connected'] and conf.conf['MyIP'][1] == conf.conf['login']:
        NewIP(conf.conf['MyIP'], PrivCode(decode(json.dumps(['NewIP', conf.conf['MyIP'][0], conf.conf['login']]), 256),
                                          conf.conf['PrivKey']))
    conf.conf.close()
    get_conf()


def DelIP_TCP(ip, Pass):
    if not ip in conf.conf['Connected_TCP']:
        return
    pub = PubCode(Pass, get_UserOF(ip[2])['PubKey'])
    lol = decode(json.dumps(['DelIP', ip[0], ip[1], ip[2]]), 256)
    if pub != lol:
        return
    x = conf.conf['Connected_TCP']
    x.remove(ip)
    conf.conf['Connected_TCP'] = x
    print(x)  # LOL
    del x
    Send_T1(DelIP_TCP_S(ip, Pass))


def NewIP_TCP(ip, Pass):
    if ip in conf.conf['Connected_TCP']:
        return
    pub = PubCode(Pass, get_UserOF(ip[2])['PubKey'])
    lol = decode(json.dumps(['NewIP', ip[0], ip[1], ip[2]]), 256)
    if pub != lol:
        return
    x = conf.conf['Connected_TCP']
    for i in x:
        if i[2] == ip[2]:
            x.remove(i)
    x.append(ip)
    conf.conf['Connected_TCP'] = x
    print(x)  # LOL
    del x
    Send_T1(NewIP_TCP_S(ip, Pass))


def DelIP(ip, Pass):
    if not ip in conf.conf['Connected']:
        return
    pub = PubCode(Pass, get_UserOF(ip[1])['PubKey'])
    lol = decode(json.dumps(['DelIP', ip[0], ip[1]]), 256)
    if pub != lol:
        return
    x = conf.conf['Connected']
    x.remove(ip)
    conf.conf['Connected'] = x
    print(x)  # LOL
    del x
    Send_T1(DelIP_S(ip, Pass))


def NewIP(ip, Pass):
    if ip in conf.conf['Connected']:
        return
    pub = PubCode(Pass, get_UserOF(ip[1])['PubKey'])
    lol = decode(json.dumps(['NewIP', ip[0], ip[1]]), 256)
    if pub != lol:
        return
    x = conf.conf['Connected']
    for i in x:
        if i[1] == ip[1]:
            x.remove(i)
    x.append(ip)
    conf.conf['Connected'] = x
    print(x)
    del x
    Send_T1(NewIP_S(ip, Pass))


#
def Server_Ent_TCP():
    sock = socket.socket()
    sock.bind(('', 10101))
    while (True):
        sock.listen(1)
        conn, addr = sock.accept()
        Server_Proc_TCP(conn)
        conn.close()


def Server_Proc_TCP(sock):
    res = None
    tor = 1
    try:
        dat = Recv_TCP(sock)
        get_conf()
        if dat is None:
            Send_TCP(res, sock)
        print(dat['Protocol'])
        if dat['Protocol'] in Functions_R_res:
            res = Functions_R_res[dat['Protocol']](dat)
        else:
            tor = 0
        Send_TCP(res, sock)
        if tor:
            return
        if dat['Protocol'] in Functions_R:
            Functions_R[dat['Protocol']](dat)
    except Exception as e:
        pass
    finally:
        conf.conf.close()


def Server_Ent():
    conf.conf['isRunning'] = True
    app.run(host='127.0.0.1', port=10101)


@app.after_request
def lol(f):
    get_conf()
    dat = None
    try:
        try:
            dat = g.dat
        except Exception as e:
            pass
        if dat is None:
            return f
        if dat['Protocol'] in Functions_R:
            Functions_R[dat['Protocol']](dat)
    except Exception as e:
        print(e)
    return f


@app.route("/", methods=['GET'])
def Main_program():
    return render_template("index.html")


@app.route("/", methods=['POST'])
def Server_Proc():
    res = None
    try:
        g.dat = dat = json.loads(request.data.decode())
        get_conf()
        if dat is None:
            return jsonify(res)
        print(dat['Protocol'])
        if dat['Protocol'] in Functions_R_res:
            res = Functions_R_res[dat['Protocol']](dat)
    except Exception as e:
        print(e)
    return jsonify(res)

@app.route('/user_logo/<login>')
def show_user_profile(login):
    src = 'avatar2.png'
    conn = sql3connect(Path + '/exmp1.db')
    c = conn.cursor()
    dat = c.execute(
        f''' SELECT Photo FROM UserOF WHERE Address = '{login}' ''').fetchall()[0][0]
    conn.close()
    if(dat != None):
        dat = b64decode(encode(PubCode(decode(dat,256),get_UserOF(login)['PubKey']),256).encode('utf-8'))
        return send_file(io.BytesIO(dat),attachment_filename='logo.png',
                     mimetype='image/png')
    # show the user profile for that user
    return send_file(src)

def Send_T1(dat, OUT=False, func=None):  # Send to all
    if OUT == False:
        for ip in conf.conf['Connected_TCP']:
            if ip == conf.conf['MyIP_TCP']:
                continue
            try:
                sock = socket.socket()
                sock.connect((ip[0], ip[1]))
                Send_TCP(dat, sock)
                res = Recv_TCP(sock)
                sock.close()
                # print (type(res), res)
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass
        for ip in conf.conf['Connected']:
            if ip == conf.conf['MyIP']:
                continue
            try:
                res = requests_post(f'http://{str(ip[0])}/', json=dat)
                res = res.json()
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass
    else:
        for ip in conf.conf['SUPERIP_TCP']:
            ip1 = json.loads(encode(PubCode(int(ip), AdrToPub(conf.conf['Key'])), 256))
            try:
                sock = socket.socket()
                sock.connect((ip1[0], ip1[1]))
                Send_TCP(dat, sock)
                res = Recv_TCP(sock)
                sock.close()
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass
        for ip in conf.conf['SUPERIP']:
            ip1 = encode(PubCode(int(ip), AdrToPub(conf.conf['Key'])), 256)
            try:
                res = requests_post(f'http://{str(ip1[0])}/', json=dat)
                res = res.json()
                if not func is None:
                    res = func(res)
                if not res is None:
                    return res
            except Exception as e:
                pass


def End(tor=True):
    if conf.conf['isRunning']:
        CloseNODA()


def Start():
    if conf.conf['isRunning']:
        BecomNODA()


def BecomNODA():
    if get_User(get_UserOF(conf.conf['login'])['Balance']['SKR'][0][0], 'SKR')['Freez'] >= 1000:
        while (conf.conf['HTTP_TCP'] != "HTTP" and lol != "TCP"):
            conf.conf['HTTP_TCP'] = input('Choose TCP or HTTP : ')
        if (conf.conf['HTTP_TCP'] == "HTTP"):
            variable = Thread(target=Server_Ent, args=())
        else:
            variable = Thread(target=Server_Ent_TCP, args=())
        variable.start()
        try:
            GetAllData()
            GetConf()
        except Exception as e:
            pass
        AddMyIP()
        if (conf.conf['HTTP_TCP'] == "HTTP"):
            AddMyIP()
        else:
            AddMyIP_TCP()
        conf.conf['isRunning'] = True
        conf.conf['isServer'] = True
        Activate(conf.conf['login'])


def CloseNODA():
    DeleteIP()
    DisActivate(conf.conf['login'])
    conf.conf['isRunning'] = False


def LogOut():
    conf.conf['login'] = ''
    conf.conf['passw'] = ''
    conf.conf['PrivKey'] = ''
    conf.conf['PubKey'] = ''
    conf.conf['In'] = False


def RegistrNewWallet(Wallet):
    if conf.conf['In']:
        PrivKey = GetUnUsedAddress(Wallet)
        PubKey = PrivToPub(PrivKey)
        Registr(PubKey, Wallet, conf.conf['login'])
        PrivKey = decode(PrivKey, 16)
        PrivKey = (PubCode(PrivKey, conf.conf['PubKey']))
        time_sleep(0.5)
        ConACC(conf.conf['login'], Wallet, PubToAdr(PubKey), PrivKey)
        return encode(PrivKey, 16)


def SendOUT(Wal, Address, AddressTo, Sum):  # Using our Address system and external Address To
    if conf.conf['In']:
        kek = get_UserOF(conf.conf['login'])['Balance'][Wal]
        lol = None
        i = 0
        while i < len(kek):
            if kek[i][0] == Address:
                lol = kek[i][1]
                break
        if (lol == None):
            return
        kke = get_User(Address, Wal)
        BOut = getBalanceOUT(Wal, kke['AddressFrom'])
        x = min(float(BOut), Sum)
        lol = PrivCode(lol, conf.conf['PrivKey'])
        lol = encode(lol, 16)
        SendOUT_P(kke['AddressFrom'], AddressTo,
                  PrivCode(decode(kke['AddressFrom'] + AddressTo + str(x) + Wal, 256), lol), x, Wal)
        Sum -= x
        if Sum <= 0:
            return
            # lol = decode(lol, 16)
        dat = GetDataToSendOUT(Sum, Wal)
        i = 0
        while i < len(dat):
            dat[i][0] = kke['PubKey']
            dat[i][4] = lol
            i += 1
        SendTranzh(Tranzhs.Create(PreSendTranzh(dat), AddressTo,
                                  PrivCode(decode(kke['AddressFrom'] + AddressTo + str(Sum) + Wal, 256), lol)))


def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])


def CheckVer():
    ver = Send_T1(CheckVer_S())
    if ver != None and ver != conf.conf['Version']:
        conf.conf['ExitCode'] = 82
        conf.conf.close()
        os._exit(82)
    else:
        dat = {'dirs': [], 'files': []}

        def indir(dirs, arc):
            dat['dirs'].append(dirs[arc:])
            for file in os.listdir(dirs):
                if os.path.isfile(dirs + '//' + file):
                    with open(dirs + '//' + file, 'rb') as input:
                        if file != '.DS_Store' and file != 'exmp1.db' and file != 'V_type.py' and file != 'Out_Data_Base.db':
                            dat['files'].append([(dirs + '//' + file)[arc:],
                                                 str(b64encode(input.read()), 'utf-8', errors='ignore').strip()])
                elif file != '__pycache__':
                    indir(dirs + '//' + file, arc)

        indir(Path, len(Path) - 6)
        dat['files'] = sorted(dat['files'])
        import Sakaar.V_type
        # print(PubCode(int(V_type.Key), AdrToPub(conf.conf['Key'])))
        if decode(sha256_16(sha256_16(dat) + conf.conf['Version']), 16) != PubCode(int(V_type.Key),
                                                                                   AdrToPub(conf.conf['Key'])):
            # pass
            raise Exception("Incorrect version of soft")


def UpDate(Ver):
    Send_T1(UpDate_S(Ver))


def GetConf():
    dat = Send_T1(GetConf_S())
    if dat is None:
        raise "Error with connection"
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
    conf.conf['VoitingTime'] = dat[11]
    conf.conf['VoitingTitle'] = dat[12]
    conf.conf['VoitingDescription'] = dat[13]
    conf.conf['Connected_TCP'] = dat[14]
    conf.conf['SUPERIP_TCP'] = dat[15]


def VoteFor(key, Address=None, Pass=None):
    if Pass == None and conf.conf['In']:
        Address = conf.conf['login']
        Pass = PrivCode(decode(key, 256), conf.conf['PrivKey'])
    elif not conf.conf['In']:
        return
    if time_time() - conf.conf['VoitingTime'] == 34560:
        print("You are late")
        return
    if conf.conf['isServer']:
        kke = get_UserOF(Address)
        if not User.Check(kke, key, Pass):
            print('Error')
            return
        kke = get_User(kke['Balance']['SKR'][0][0], 'SKR')
        if kke['Freez'] <= 0 or Address in conf.conf['Voited']:
            print('Error1')
            return
        x = conf.conf['Voited']
        x[Address] = key
        conf.conf['Voited'] = x
        del x
        x = conf.conf['Voiting']
        x[key][0] += kke['Freez']
        conf.conf['Voiting'] = x
        del x
    Send_T1(VoteFor_S(Address, key, Pass))


def ChangeVoiting(new, newTiltel, newDidk):  # obj <- Str <- int
    dat = json.loads(encode(PubCode(new, AdrToPub(conf.conf['Key'])), 256))
    if conf.conf['Voiting'] != dat:
        conf.conf['Voited'] = {}
        conf.conf['Voiting'] = dat
        conf.conf['VoitingTime'] = time_time()
        conf.conf['VoitingDescription'] = json.loads(encode(PubCode(newDidk, AdrToPub(conf.conf['Key'])), 256))
        conf.conf['VoitingTitle'] = json.loads(encode(PubCode(newTiltel, AdrToPub(conf.conf['Key'])), 256))
    else:
        return
    Send_T1(ChangeVoiting_S(new, newTiltel, newDidk))


def UpdateVoiting():
    conf.conf['Voiting'] = Send_T1(GetVoiting_S())
    return


def GetAllData():
    dat = Send_T1(GetAllData_S())
    if dat is None:
        raise "Error with connection"
    for x in dat:
        with open(Path[:len(Path) - 6] + x, 'wb') as f:
            f.write(b64decode(bytes(dat[x], 'utf-8')))


def CancelOrder(stk, Pass=None):
    if Pass == None and conf.conf['In'] and conf.conf['login'] == get_User(stk['Address1'], stk['Wallet1'])[
        'AddressTo']:
        Pass = PrivCode(decode(str(stk), 256), conf.conf['PrivKey'])
        SendTranzh(Tranzhs.Create(PreSendTranzh([[PrivToPub(stk['priv']), AdrToPub(
            get_UserOF(conf.conf['login'])['Balance'][stk['Wallet1']][0][0]), stk['Wallet1'], stk['Sum1'], stk['priv'],
                                                  '']])))
    elif Pass == None and not (
            conf.conf['In'] and conf.conf['login'] == get_User(stk['Address1'], stk['Wallet1'])['AddressTo']):
        return
    if conf.conf['isServer']:
        if not User.Check(get_UserOF(get_User(stk['Address1'], stk['Wallet1'])['AddressTo']), str(stk), Pass):
            return
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        x = c.execute(
            f'''SELECT * From Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}'  AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''').fetchall()
        if len(x) == 0:
            conn.close()
            return
        stk = Order.FromSQL(x[0])
        c.execute(
            f'''DELETE FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
        conn.commit()
        c.execute(f'''UPDATE {stk['Wallet1']} SET FuncH = '', Func = '' WHERE Address = '{stk['Address1']}' ''')
        conn.commit()
        conn.close()
    Send_T1(CancelOrder_S(stk, Pass))


def CancelOrder_S(stk, Pass):
    return {'Protocol': 'CancelOrder', 'Stk': stk, 'Pass': Pass}


def MakeOrder(Adr1, Wal1, Sum1, Adr2, Wal2, k):
    if conf.conf['In']:
        # print ('MakeOrder')
        Priv = None
        usr1 = get_UserOF(conf.conf['login'])
        for pop in usr1['Balance'][Wal1]:
            if (pop[0] == Adr1):
                Priv = encode(PrivCode(pop[1], conf.conf['PrivKey']), 16)
        if Priv == None:
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
                    mas[T['Wal']][T['PubKey1']] = get_User(PubToAdr(T['PubKey1']), T['Wal'])
                    if mas[T['Wal']][T['PubKey1']]['Func'] != '':
                        if (tor == 1):
                            res = 0
                            break
                        tor = 1
                        print(mas[T['Wal']][T['PubKey1']])
                        stk = User.getFunc(mas[T['Wal']][T['PubKey1']])
                if not T['PubKey2'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey2']] = get_User(PubToAdr(T['PubKey2']), T['Wal'])
                res &= Checker(T, mas[T['Wal']][T['PubKey1']], mas[T['Wal']][T['PubKey2']])
                mas[T['Wal']][T['PubKey1']]['Balance'] -= T['Sum']
                if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
                else:
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
                mas[T['Wal']][T['PubKey1']]['Hash'] = T['Hash1']
                mas[T['Wal']][T['PubKey2']]['Hash'] = T['Hash2']
            res = res and (tor != 1 or Func(mas, TS, stk))
            print(res, (tor != 1 or Func(mas, TS, stk)))
            return res

        dat = get_Order(Wal2, Wal1, 1 / k)
        # print (dat)
        for row in dat:
            row = Order.FromSQL(row)
            usr02 = get_User(row['Address1'], Wal2)
            t = time_time()
            # print (stk2.Adr1 + " " + Adr1)
            SUM1 = min(Sum1, usr02['Balance'] / k)
            SUM2 = min(Sum1 * k, usr02['Balance'])
            # print ('OLOLO', row, Adr2)
            # print('SUMM', SUM1, SUM2)
            TS = [[PrivToPub(row['priv']), AdrToPub(Adr2), Wal2, SUM2, row['priv'], ''],
                  [AdrToPub(Adr1), AdrToPub(row['Address2']), Wal1, SUM1, Priv, '']]
            TS = PreSendTranzh(TS)
            # print ('NOOOOO', COOL(TS))
            # if COOL(TS):
            Sum1 -= SUM1
            SendTranzh(Tranzhs.Create(TS))
        # print (Sum1)
        if (Sum1 > 0):
            PrivKey = GetUnUsedAddress(Wal1)
            PubKey = PrivToPub(PrivKey)
            # print ('lll', PrivKey, PubKey)
            t = time_time()
            Stk = Order.FromSQL((PubToAdr(PubKey), Adr2, conf.conf['login'], Wal1, Wal2, Sum1, Sum1, k, t, t, PrivKey))
            x = User.CodeFunc(Stk, conf.conf['PrivKey'])
            Registr(PubKey, Wal1, conf.conf['login'], x[0], x[1])
            PrivKey = decode(PrivKey, 16)
            PrivKey = (PubCode(PrivKey, conf.conf['PubKey']))
            time_sleep(0.5)
            ConACC(conf.conf['login'], Wal1, PubToAdr(PubKey), PrivKey)
            # print (AdrToPub(Adr1)== PubKey)
            # print ('Priv :', Priv)
            TS = [[AdrToPub(Adr1), PubKey, Wal1, Sum1, Priv, '']]
            SendTranzh(Tranzhs.Create(PreSendTranzh(TS)))
            time_sleep(3)
            # print (get_User(PubToAdr(PubKey), Wal1)['Balance'] )
            # print
            Send_T1(SendOrder_S(Stk))


def Func(mas, TS, stk):
    lol = len(TS) == 1 and mas[TS[0]['Wal']][TS[0]['PubKey1']]['AddressTo'] == mas[TS[0]['Wal']][TS[0]['PubKey2']][
        'AddressTo']
    # print (len(TS)== 2, mas[TS[0]['PubKey1'] ]['AddressTo'], mas[TS[1]['PubKey2'] ]['AddressTo'], stk, stk['Wallet1']== TS[0]['Wal'], stk['Wallet2']== TS[1]['Wal'], TS[0]['Sum'] / TS[1]['Sum']== stk['k'], mas[TS[0]['PubKey1'] ]['Address']== stk['Address1'])
    pop = len(TS) == 2 and mas[TS[0]['Wal']][TS[0]['PubKey1']]['AddressTo'] == mas[TS[1]['Wal']][TS[1]['PubKey2']][
        'AddressTo'] and stk['Wallet1'] == TS[0]['Wal'] and stk['Wallet2'] == TS[1]['Wal'] and TS[0]['Sum'] / TS[1][
              'Sum'] == stk['k'] and mas[TS[0]['Wal']][TS[0]['PubKey1']]['Address'] == stk['Address1']
    return lol or pop


def chOrder(a, b):
    [x['Address1'], x['Address2'], x['SumS'], x['k'], x['t'], x['priv']]
    return (a.Adr1 == b.Adr1) and (a.Adr2 == b.Adr2) and (a.t == b.t) and (a.Wal1 == b.Wal1) and (
                a.Wal2 == b.Wal2) and (a.k == b.k)


def SendOrder(stk):
    if conf.conf['isServer']:
        if stk['Sum1'] <= 0 or stk['k'] <= 0:
            return
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(
            f'''SELECT * FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
        if not (c.fetchone() is None):
            conn.close()
            return
        conn.close()
        Order.Create(stk['Address1'], stk['Wallet1'], stk['AddressFrom'], stk['Sum1'], stk['Address2'], stk['Wallet2'],
                     stk['k'], stk['t'], stk['priv'])
    Send_T1(SendOrder_S(stk))


def get_Order(Wallet1, Wallet2, k=0):
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        if k != 0:
            dat = c.execute(
                f'''SELECT * FROM Orders WHERE Wallet1 = '{Wallet1}' AND Wallet2 = '{Wallet2}' AND k = {k} AND Sum1 > 0''').fetchall()
        else:
            dat = c.execute(
                f'''SELECT * FROM Orders WHERE Wallet1 = '{Wallet1}' AND Wallet2 = '{Wallet2}' AND Sum1 > 0''').fetchall()
        conn.close()
        return dat
    return Send_T1(get_Order_S(Wallet1, Wallet2, k))


def ANConACC(Login, Wallet, AddressTo, Pass=None):
    if Pass == None:
        if conf.conf['In'] and conf.conf['login'] == Login:
            Pass = PrivCode(decode(str(Login) + str(Wallet) + str(AddressTo), 256), conf.conf['PrivKey'])
        else:
            return
    if conf.conf['isServer']:
        kke = get_UserOF(Login)
        if User.Check(kke, str(Login) + str(Wallet) + str(AddressTo), Pass):
            conn = sql3connect(Path + '/exmp1.db')
            c = conn.cursor()
            c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Login}' ''')
            tor = not (c.fetchone() is None)
            c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{AddressTo}' AND AddressTo = '{Login}' ''')
            if not (c.fetchone() is None) and tor:
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
                    c.execute(
                        f'''UPDATE {Wallet} SET AddressTo = '', FuncH = '', Func = '' WHERE Address = '{AddressTo}' AND AddressTo = '{Login}' ''')
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
    Send_T1(ANConACC_S(Login, Wallet, AddressTo, Pass))


def Login(login, Password):
    if not conf.conf['In']:
        res = get_UserOF(login)['PubKey']
        if res == PrivToPub(sha256_16(sha256_16(login + sha256_16(Password)))):
            conf.conf['login'] = login
            print(conf.conf['login'])
            conf.conf['passw'] = sha256_16(Password)
            print(conf.conf['passw'])
            conf.conf['PrivKey'] = sha256_16(sha256_16(login + sha256_16(Password)))
            print(conf.conf['PrivKey'])
            conf.conf['PubKey'] = PrivToPub(conf.conf['PrivKey'])
            print(conf.conf['PubKey'])
            conf.conf['In'] = True
            print('LogIN')
            if IsServer(conf.conf['login']):
                print('Active')


def CreateAccountS(Login, Hash):
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Login}' ''')
        if not (c.fetchone() is None):
            conn.close()
            return
        conn.close()
        UserOF.Create(Login, Hash)
        # print kke['Balance']
    Send_T1(CreateAccountS_S(Login, Hash))


def CreateAccount(Login, Password):
    CreateAccountS(Login, PrivToPub(sha256_16(sha256_16(Login + sha256_16(Password)))))


def get_UserOF(Address):
    if conf.conf['isServer']:
        kke = None
        Address = str(Address)
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        dat = c.execute(f'''SELECT * FROM UserOF WHERE Address = '{Address}' ''').fetchone()
        if not (dat is None):
            kke = UserOF.FromSQL(dat)
        conn.close()
        return kke
    return Send_T1(get_UserOF_S(Address))


def IsServer(Address):
    if conf.conf['isServer']:
        return get_UserOF(Address)['Active']
    return Send_T1(IsServer_S(Address))


def AddWallet(Wallet):
    if Wallet in conf.conf['OurWallets']:
        return
    x = conf.conf['OurWallets']
    x.append(Wallet)
    conf.conf['OurWallets'] = x
    del x
    conn = sql3connect(Path + '/exmp1.db')
    c = conn.cursor()
    c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
            Address         varchar(128)     NOT NULL,
            AddressTo         varchar(128),
            PubKey             varchar(128)     NOT NULL,
            FuncH             varchar(128),
            Func             varchar(128),
            Time            Double,
            Freez            Double            NOT NULL,
            Balance            Double            NOT NULL,
            Hash            varchar(128)    NOT NULL,
            AddressFrom        varchar(128),
            Wallet             varchar(16)     NOT NULL
            ); ''')
    conn.commit()
    conn.close()
    Send_T1(AddWallet_S(Wallet))


def ConACC(Address, Wallet, AddressTo, PrivKey):
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Address}' ''')
        tor = not (c.fetchone() is None)
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{AddressTo}' ''')
        if not (c.fetchone() is None) and tor:
            kke = get_UserOF(Address)['Balance']
            if not Wallet in kke:
                kke[Wallet] = []
            lol = [AddressTo, str(PrivKey)]
            if Wallet in conf.conf['OtherWallets']:
                lol.append(get_User(AddressTo, Wallet)['AddressFrom'])
            if lol in kke[Wallet]:
                return
            kke[Wallet].append(lol)
            c.execute(f'''UPDATE UserOF SET Balance = '{json.dumps(kke)}' WHERE Address = '{Address}' ''')
            conn.commit()
            print('ConACC OK')
            conn.close()
        else:
            print('ConACC ERRROR', tor, not (c.fetchone() is None))
            conn.close()
            return
    Send_T1(ConACC_S(Address, Wallet, AddressTo, PrivKey))


def SaveTranzhs(Tranzh):
    mas = {}
    res = 1
    tor = 0
    stk = None
    for T in Tranzh['TS']:
        if not T['Wal'] in mas:
            mas[T['Wal']] = {}
        if not T['PubKey1'] in mas[T['Wal']]:
            mas[T['Wal']][T['PubKey1']] = get_User(PubToAdr(T['PubKey1']), T['Wal'])
            if mas[T['Wal']][T['PubKey1']]['Func'] != '':
                if (tor == 1):
                    res = 0
                    break
                tor = 1
                stk = User.getFunc(mas[T['Wal']][T['PubKey1']])
        if not T['PubKey2'] in mas[T['Wal']]:
            mas[T['Wal']][T['PubKey2']] = get_User(PubToAdr(T['PubKey2']), T['Wal'])
        res &= Checker(T, mas[T['Wal']][T['PubKey1']], mas[T['Wal']][T['PubKey2']])
        mas[T['Wal']][T['PubKey1']]['Hash'] = T['Hash1']
        mas[T['Wal']][T['PubKey1']]['Balance'] -= T['Sum']
        # TranzhHistory(T)
        mas[T['Wal']][T['PubKey2']]['Hash'] = T['Hash2']
        if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
            mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
        else:
            mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
    res = res and (tor != 1 or Func(mas, Tranzh['TS'], stk))
    conn = sql3connect(Path + '/exmp1.db')
    c = conn.cursor()
    T2 = None
    if Tranzh['AddressTo'] != None and conf.conf['isSUPER']:
        T2 = Tranzh.Create(AdrToPub(k['AddressTo']), 'out/' + AddressTo, Wal, Sum, sha256_16(kek['Hash'] + Pass), '',
                           Pass, time_time(), MesIn='', MesOut='')
    conf.conf['Block'] += 1
    for T in Tranzh['TS']:
        if len(mas[T['Wal']][T['PubKey2']]['AddressTo']) > 0 and len(mas[T['Wal']][T['PubKey2']]['AddressTo']) > 0 and \
                mas[T['Wal']][T['PubKey2']]['AddressTo'] == mas[T['Wal']][T['PubKey1']]['AddressTo']:
            continue
        if Tranzh['AddressTo'] != None and conf.conf['isSUPER']:
            AddressFrom = get_User(PubToAdr(T['PubKey2']), T['Wal'])['AddressFrom']
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
            if looop >= 1000 and len(kke['AddressTo']) > 0 and not kke['AddressTo'] in ARRR:
                kke = get_UserOF(kke['AddressTo'])
                if not kke['Active']:
                    continue
                if T['Wal'] in kke['Balance']:
                    Adr = AdrToPub(kke['Balance'][T['Wal']][0][0])
                    if not Adr in mas[T['Wal']]:
                        mas[T['Wal']][Adr] = get_User(kke['Balance'][T['Wal']][0][0], T['Wal'])
                    popp = looop / conf.conf['FullFreez'] * SumCom
                    Pass = str(T['PubKey1']) + str(T['PubKey2']) + T['Wal'] + str(T['Sum']) + T['Hash1'] + T[
                        'Hash2'] + str(T['time'])
                    Pass = sha256_16(Pass)
                    # T.NODA( AdrToPub(kke['Address'] ), sha256_16( kke['Hash'] + Pass), (looop /conf.conf['FullFreez']))
                    mas[T['Wal']][Adr]['Balance'] += popp
                    T['Comision'].append([mas[T['Wal']][Adr]['Address'], popp])
                    mas[T['Wal']][Adr]['Hash'] = sha256_16(mas[T['Wal']][Adr]['Hash'] + Pass)
                    ARRR.append(kke['Address'])
        c.execute(f'''INSERT INTO History VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
        conf.conf['Block'], PubToAdr(T['PubKey1']), PubToAdr(T['PubKey2']), T['Sum'], T['Comis'], T['Wal'], T['time'],
        mas[T['Wal']][T['PubKey1']]['AddressTo'], mas[T['Wal']][T['PubKey2']]['AddressTo'], json.dumps(T['Comis']),
        encode(int(T['MesIn']),256), encode(int(T['MesOut']),256)))
        conn.commit()
    for wal in mas:
        for name in mas[wal]:
            name = mas[wal][name]
            c.execute(
                f'''UPDATE {name['Wallet']} SET Balance = {str(name['Balance'])}, Hash = '{encode(decode(name['Hash'], 256), 16)}' WHERE Address = '{name['Address']}' ''')
            conn.commit()
    if stk and res and tor and len(Tranzh['TS']) == 2:
        usr1 = get_UserOF(mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1']]['AddressTo'])
        for row in c.execute(
                f'''SELECT * FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' '''):
            row = Order.FromSQL(row)
            if (row['t1'] < Tranzh['TS'][0]['time']):
                row['t1'] = Tranzh['TS'][0]['time']
                row['Sum1'] -= Tranzh['TS'][0]['Sum']
                if row['Sum1'] == 0:
                    c.execute(
                        f'''DELETE FROM Orders WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
                    conn.commit()
                    c.execute(
                        f'''UPDATE {stk['Wallet1']} SET FuncH = '', Func = '' WHERE Address = '{stk['Address1']}' ''')
                    conn.commit()
                else:
                    c.execute(
                        f'''UPDATE Orders SET t1 = {row['t1']}, Sum1 = {row['Sum1']} WHERE Wallet1 = '{stk['Wallet1']}' AND Wallet2 = '{stk['Wallet2']}' AND Address1 = '{stk['Address1']}' AND AddressFrom = '{stk['AddressFrom']}' AND Address2 = '{stk['Address2']}' AND SumS = '{stk['SumS']}' AND k = '{stk['k']}' AND t = '{stk['t']}' AND priv = '{stk['priv']}' ''')
                    conn.commit()
                c.execute(f'''INSERT INTO Orders_H VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (
                stk['k'], row['t1'], stk['Wallet1'], stk['Wallet2'], conf.conf['Block'],
                mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1']]['AddressTo'],
                mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey2']]['AddressTo'], Tranzh['TS'][0]['Sum']))
                conn.commit()
                c.execute(f'''INSERT INTO Orders_H VALUES(?, ?, ?, ?, ?, ?, ?, ?)''', (
                1 / stk['k'], row['t1'], stk['Wallet2'], stk['Wallet1'], conf.conf['Block'],
                mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey2']]['AddressTo'],
                mas[Tranzh['TS'][0]['Wal']][Tranzh['TS'][0]['PubKey1']]['AddressTo'], Tranzh['TS'][1]['Sum']))
                conn.commit()
            break
    conn.commit()
    c.close()
    conn.close()


def EndTranzh(Tranzh, res):
    print('EndTranzh ' + str(res))
    if conf.conf['isServer']:
        tor = False
        print("RES " + str(res))
        for arc in conf.conf['InMemory']:
            if Ch_Tranzh(Tranzh, arc):
                # x = conf.conf['InMemory']
                # x.remove(arc)
                # conf.conf['InMemory'] = x
                # del x
                tor = True
                break
        if tor:
            conn = sql3connect(Path + '/exmp1.db')
            c = conn.cursor()
            for T in Tranzh['TS']:
                c.execute(
                    f'''DELETE FROM ATran WHERE PubKey1 = '{PubToAdr(T['PubKey1'])}' AND PubKey2 = '{PubToAdr(T['PubKey2'])}' AND Wallet = '{T['Wal']}' AND Time = {T['time']} ''')
            conn.commit()
            conn.close()
        if (not tor) or (not res):
            return
        SaveTranzhs(Tranzh)


def Activate(Address):
    if conf.conf['isServer']:
        print(IsServer(Address))
        if IsServer(Address):
            return
        kke = get_UserOF(Address)
        if not 'SKR' in kke['Balance']:
            return
        if get_User(kke['Balance']['SKR'][0][0], 'SKR')['Freez'] < 1000:
            return
        kke['Active'] = True
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''UPDATE UserOF SET Active = true WHERE Address = '{kke['Address']}' ''')
        conn.commit()
        conn.close()
    Send_T1(Activate_S(Address))


def DisActivate(Address):
    if conf.conf['isServer']:
        if 1 != IsServer(Address):
            return
        kke = get_UserOF(Address)
        kke['Active'] = False
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''UPDATE UserOF SET Active = false WHERE Address = '{kke['Address']}' ''')
        conn.commit()
        conn.close()
    Send_T1(DisActivate_S(Address))


def ResTranzh(Address, Tranzh, res, Pass=None):
    if Pass == None and Address == conf.conf['login'] and conf.conf['In']:
        Pass = PrivCode(decode(str(Tranzh) + str(res), 256), conf.conf['PrivKey'])
    elif Pass == None and not (Address == conf.conf['LogIN'] and conf.conf['In']):
        return
    print('ResTranzh ' + str(res > 0))
    lol = 0
    if conf.conf['isServer']:
        if not User.Check(get_UserOF(Address), str(Tranzh) + str(res), Pass):
            return
        kke = get_User(get_UserOF(Address)['Balance']['SKR'][0][0], 'SKR')
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
            print(tor)
            return
    Send_T1(ResTranzh_S(Address, Tranzh, res, Pass))
    print('ResTranzh', conf.conf['isServer'], Ch_Tranzh(Tranzh, conf.conf['InMemory'][i]))
    if conf.conf['isServer'] and Ch_Tranzh(Tranzh, conf.conf['InMemory'][i]):
        if conf.conf['InMemory'][i]['resTO'] >= 0.5 and res and conf.conf['InMemory'][i]['resTO'] - lol < 0.5:
            EndTranzh(Tranzh, True)
        elif conf.conf['InMemory'][i]['resAnti'] > 0.5 and res and conf.conf['InMemory'][i]['resAnti'] - lol <= 0.5:
            EndTranzh(Tranzh, False)


def Checker(T, kke1, kke2):
    print('Checker')
    Pass = sha256_16(
        str(T['PubKey1']) + str(T['PubKey2']) + T['Wal'] + str(T['Sum']) + kke1['Hash'] + kke2['Hash'] + str(T['time']))
    print(Pass)
    res1 = 1
    if (T['Wal'] in conf.conf['OurWallets']):
        # print(kke1['Balance'] - T['Sum']>=0), (kke2['Balance']>=0)
        res1 = (kke1['Balance'] - T['Sum'] >= 0) and (kke2['Balance'] >= 0)
    elif (T['Wal'] in conf.conf['OtherWallets']):
        # print ('ERRROR')
        res1 = (kke1['Balance'] + float(getBalanceOUT(kke1['Wallet'].lower(), kke1['AddressFrom'])) - T['Sum'])
    else:
        # print ('NOOOOOOOOO', T['Wal'], conf.conf['OurWallets'])
        res1 = 0
    tor = T['Comis'] >= conf.conf['Comis'] and User.Check(kke1, Pass, T['Pass']) and sha256_16(kke1['Hash'] + Pass) == T['Hash1'] and sha256_16(kke2['Hash'] + Pass) == T['Hash2'] and T['Sum'] > 0
    print('Checker', T['Comis'] >= conf.conf['Comis'], User.Check(kke1, Pass, T['Pass']),
          sha256_16(kke1['Hash'] + Pass) == T['Hash1'], sha256_16(kke2['Hash'] + Pass) == T['Hash2'], T['Sum'] > 0,
          T['Sum'])
    print('Checker', res1, tor)
    return tor and res1


def CheckerTranzh():
    print('CheckerTranzh')
    i = 0
    while i < len(conf.conf['InMemory']):
        if (time_time() - conf.conf['InMemory'][i]['TS'][0]['time'] > 86400) and (
                conf.conf['InMemory'][i]['resTO'] >= 0.5 or conf.conf['InMemory'][i]['resAnti'] > 0.5):
            x = conf.conf['InMemory']
            x.remove(x[i])
            conf.conf['InMemory'] = x
            continue
        # if not Ch_Tranzh(conf.conf['InMemory'][i], x):
        #     continue
        if not conf.conf['login'] in conf.conf['InMemory'][i]['Users']:
            print("YES")
            res = 1
            mas = {}
            tor = 0
            stk = None
            SUM = 0
            Wal = conf.conf['InMemory'][i]['TS'][0]['Wal']
            OUT = conf.conf['InMemory'][i]['TS'][0]['PubKey1']
            for T in conf.conf['InMemory'][i]['TS']:

                T['MesIn'] = int(T['MesIn'])
                T['MesOut'] = int(T['MesOut'])
                SUM += T['Sum']
                if not T['Wal'] in mas:
                    mas[T['Wal']] = {}
                if not T['PubKey1'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey1']] = get_User(PubToAdr(T['PubKey1']), T['Wal'])
                    if mas[T['Wal']][T['PubKey1']]['Func'] != '':
                        if OUT != T['PubKey1']:
                            OUT = None
                        if (tor == 1):
                            res = 0
                            break
                        tor = 1
                        stk = User.getFunc(mas[T['Wal']][T['PubKey1']])
                    # print ('T["PubKey1"] ' + T['PubKey1'] )
                if Wal != conf.conf['InMemory'][i]['TS'][0]['Wal']:
                    Wal = None
                if not T['PubKey2'] in mas[T['Wal']]:
                    mas[T['Wal']][T['PubKey2']] = get_User(PubToAdr(T['PubKey2']), T['Wal'])
                    # print ('T["PubKey2"] ' + T['PubKey2'] )
                res &= Checker(T, mas[T['Wal']][T['PubKey1']], mas[T['Wal']][T['PubKey2']])
                print(res)
                mas[T['Wal']][T['PubKey1']]['Balance'] -= T['Sum']
                if len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 and mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] :
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum']
                else:
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis'])
                mas[T['Wal']][T['PubKey1']]['Hash'] = T['Hash1']
                mas[T['Wal']][T['PubKey2']]['Hash'] = T['Hash2']
            if conf.conf['InMemory'][i]['AddressTo'] != None or conf.conf['InMemory'][i]['AddressHashed'] != None:
                if conf.conf['InMemory'][i]['AddressTo'] == None or Wal == None or conf.conf['InMemory'][i][
                    'AddressHashed'] == None or OUT == None or not User.Check(mas[Wal][OUT],
                                                                              mas[Wal][OUT]['AddressFrom'] +
                                                                              conf.conf['InMemory'][i][
                                                                                  'AddressTo'] + str(SUM) + Wal,
                                                                              conf.conf['InMemory'][i][
                                                                                  'AddressHashed']):
                    print('ERRROR')
                    res = 0
            res = res and (tor != 1 or Func(mas, conf.conf['InMemory'][i]['TS'], stk))
            print(res, (tor != 1 or Func(mas, conf.conf['InMemory'][i]['TS'], stk)))
            ResTranzh(conf.conf['login'], conf.conf['InMemory'][i], res)
            return
        i += 1


def SendTONODA(Address, Sum, t=None, Pass=None):
    Sum = float(Sum)
    if Pass == None and conf.conf['In'] and conf.conf['login'] == Address:
        t = time_time()
        lol = encode(PrivCode((get_UserOF(conf.conf['login'])['Balance']['SKR'][0][1]), conf.conf['PrivKey']), 16)
        Pass = decode(sha256_16(str(Sum) + str(t)), 256)
        Pass = PrivCode(Pass, lol)
    elif Pass == None and not (conf.conf['In'] and conf.conf['login'] == Address):
        return
    if Sum == 0:
        return
    if conf.conf['isServer']:
        kke = get_UserOF(Address)
        if not 'SKR' in kke['Balance']:
            return
        kke = get_User(kke['Balance']['SKR'][0][0], 'SKR')
        if kke['Time'] >= t:
            return
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        kke['Time'] = t
        c.execute(f'''UPDATE SKR SET Time = '{kke['Time']}' WHERE Address = '{kke['Address']}' ''')
        conn.commit()
        if Address in conf.conf['Voited']:
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
            Sum = min(Sum, kke['Balance'] - kke['Freez'])
            if Sum == 0:
                return
            kke['Freez'] += Sum
            conf.conf['FullFreez'] += Sum
        else:
            Sum = min(-1 * Sum, kke['Freez'])
            if Sum == 0:
                return
            kke['Freez'] -= Sum
            conf.conf['FullFreez'] -= Sum
        if (User.Check(kke, sha256_16(str(Sum) + str(t)), Pass)):
            c.execute(f'''UPDATE SKR SET Freez = '{kke['Freez']}' WHERE Address = '{kke['Address']}' ''')
            conn.commit()
        conn.close()
    Send_T1(SendTONODA_S(Address, Sum, t, Pass))


# [[PubKey1, PubKey2, Wal, Sum, PrivKey1, MesIn]]
def PreSendTranzh(lol):
    mas = {}
    res = 1
    TS = []
    for T in lol:
        if not T[2] in mas:
            mas[T[2]] = {}
        if not T[0] in mas[T[2]]:
            mas[T[2]][T[0]] = get_User(PubToAdr(T[0]), T[2])
        if not T[1] in mas[T[2]]:
            mas[T[2]][T[1]] = get_User(PubToAdr(T[1]), T[2])
        t = time_time()
        if len(T) == 8:
            Comis = T[7]
        else:
            Comis = conf.conf['Comis']
        print(str(T[0]))
        print(str(T[1]))
        print(T[2])
        print(str(T[3]))
        print(mas[T[2]][T[0]]['Hash'])
        print(mas[T[2]][T[1]]['Hash'])
        print(str(t))
        Pass = str(T[0]) + str(T[1]) + T[2] + str(T[3]) + mas[T[2]][T[0]]['Hash'] + mas[T[2]][T[1]]['Hash'] + str(t)
        Pass = sha256_16(Pass)
        print(Pass)
        T1 = Tranzh.Create(T[0], T[1], T[2], T[3], sha256_16(mas[T[2]][T[0]]['Hash'] + Pass),
                           sha256_16(mas[T[2]][T[1]]['Hash'] + Pass), Pass, t, PubCode(decode(T[5], 256), T[1]),
                           PubCode(decode(T[5], 256), T[0]), Comis)
        T1['Pass'] = PrivCode(decode(T1['Pass'], 256), T[4])
        if len(mas[T[2]][T[1]]['AddressTo'] ) > 0 and mas[T[2]][T[1]]['AddressTo']== mas[T[2]][T[0]]['AddressTo'] :
            mas[T[2]][T[1]]['Balance']      += T[3]
        else:
            mas[T[2]][T[1]]['Balance']      += T[3]*(1-Comis)
        mas[T[2]][T[0]]['Hash'] = T1['Hash1']
        mas[T[2]][T[1]]['Hash'] = T1['Hash2']
        TS.append(T1)
    return TS
    pass


def Ch_Tranzh(a, b):
    res = len(a['TS']) == len(b['TS'])
    res &= json.dumps(a['TS']) == json.dumps(b['TS'])
    return res


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
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        for T in x['TS']:
            c.execute(f'''INSERT INTO ATran VALUES(?, ?, ?, ?, ?, ?, ?)''', (
            PubToAdr(T['PubKey1']), PubToAdr(T['PubKey2']), T['Sum'], T['Comis'], T['Wal'], T['time'],
            get_User(PubToAdr(T['PubKey1']), T['Wal'])['AddressTo']))
            conn.commit()
        conn.close()
        tor = 1
    Send_T1(SendTranzh_S(x))
    if tor and conf.conf['isServer']:
        CheckerTranzh()
        pass


def GetUnUsedAddress(Wallet):
    if conf.conf['isServer']:
        while True:
            PrivKey = sha256_16(sha256_16(Generator(16)))
            conn = sql3connect(Path + '/exmp1.db')
            c = conn.cursor()
            c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{PubToAdr(PrivToPub(PrivKey))}' ''')
            if (c.fetchone() is None):
                conn.close()
                return PrivKey
        return PrivKey
    else:
        PrivKey = sha256_16(sha256_16(Generator(16)))
        while Send_T1(GetUnUsedAddress_S(PubToAdr(PrivToPub(PrivKey)), Wallet)) != '1':
            PrivKey = sha256_16(sha256_16(Generator(16)))
        return PrivKey


def get_User(Address, Wallet):
    if conf.conf['isServer']:
        kke = None
        Address = str(Address)
        Wallet = str(Wallet)
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        dat = c.execute(f'''SELECT * FROM {Wallet} WHERE Address = '{Address}' ''').fetchone()
        if not (dat is None):
            kke = User.FromSQL(dat)
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


def Registr(PubKey, Wallet, AddressTo='', FuncH='', Func='', AddressFrom=''):
    if Wallet in conf.conf['OtherWallets'] and AddressFrom == '':
        AddressFrom = RegistrOUT(Wallet, PubToAdr(PubKey))
    if conf.conf['isServer']:
        Address = PubToAdr(PubKey)
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{Address}' ''')
        if (c.fetchone() is None):
            conn.close()
            User.Create(Address, PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom)
        else:
            conn.close()
            return
    Send_T1(Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom))


def DelSUPERIP(ip):
    if not str(PubCode(int(ip), AdrToPub(conf.conf['Key']))) in conf.conf['SUPERIP']:
        return
    x = conf.conf['SUPERIP']
    x.remove(str(PubCode(int(ip), AdrToPub(conf.conf['Key']))))
    conf.conf['SUPERIP'] = x
    del x
    Send_T1(DelSUPERIP_S(ip))


def NewSUPERIP(ip):
    ip = str(ip)
    if ip in conf.conf['SUPERIP']:
        return
    x = conf.conf['SUPERIP']
    x.append(ip)
    conf.conf['SUPERIP'] = x
    del x
    Send_T1(NewSUPERIP_S(ip))


def getBalance_list(Wal, Addresses):  # exteranl Address
    if type(Addresses) is str:
        Addresses = [Addresses]
    if conf.conf['isServer']:
        dat = []
        for Address in Addresses:
            kke = get_User(Address, Wal)['Balance']
            if Wal in conf.conf['OtherWallets']:
                kke += getBalanceOUT(Wal, Address)
            dat.append(kke)
        return dat
    return Send_T1(getBalance_list_S(Wal, Addresses))


def getBalance(Wal, Address):  # exteranl Address
    if conf.conf['isServer']:
        kke = get_User(Address, Wal)['Balance']
        if Wal in conf.conf['OtherWallets']:
            kke += getBalanceOUT(Wal, Address)
        return kke
    return Send_T1(getBalance_S(Wal, Addresses))


def getATran(Wal, Address):  # exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        return c.execute(
            f''' SELECT * FROM ATran WHERE AddressFrom = '{Address}' AND Wallet = '{Wal}' ORDER BY Time DESC LIMIT 0, 50''').fetchall()
    return Send_T1(getATran_S(Wal, Address))


def getHTran(Wal, Address, t=None, ofPub=1):  # exteranl Address
    print(Wal, Address, t, ofPub)
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        dat = None
        if t == None:
            if (ofPub == 1):
                dat = c.execute(
                    f''' SELECT * FROM History WHERE (PubKey2 = '{Address}' OR PubKey1 = '{Address}') AND Wallet = '{Wal}' ORDER BY Time''').fetchall()
            else:
                dat = c.execute(
                    f''' SELECT * FROM History WHERE (Address1 = '{Address}' OR Address2 = '{Address}') AND Wallet = '{Wal}' ORDER BY Time''').fetchall()
        else:
            if (ofPub == 1):
                dat = c.execute(
                    f''' SELECT * FROM History WHERE (PubKey2 = '{Address}' OR PubKey1 = '{Address}') AND Wallet = '{Wal}' AND Time > {t} AND Wallet = '{Wal}' ORDER BY Time LIMIT 0, 50''').fetchall()
            else:
                dat = c.execute(
                    f''' SELECT * FROM History WHERE (Address1 = '{Address}' OR Address2 = '{Address}') AND Wallet = '{Wal}' AND Time > {t} AND Wallet = '{Wal}' ORDER BY Time LIMIT 0, 50''').fetchall()
        conn.close()
        return dat
    return Send_T1(getHTran_S(Wal, Address, t, ofPub))


def getAOrder(Wal, Address):  # exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        return c.execute(
            f''' SELECT * FROM Orders WHERE AddressFrom = '{Address}' AND Wallet1 = '{Wal}' ORDER BY t DESC LIMIT 0, 50 ''').fetchall()
    return Send_T1(getAOrder_S(Wal, Address))


def getHOrder(Wal, Address):  # exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        return c.execute(
            f''' SELECT * FROM Orders_H WHERE AddressFrom = '{Address}' AND Wallet1 = '{Wal}' ORDER BY t DESC LIMIT 0, 50 ''').fetchall()
    return Send_T1(getHOrder_S(Wal, Address))


def getDataForGraf(Wallet1, Wallet2, Time, lastTime):  # exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        Graf = []
        dat = c.execute(
            f'''SELECT k, t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wallet2}' AND t <= {Time}  AND t >= {Time - lastTime} ORDER BY t DESC''').fetchall()
        if len(dat) == 0:
            dat = c.execute(
                f'''SELECT k, t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wallet2}' AND t <= {Time} ORDER BY t DESC LIMIT 0, 1''').fetchall()
        conn.commit()
        conn.close()
        return dat
    return Send_T1(getDataForGraf_S(Wallet1, Wallet2, Time, lastTime))


def GetPricesF(Wallet1, data):  # exteranl Address
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        for Wal2 in data:
            try:
                ti = time_time();
                lol = c.execute(
                    f'''SELECT k, t FROM Orders_H WHERE Wallet1 == '{Wallet1}' AND Wallet2 == '{Wal2}' AND t <= {ti} ORDER BY t DESC LIMIT 0, 1''').fetchall()
                if len(lol) > 0:
                    data[Wal2] = float(lol[0][0])
                else:
                    data[Wal2] = -1
            except Exception as e:
                data[Wal2] = -1
        conn.commit()
        conn.close()
        return data
    return Send_T1(GetPricesF_S(Wallet1, data))


def PrivCode_list(dat):
    res = {}
    for arc in dat:
        res[str(arc[0]) + str(arc[1])] = PrivCode(decode(arc[0],256), arc[1])
    return res


def RegistrOUT(Wal, AddressTo):
    if not Wal in conf.conf['OtherWallets']:
        return
    if conf.conf['isSUPER']:
        Wal = Wal.lower()
        W = WebNet.WalleT(Wal, Generator(64), AddressTo)
        W.save()
        return W.Adr
    return Send_T1(RegistrOUT_S(Wal, AddressTo), Out=True)


def AddWalletOUT(Wallet, DataToConnect):
    if Wallet in conf.conf['OtherWallets']:
        return
    x = conf.conf['OtherWallets']
    x.append(Wallet)
    conf.conf['OtherWallets'] = x
    del x
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
                Address         varchar(128)     NOT NULL,
                AddressTo         varchar(128),
                PubKey             varchar(128)     NOT NULL,
                FuncH             varchar(128),
                Func             varchar(128),
                Time            Double,
                Freez            Double            NOT NULL,
                Balance            Double            NOT NULL,
                Hash            varchar(128)    NOT NULL,
                AddressFrom        varchar(128),
                Wallet             varchar(16)     NOT NULL
            ) ''')
        conn.commit()
        conn.close()
        WebNet.Wallet_Out(DataToConnect['Symbol'],
                          DataToConnect['Registr_API'],
                          DataToConnect['Registr_API_1'],
                          DataToConnect['Registr_API_R'],
                          DataToConnect['Registr_API_R_1'],
                          DataToConnect['Registr_API_R_2'],
                          DataToConnect['GetBalance_API'],
                          DataToConnect['GetBalance_API_1'],
                          DataToConnect['GetBalance_API_R'],
                          DataToConnect['GetBalance_API_R_1'],
                          DataToConnect['Send_API'],
                          DataToConnect['Send_API_1'],
                          DataToConnect['Send_API_2'],
                          DataToConnect['Send_API_3'],
                          DataToConnect['Send_API_4'],
                          DataToConnect['Send_API_R'],
                          DataToConnect['tcp_http'],
                          DataToConnect['http_reg'],
                          DataToConnect['http_bal'],
                          DataToConnect['http_sen'],
                          DataToConnect['tcp_address'],
                          DataToConnect['tcp_port'])
    Send_T1(AddWalletOUT_S(Wallet, DataToConnect))


def getBalanceOUT(Wal, Address):  # exteranl Address
    # if not Wal in conf.conf['OtherWallets']:
    #     return 'ERROR'
    if conf.conf['isSUPER']:
        Wal = Wal.lower()
        return WebNet.WalleT.getBalance(Address, Wal)
    return Send_T1(getBalanceOUT_S(Wal, Address), OUT=True)


def SendOUT_P1(Address, AddressTo, Sum, Wal):
    Wal = Wal.lower()
    if conf.conf['isSUPER']:
        k = WebNet.get_account(Address, Wal)
        k.Send(AddressTo, Sum)
        return True


def SendOUT_P(Address, AddressTo, Pass, Sum, Wal):
    Wal1 = Wal
    Wal = Wal.lower()
    if conf.conf['isSUPER']:
        k = WebNet.get_account(Address, Wal)
        kek = get_User(k['AddressTo'], Wal1)
        Pass1 = Address + AddressTo + str(Sum) + Wal
        if not kek.Check(Pass1, Pass):
            return False
        k.Send(AddressTo, Sum)
        T = Tranzh.Create(AdrToPub(k['AddressTo']), 'out:' + AddressTo, Wal, Sum, sha256_16(kek['Hash'] + Pass), '',
                          Pass, time_time(), MesIn='', MesOut='')
        # TranzhHistory(T)
        return True
    return Send_T1(SendOUT_P_S(Address, AddressTo, Pass, Sum, Wal1), OUT=True)


def GetDataToSendOUT(Sum, Wal):
    symbol = Wal.lower()
    if conf.conf['isSUPER']:
        dat = []
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        for row in c.execute(f'''SELECT * FROM {Wal} '''):
            kke = User.FromSQL(row)
            AddressOUT = kke['AddressFrom']
            Bal = float(WebNet.WalleT.getBalance(AddressOUT, symbol))
            if Bal > 0:
                x = min(Sum, Bal)
                Sum -= x
                dat.append(['', kke['PubKey'], Wal, x, '', ''])
            if Sum <= 0:
                break
        conn.close()
        return dat
    return Send_T1(GetDataToSendOUT_S(Sum, Wal), OUT=True)


conn = sql3connect(Path + '/exmp1.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS UserOF(
    Address         varchar(128)    NOT NULL,
    PubKey          varchar(128)    NOT NULL,
    Active          BOOL            NOT NULL,
    Masseges        Text            NOT NULL,
    Balance         Text            NOT NULL,
    Time            Double          NOT NULL,
    Photo            BLOB) ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS ATran(
    PubKey1            varchar(128)    NOT NULL,
    PubKey2            varchar(128)    NOT NULL,
    Sum                Double          NOT NULL,
    Comis              Double          NOT NULL,
    Wallet             varchar(16)     NOT NULL,
    Time               Double          NOT NULL,
    AddressFrom        varchar(128)    NOT NULL)
     ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS History(
    Num             int             NOT NULL,
    PubKey1         varchar(128)    NOT NULL,
    PubKey2         varchar(128)    NOT NULL,
    Sum             Double          NOT NULL,
    Comis           Double          NOT NULL,
    Wallet          varchar(16)     NOT NULL,
    Time            Double          NOT NULL,
    Address1        varchar(128)    NOT NULL,
    Address2        varchar(128)    NOT NULL,
    Comision        Text            NOT NULL,
    MesInsageIn     Text,
    MesInsageOut    Text
    ) ''')
conn.commit()
c.execute('''CREATE TABLE IF NOT EXISTS Orders(
    Address1        varchar(128)    NOT NULL,
    Address2        varchar(128)    NOT NULL,
    AddressFrom     varchar(128)    NOT NULL,
    Wallet1         varchar(16)        NOT NULL,
    Wallet2         varchar(16)        NOT NULL,
    Sum1            Double            NOT NULL,
    SumS            Double            NOT NULL,
    k               Double            NOT NULL,
    t               Double,
    t1              Double,
    priv            varchar(128)    NOT NULL) ''')
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
conn.commit()
# blobData = None
# with open(Path + '\\unnamed.jpg', 'rb') as file:
#     blobData = file.read()
# print(blobData)
# c.execute(f'''INSERT OR IGNORE INTO Users_Logo VALUES(?, ?)''',
#           ('StiveMan1',blobData))
# conn.commit()
conn.close()


class conf:
    conf = None


class User:
    def Create(Address='', PubKey='', Wallet='', AddressTo='', FuncH='', Func='',
               AddressFrom=''):  # AddressFrom - Other Wallets
        if FuncH != '' and Func != '' and AddressTo != '' and PubCode(FuncH, get_UserOF(AddressTo)['PubKey']) == Func:
            Func = FuncH
        else:
            Func = ''

        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''CREATE TABLE IF NOT EXISTS {Wallet}(
            Address         varchar(128)     NOT NULL,
            AddressTo         varchar(128),
            PubKey             varchar(128)     NOT NULL,
            FuncH             varchar(128),
            Func             varchar(128),
            Time            Double,
            Freez            Double            NOT NULL,
            Balance            Double            NOT NULL,
            Hash            varchar(128)    NOT NULL,
            AddressFrom        varchar(128),
            Wallet             varchar(16)     NOT NULL
            ) ''')
        conn.commit()
        c.execute(f'''SELECT Address FROM {Wallet} WHERE Address = '{Address}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO {Wallet} VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (Address, AddressTo, PubKey, str(FuncH), str(FuncH), 0, 0.0, 0.0, '', AddressFrom, Wallet))
        conn.commit()
        conn.close()

    def FromSQL(x):
        return {'Address': x[0], 'AddressTo': x[1], 'PubKey': x[2], 'FuncH': x[3], 'Func': x[4], 'Time': x[5],
                'Freez': x[6], 'Balance': x[7], 'Hash': x[8], 'AddressFrom': x[9], 'Wallet': x[10]}

    def ToSQL(x):
        return [x['Address'], x['AddressTo'], x['PubKey'], x['FuncH'], x['Func'], x['Time'], x['Freez'], x['Balance'],
                x['Hash'], x['AddressFrom'], x['Wallet']]

    def Check(AC, a, RES):
        a = decode(a, 256)
        RES = PubCode(RES, AC['PubKey'])
        return RES == a

    def ChangeFunc(AC, FuncH, Func):
        if (AC['AddressTo'] != ''):
            PubKey = get_UserOF(AC['AddressTo'])['PubKey']
            RES = PubCode(FuncH, PubKey)
            if RES == Func:
                conn = sql3connect(Path + '/exmp1.db')
                c = conn.cursor()
                c.execute(f'''UPDATE {AC['Wallet']} SET Func = '{FuncH}' WHERE Address = '{AC['Address']}' ''')
                conn.commit()
                conn.close()

    def getFunc(AC):
        if (AC['AddressTo'] != ''):
            PubKey = get_UserOF(AC['AddressTo'])['PubKey']
            return json.loads(encode(PubCode(AC['Func'], PubKey), 256))
            # return encode(PubCode(self['Func'], PubKey), 256)

    def CodeFunc(Func, PrivKey):
        Func = json.dumps(Func)
        Func1 = decode(Func, 256)
        return PrivCode(Func1, PrivKey), Func1


class Tranzh:
    def Create(PubKey1, PubKey2, Wal, Sum, Hash1, Hash2, Pass, time, MesIn='', MesOut='', Comis=None):
        x = {
            'PubKey1': PubKey1,
            'PubKey2': PubKey2,
            'Sum': Sum,
            'Wal': Wal,
            'Hash1': Hash1,
            'Hash2': Hash2,
            'Pass': Pass,
            'MesIn': MesIn,
            'MesOut': MesOut,
            'time': time,
            'Comision': []
        }
        if Comis == None or Comis < conf.conf['Comis']:
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
    def Create(TS, AddressTo=None, AddressHashed=None):
        x = {
            'TS': TS,
            'Users': [],
            'resTO': 0.0,
            'resAnti': 0.0,
            'AddressTo': AddressTo,
            'AddressHashed': AddressHashed
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
    def Create(Address='', PubKey=''):
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM UserOF WHERE Address = '{Address}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO UserOF VALUES(?, ?, ?, ?, ?, ?, ?)''',
                      (Address, PubKey, False, json.dumps([]), json.dumps({}), 0, None))
        conn.commit()
        conn.close()
        # return self

    def FromSQL(x):
        return {'Address': x[0], 'PubKey': x[1], 'Active': x[2], 'Masseges': json.loads(x[3]),
                'Balance': json.loads(x[4]), 'Time': x[5]}

    def ToSQL(x):
        return [x['Address'], x['PubKey'], x['Active'], json.dumps(x['Masseges']), json.dumps(x['Balance']), x['Time']]

    def Check(AC, a, RES):
        a = decode(a, 256)
        RES = PubCode(RES, AC['PubKey'])
        return RES == a


class Order:
    def Create(Adr1, Wal1, AddressFrom, Sum1, Adr2, Wal2, k, time, priv):
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(
            f'''SELECT * FROM Orders WHERE Wallet1 = '{Wal1}' AND Wallet2 = '{Wal2}' AND Address1 = '{Adr1}' AND AddressFrom = '{AddressFrom}' AND Address2 = '{Adr2}' AND SumS = '{Sum1}' AND k = '{k}' AND t = '{time}' AND priv = '{priv}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO Orders VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''',
                      (Adr1, Adr2, AddressFrom, Wal1, Wal2, Sum1, Sum1, k, time, time, priv))
        conn.commit()
        conn.close()

    def FromSQL(x):
        return {'Address1': x[0], 'Address2': x[1], 'AddressFrom': x[2], 'Wallet1': x[3], 'Wallet2': x[4], 'Sum1': x[5],
                'SumS': x[6], 'k': x[7], 't': x[8], 't1': x[9], 'priv': x[10]}

    def ToSQL(x):
        return [x['Address1'], x['Address2'], x['AddressFrom'], x['Wallet1'], x['Wallet2'], x['Sum1'], x['SumS'],
                x['k'], x['t'], x['t1'], x['priv']]


def get_conf():
    # pass
    conf.conf = getattr(conf.conf, '_conf', None)
    if conf.conf is None:
        conf.conf = shelve_open('conf')
    return conf


def PrivCode_list_S(dat):
    return {'Protocol': 'PrivCode_list', 'Data': dat}


def CheckVer_S():
    return {'Protocol': 'CheckVer'}


def UpDate_S(Ver):
    return {'Protocol': 'UpDate', 'Version': Ver}


def GetConf_S():
    return {'Protocol': 'GetConf'}


def VoteFor_S(Address, key, Pass):
    return {'Protocol': 'VoteFor', 'Address': Address, 'key': key, 'Pass': Pass}


def ChangeVoiting_S(new, newTiltel, newDidk):
    return {'Protocol': 'ChangeVoiting', 'new': new, 'newTiltel': newTiltel, 'newDidk': newDidk}


def UpdateVoiting_S():
    return {'Protocol': 'UpdateVoiting'}


def GetAllData_S():
    return {'Protocol': 'GetAllData'}


def CancelOrder_S(stk, Pass):
    return {'Protocol': 'CancelOrder', 'Stk': stk, 'Pass': Pass}


def SendOrder_S(Stk):
    return {'Protocol': 'SendOrder', 'Stk': Stk}


def get_Order_S(Wallet1, Wallet2, k):
    return {'Protocol': 'get_Order', 'Wallet1': Wallet1, 'Wallet2': Wallet2, 'k': k}


def ANConACC_S(Login, Wallet, AddressTo, Pass):
    return {'Protocol': 'ANConACC', 'Address': Login, 'Wallet': Wallet, 'AddressTo': AddressTo, 'Pass': Pass}


def CreateAccountS_S(Login, Hash):
    return {'Protocol': 'CreateAccountS', 'Login': Login, 'Hash': Hash}


def get_UserOF_S(Address):
    return {'Protocol': 'get_UserOF', 'Address': Address}


def IsServer_S(Address):
    return {'Protocol': 'IsServer', 'Address': Address}


def AddWallet_S(Wallet):
    return {'Protocol': 'AddWallet', 'Wallet': Wallet}


def ConACC_S(Address, Wallet, AddressTo, PrivKey):
    return {'Protocol': 'ConACC', 'Address': Address, 'Wallet': Wallet, 'AddressTo': AddressTo, 'PrivKey': PrivKey}


def DelIP_TCP_S(ip, Pass):
    return {'Protocol': 'DelIP_TCP', 'IP': ip, 'Pass': Pass}


def NewIP_TCP_S(ip, Pass):
    return {'Protocol': 'NewIP_TCP', 'IP': ip, 'Pass': Pass}


def DelIP_S(ip, Pass):
    return {'Protocol': 'DelIP', 'IP': ip, 'Pass': Pass}


def NewIP_S(ip, Pass):
    return {'Protocol': 'NewIP', 'IP': ip, 'Pass': Pass}


def Activate_S(Address):
    return {'Protocol': 'Activate', 'Address': Address}


def DisActivate_S(Address):
    return {'Protocol': 'DisActivate', 'Address': Address}


def ResTranzh_S(Address, Tranzh, res, Pass):
    return {'Protocol': 'ResTranzh', 'Address': Address, 'Tranzh': Tranzhs.ToJSON(Tranzh), 'res': res, 'Pass': Pass}


def SendTONODA_S(Address, Sum, time, Pass):
    return {'Protocol': 'SendTONODA', 'Address': Address, 'Sum': Sum, 'Time': time, 'Pass': Pass}


def SendTranzh_S(x):
    return {'Protocol': 'SendTranzh', 'Tranzh': x}


def GetUnUsedAddress_S(Address, Wallet):
    return {'Protocol': 'GetUnUsedAddress', 'Wallet': Wallet, 'Address': Address}


def get_User_S(Address, Wallet='SKR'):
    return {'Protocol': 'get_User', 'Wallet': Wallet, 'Address': Address}


def Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom):
    return {'Protocol': 'Registr', 'PubKey': PubKey, 'Wallet': Wallet, 'AddressTo': AddressTo, 'FuncH': FuncH,
            'Func': Func, 'AddressFrom': AddressFrom}


def RegistrOUT_S(Wallet, AddressTo):
    return {'Protocol': 'RegistrOUT', 'Wallet': Wallet, 'AddressTo': AddressTo}


def DelSUPERIP_S(ip):
    return {'Protocol': 'DelSUPERIP', 'IP': ip}


def NewSUPERIP_S(ip):
    return {'Protocol': 'NewSUPERIP', 'IP': ip}


def AddWalletOUT_S(Wallet, DataToConnect):
    return {'Protocol': 'AddWalletOUT', 'Wallet': Wallet, 'DataToConnect': DataToConnect}


def getBalanceOUT_S(Wallet, Address):
    return {'Protocol': 'getBalanceOUT', 'Address': Address, 'Wallet': Wallet}


def SendOUT_P_S(Address, AddressTo, Pass, Sum, Wallet):
    return {'Protocol': 'SendOUT_P', 'Address': Address, 'AddressTo': AddressTo, 'Pass': Pass, 'Sum': Sum,
            'Wallet': Wallet}


def GetDataToSendOUT_S(Sum, Wallet):
    return {'Protocol': 'GetDataToSendOUT', 'Wallet': Wallet, 'Sum': Sum}


def getBalance_S(Wallet, Address):
    return {'Protocol': 'getBalance', 'Wallet': Wallet, 'Address': Address}


def getBalance_list_S(Wallet, Addresses):
    return {'Protocol': 'getBalance_list', 'Wallet': Wallet, 'Addresses': Addresses}


def getATran_S(Wallet, Address):
    return {'Protocol': 'getATran', 'Wallet': Wallet, 'Address': Address}


def getHTran_S(Wal, Address, t=None, ofPub=1):
    return {'Protocol': 'getHTran', 'Wallet': Wal, 'Address': Address, 'Time': t, 'ofPub': ofPub}


def getAOrder_S(Wallet, Address):
    return {'Protocol': 'getAOrder', 'Wallet': Wallet, 'Address': Address}


def getHOrder_S(Wallet, Address):
    return {'Protocol': 'getHOrder', 'Wallet': Wallet, 'Address': Address}


def getDataForGraf_S(Wallet1, Wallet2, Time, lastTime):
    return {'Protocol': 'getDataForGraf', 'Wallet1': Wallet1, 'Wallet2': Wallet2, 'Time': Time, 'lastTime': lastTime}


def GetPricesF_S(Wallet1, data):
    return {'Protocol': 'GetPricesF', 'Wallet1': Wallet1, 'data': data}


def PrivCode_list_R(dat):
    return PrivCode_list(dat['Data'])


def generate_Private_R(dat):
    return generate_Private(dat['Password'])


def PubToAdr_R(dat):
    return PubToAdr(dat['Public'])


def AdrToPub_R(dat):
    return AdrToPub(dat['Address'])


def PrivToPub_R(dat):
    return PrivToPub(dat['Password'])


def PubCode_R(dat):
    return str(PubCode(dat['Message'], dat['Public_key']))


def PrivCode_R(dat):
    return str(PrivCode(dat['Message'], dat['Public_key']))


def CheckVer_R(dat):
    return Version


def UpDate_R(dat):
    if dat['Version'] != conf.conf['Version']:
        conf.conf['Version'] = dat['Version']
        UpDate(dat['Version'])
        conf.conf['ExitCode'] = 82
        conf.conf.close()
        os._exit(82)
        # ReBorn()


def GetConf_R(dat):
    return {"Data": [
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
        conf.conf['Voited'],
        conf.conf['VoitingTime'],
        conf.conf['VoitingTitle'],
        conf.conf['VoitingDescription'],

        conf.conf['Connected_TCP'],
        conf.conf['SUPERIP_TCP']
    ]}


def VoteFor_R(dat):
    VoteFor(dat['key'], dat['Address'], dat['Pass'])


def ChangeVoiting_R(dat):
    ChangeVoiting(dat['new'], dat['newTiltel'], dat['newDidk'])


def UpdateVoiting_R(dat):
    return conf.conf['Voiting']


def GetAllData_R(dat):
    dat = {}
    print(Path + '/exmp1.db')
    with open(Path + '/exmp1.db', 'rb') as input:
        print('Sakaar/exmp1.db')
        dat['Sakaar/exmp1.db'] = str(b64encode(input.read()), 'utf-8', errors='ignore').strip()
    # print(dat)
    return dat


def CancelOrder_R(dat):
    CancelOrder(dat['Stk'], dat['Pass'])


def SendOrder_R(dat):
    SendOrder(dat['Stk'])


def get_Order_R(dat):
    # print('get_Order')
    return get_Order(dat['Wallet1'], dat['Wallet2'], dat['k'])


def ANConACC_R(dat):
    ANConACC(dat['Address'], dat['Wallet'], dat['AddressTo'], dat['Pass'])


def CreateAccountS_R(dat):
    CreateAccountS(dat['Login'], dat['Hash'])


def get_UserOF_R(dat):
    return get_UserOF(dat['Address'])


def IsServer_R(dat):
    return IsServer(dat['Address'])


def AddWallet_R(dat):
    AddWallet(dat['Wallet'])


def ConACC_R(dat):
    ConACC(dat['Address'], dat['Wallet'], dat['AddressTo'], dat['PrivKey'])


def DelIP_R(dat):
    DelIP(dat['IP'], dat['Pass'])


def NewIP_R(dat):
    NewIP(dat['IP'], dat['Pass'])


def DelIP_TCP_R(dat):
    DelIP_TCP(dat['IP'], dat['Pass'])


def NewIP_TCP_R(dat):
    NewIP_TCP(dat['IP'], dat['Pass'])


def Activate_R(dat):
    Activate(dat['Address'])


def DisActivate_R(dat):
    DisActivate(dat['Address'])


def ResTranzh_R(dat):
    ResTranzh(dat['Address'], Tranzhs.FromJSON(dat['Tranzh']), dat['res'], dat['Pass'])


def SendTONODA_R(dat):
    SendTONODA(dat['Address'], dat['Sum'], dat['Time'], dat['Pass'])


def SendTranzh_R(dat):
    SendTranzh(dat['Tranzh'])


def GetUnUsedAddress_R(dat):
    if conf.conf['isServer']:
        conn = sql3connect(Path + '/exmp1.db')
        c = conn.cursor()
        c.execute(f'''SELECT Address FROM {dat['Wallet']} WHERE Address = '{dat['Address']}' ''')
        tor = ''
        if (c.fetchone() is None):
            tor = '1'
        else:
            tor = '0'
        conn.close()
        return tor


def get_User_R(dat):
    return get_User(dat['Address'], dat['Wallet'])


def Registr_R(dat):
    Registr(dat['PubKey'], dat['Wallet'], dat['AddressTo'], dat['FuncH'], dat['Func'], dat['AddressFrom'])


def RegistrOUT_R(dat):
    return RegistrOUT(dat['Wallet'], dat['AddressTo'])


def DelSUPERIP_R(dat):
    DelSUPERIP(dat['IP'])


def NewSUPERIP_R(dat):
    NewSUPERIP(dat['IP'])


def AddWalletOUT_R(dat):
    AddWalletOUT(dat['Wallet'], dat['DataToConnect'])


def getBalanceOUT_R(dat):
    return getBalanceOUT(dat['Wallet'], dat['Address'])


def SendOUT_P_R(sock, dat):
    return SendOUT_P(dat['Address'], dat['AddressTo'], dat['Pass'], dat['Sum'], dat['Wallet'])


def GetDataToSendOUT_R(dat):
    return GetDataToSendOUT(dat['Sum'], dat['Wallet'])


def getBalance_R(dat):
    return getBalance(dat['Wallet'], dat['Address'])


def getBalance_list_R(dat):
    return getBalance_list(dat['Wallet'], dat['Addresses'])


def getATran_R(dat):
    return getATran(dat['Wallet'], dat['Address'])


def getHTran_R(dat):
    return getHTran(dat['Wallet'], dat['Address'], dat['Time'], dat['ofPub'])


def getAOrder_R(dat):
    return getAOrder(dat['Wallet'], dat['Address'])


def getHOrder_R(dat):
    return getHOrder(dat['Wallet'], dat['Address'])


def getDataForGraf_R(dat):
    return getDataForGraf(dat['Wallet1'], dat['Wallet2'], dat['Time'], dat['lastTime'])


def GetPricesF_R(dat):
    return GetPricesF(dat['Wallet1'], dat['data'])


Functions_R_res = {
    'Registr': Registr_R,
    'getAOrder': getAOrder_R,
    'getHOrder': getHOrder_R,
    'get_User': get_User_R,
    'GetUnUsedAddress': GetUnUsedAddress_R,
    'get_UserOF': get_UserOF_R,
    'IsServer': IsServer_R,
    'UpdateVoiting': UpdateVoiting_R,
    'GetConf': GetConf_R,
    'CheckVer': CheckVer_R,
    'GetAllData': GetAllData_R,
    'RegistrOUT': RegistrOUT_R,
    'get_Order': get_Order_R,
    'getBalanceOUT': getBalanceOUT_R,
    'SendOUT_P': SendOUT_P_R,
    'GetDataToSendOUT': GetDataToSendOUT_R,
    'getBalance': getBalance_R,
    'getBalance_list': getBalance_list_R,
    'getATran': getATran_R,
    'getHTran': getHTran_R,
    'GetPricesF': GetPricesF_R,
    'getDataForGraf': getDataForGraf_R,
    'generate_Private': generate_Private_R,
    'PubToAdr': PubToAdr_R,
    'AdrToPub': AdrToPub_R,
    'PrivToPub': PrivToPub_R,
    'PubCode': PubCode_R,
    'PrivCode': PrivCode_R,
    'PrivCode_list': PrivCode_list_R,
}
Functions_R = {
    'SendTranzh': SendTranzh_R,
    'SendTONODA': SendTONODA_R,
    'ResTranzh': ResTranzh_R,
    'CreateAccountS': CreateAccountS_R,
    'ConACC': ConACC_R,
    'ANConACC': ANConACC_R,
    'Activate': Activate_R,
    'DelIP': DelIP_R,
    'NewIP': NewIP_R,
    'DelIP_TCP': DelIP_TCP_R,
    'NewIP_TCP': NewIP_TCP_R,
    'DisActivate': DisActivate_R,
    'ChangeVoiting': ChangeVoiting_R,
    'VoteFor': VoteFor_R,
    'UpDate': UpDate_R,
    'SendOrder': SendOrder_R,
    'AddWallet': AddWallet_R,
    'CancelOrder': CancelOrder_R,
    'NewSUPERIP': NewSUPERIP_R,
    'DelSUPERIP': DelSUPERIP_R,
    'AddWalletOUT': AddWalletOUT_R
}

get_conf()
# 4a9fb18ec3bf.ngrok.io
if 'HTTP_TCP' not in conf.conf:
    conf.conf['HTTP_TCP'] = None
if 'Connected' not in conf.conf:
    conf.conf['Connected'] = [['127.0.0.1:10101', 'GrandBull']]
if 'Connected_TCP' not in conf.conf:
    conf.conf['Connected_TCP'] = [['4.tcp.ngrok.io', 11602, 'GrandBull']]
if 'SUPERIP' not in conf.conf:
    conf.conf['SUPERIP'] = []
if 'SUPERIP_TCP' not in conf.conf:
    conf.conf['SUPERIP_TCP'] = []
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
if conf.conf['isSUPER'] == False:
    if not ('MyIP' not in conf.conf or conf.conf['MyIP'] is None):
        DelIP(conf.conf['MyIP'])
    conf.conf['MyIP'] = None
    if not ('MyIP_TCP' not in conf.conf or conf.conf['MyIP_TCP'] is None):
        DelIP(conf.conf['MyIP_TCP'])
    conf.conf['MyIP_TCP'] = None
if 'Key' not in conf.conf:
    conf.conf[
        'Key'] = 'AAAAgQCVyHesUOzUjebFgOfNy9kc0EfqmU8FJotUt4eO9JtdZ8pwBst0jx/p4Pcve/10zWCjYEQ5Iy/I37s30KjmKz0DiehxFJ79Mq8L8oDfY3i6uPOIk9kONeLYoovLjn/jUVYwfwYNJeNp6Q+bnqQkaTv+vAKECyoK3k0ThsURzkrUWw=='
if 'VoitingTime' not in conf.conf:
    conf.conf['VoitingTime'] = 0
if 'VoitingDescription' not in conf.conf:
    conf.conf['VoitingDescription'] = ""
if 'VoitingTitle' not in conf.conf:
    conf.conf['VoitingTitle'] = ""

CheckVer()
# DelIP('a3269702d87f.ngrok.io')
