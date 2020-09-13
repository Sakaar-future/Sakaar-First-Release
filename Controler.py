from Sakaar import *
if __name__ == '__main__':
    Start()
    GetConf()
    while(True):
        get_conf
        login = conf.conf['login']
        x = input(f'Sakaar/{ login }/# ')
        if x == 'Send':
            Wal =     input('Wallet       : ')
            AdrFrom =     input('Address From : ')
            pubto = input('Address To   : ')
            Sum =     input('Sum          : ')
            MesIn =     input('MesInsage      : ')
            x = get_UserOF(conf.conf['login'])['Balance'][Wal]
            for i in x:
                if AdrFrom == i[0]:
                    print ('Finded Account')
                    PrivKey = (PrivCode(i[1], conf.conf['PrivKey'] ))
                    PrivKey = encode(PrivKey, 16)
                    SendTranzh(Tranzhs.Create(PreSendTranzh([[AdrToPub(i[0]), AdrToPub(pubto), Wal, float(Sum), PrivKey,MesIn]])))
        elif x == 'SendL':
            Wal =         input('Wallet    : ')
            PrivKey =     input('PrivatKey : ')
            pubto =     input('Address To: ')
            Sum =         input('Wallet    : ')
            MesIn =         input('MesInsage   : ')
            SendTranzh(Tranzhs.Create(PreSendTranzh([[PrivToPub(PrivKey), AdrToPub(pubto), Wal, float(Sum), PrivKey,MesIn]])))
        elif x == 'MakeOrder':
            Wal1 = input('Wallet1  : ')
            Pub1 = input('Address1 : ')
            Wal2 = input('Wallet2  : ')
            Pub2 = input('Address2 : ')
            Sum =  input(f'Sum ({Wal1}) : ')
            k =  input(f'Koeficent ({Wal1}/{Wal2}) : ')
            MakeOrder(Pub1, Wal1, float(Sum), Pub2, Wal2, float(k))
        elif x == 'Balance':
            x = get_UserOF(conf.conf['login'])['Balance']
            for Wal in x:
                print(Wal)
                for kke in x[Wal]:
                    print (kke[0],get_User(kke[0],Wal)['Balance'])
        elif x == 'BalanceOF':
            logi = input('Login : ')
            x = get_UserOF(logi)['Balance']
            for Wal in x:
                print(Wal)
                for kke in x[Wal]:
                    print (kke[0],get_User(kke[0],Wal)['Balance'])
        elif x == 'RegistrNewWallet':
            print (conf.conf['OurWallets'])
            print (conf.conf['OtherWallets'])
            Wal = input('Wallet : ')
            RegistrNewWallet(Wal)
        elif x == 'Login':
            log =     input('Login    : ')
            Passw = input('Password : ')
            Login(log, Passw)
        elif x == 'Out':
            LogOut()
        elif x == 'Registr':
            log = input('Login     : ')
            Passw = input('Password : ')
            CreateAccount(log,Passw)
        elif x == 'History':
            Address =     input('Address : ')
            Wal =         input('Wallet  : ')
            for i in getHTran(Wal, Address):
                print (i[0],i[1],i[2],i[3])
        elif x == 'ActiveTran':
            Address =     input('Login : ')
            Wal =         input('Wallet  : ')
            for i in getATran(Wal, Address):
                print (i[0],i[1],i[2])
        elif x == 'ActiveOrders':
            Wal1 =     input('Wallet1 : ')
            Wal2 =     input('Wallet2 : ')
            for row in get_Order(Wal1, Wal2):
                row = Order.FromSQL(row)
                print (row['AddressFrom'],row['Sum1'],row['k'])
        elif x == 'SendToNoda':
            Sum = input('Sum : ')
            if conf.conf['In']:
                SendTONODA(conf.conf['login'], float(Sum))
        elif x == 'Massages':
            if conf.conf['In']:
                x = get_UserOF(conf.conf['login'])['Balance']
                for Wal in x:
                    print(Wal)
                    for kke in x[Wal]:
                        dat = getHTran(Wal,kke[0])
                        priv = encode(PrivCode(kke[1], conf.conf['PrivKey'] ), 16)
                        for i in dat:
                            print (get_User(PubToAdr(i[1]),Wal)['AddressTo'],encode(PrivCode(i[9], priv), 256),i[6])
        elif x == 'AddMyIP':
            AddMyIP()
        elif x == 'DeleteIP':
            DeleteIP()
        elif x == 'DeleteSUPERIP':
            ip = '10001'
            ip = PrivCode(decode(ip,256),sha256_16('StiveMan1'))
            ip = PrivCode(ip,sha256_16('StiveMan1'))
            DelSUPERIP(ip)
        elif x == 'AddMySUPERIP':
            ip = '10001'
            ip = PrivCode(decode(ip,256),sha256_16('StiveMan1'))
            NewSUPERIP(ip)
        elif x == 'BecomeNODA':
            BecomNODA()
        elif x == 'CloseNODA':
            CloseNODA()
        elif x == 'CheckVer':
            CheckVer()
        elif x == 'AddWallet':
            Wal = input('Wallet : ')
            AddWalletOUT(Wal)
        elif x == 'DeleteWallet':
            Wal =         input('Wallet  : ')
            Address =     input('Address : ')
            ANConACC(conf.conf['login'], Wal, Address)
        elif x == 'ShowVoiting':
            print (conf.conf['FullFreez'])
            for i in conf.conf['Voiting']:
                print (i,type(i),conf.conf['Voiting'][i][0]/conf.conf['FullFreez'],conf.conf['Voiting'][i][1])
            print(conf.conf['Voited'].keys())
        elif x == 'VoteFor':
            key = input('Key : ')
            print(conf.conf['Voiting'][key])
            VoteFor(key)
        elif x == 'ChangeVoiting':
            num = int(input('Num : '))
            dat = {}
            key = 0
            while key < num:
                dat[str(key)] = [0.0,'']

                dat[str(key)][1] = input('Statment : ')
                key  += 1
            print(dat)
            ChangeVoiting(dat)
        elif x == 'getAOrder':
            Wal =         input('Wallet  : ')
            Address =     input('Address : ')
            print(getAOrder(Wal,Address))
        elif x == 'CancelOrder':
            x = get_UserOF(conf.conf['login'])['Balance']
            dat = []
            for Wal in x:
                for kke in x[Wal]:
                    kke = get_User(kke[0],Wal)
                    if kke['Func'] != '':
                        dat.append(User.getFunc(kke))
            i = 0
            for j in dat:
                print (i,j)
                i+=1
            key = input('Key : ')
            CancelOrder(dat[int(key)])
        elif x == 'NewSUPERIP':

        # elif x == 'MakeNoda':
        #     Sum = input('Sum : ')
        #     SendTONODA(conf.conf['login'], Sum, time_time(), '', type = 0)
            lol = ''
