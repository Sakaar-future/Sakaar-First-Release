from Sakaar import *
#Crypto Test
def Test_1():
    Key = PubToAdr(PrivToPub(sha256_16('lol')))
    return PrivToPub(sha256_16('lol')) == AdrToPub(Key) and encode(PrivCode(PubCode(decode('hello',256),PrivToPub('lol')),'lol'),256) == 'hello'
#Tranzhaction Test
def Test_2():
    Priv1 = GetUnUsedAddress('SKR')
    Priv2 = GetUnUsedAddress('SKR')
    Registr(PrivToPub(Priv1), 'SKR')
    Registr(PrivToPub(Priv2), 'SKR')
    conn = sql3connect('Sakaar/exmp1.db')
    c = conn.cursor()
    c.execute(f'''UPDATE SKR SET Balance=2000 WHERE Address = '{PubToAdr(PrivToPub(Priv1))}' ''')
    conn.commit()
    conn.close()
    tor = get_User(PubToAdr(PrivToPub(Priv1)),'SKR')['Balance'] == 2000
    tor &= get_User(PubToAdr(PrivToPub(Priv2)),'SKR')['Balance'] == 0
    SendTranzh(Tranzhs.Create(PreSendTranzh([[PrivToPub(Priv1), PrivToPub(Priv2), 'SKR', 1000, Priv1,''],[PrivToPub(Priv1), PrivToPub(Priv2), 'SKR', 1000, Priv1,'']])))
    time_sleep(3)
    tor &= get_User(PubToAdr(PrivToPub(Priv1)),'SKR')['Balance'] == 0
    tor &= get_User(PubToAdr(PrivToPub(Priv2)),'SKR')['Balance'] == 1998
    return tor
#Order swap test
def Test_3():
    Login1 = Password1 = 'S1'
    Login2 = Password2 = 'S2'
    # print(Login1)
    # x = get_UserOF(Login1)['Balance']
    # for Wal in x:
    #     print(Wal)
    #     for kke in x[Wal]:
    #         print (kke[0][:10],get_User(kke[0],Wal)['Balance'])
    # print()
    # print(Login2)
    # x = get_UserOF(Login2)['Balance']
    # for Wal in x:
    #     print(Wal)
    #     for kke in x[Wal]:
    #         print (kke[0][:10],get_User(kke[0],Wal)['Balance'])
    # print()

    LogOut()
    Login(Login1,Password1)
    time_sleep(3)
    kke1 = get_UserOF(Login1)
    MakeOrder(kke1['Balance']['SKR1'][0][0],'SKR1',2000,kke1['Balance']['SKR2'][0][0],'SKR2',1)
    time_sleep(3)

    LogOut()
    Login(Login2,Password2)
    time_sleep(3)
    kke1 = get_UserOF(Login2)
    MakeOrder(kke1['Balance']['SKR2'][0][0],'SKR2',2000,kke1['Balance']['SKR1'][0][0],'SKR1',1)

    time_sleep(6)
    print(Login1)
    x = get_UserOF(Login1)['Balance']
    for Wal in x:
        print(Wal)
        for kke in x[Wal]:
            print (kke[0][:10],get_User(kke[0],Wal)['Balance'])
    print()
    print(Login2)
    x = get_UserOF(Login2)['Balance']
    for Wal in x:
        print(Wal)
        for kke in x[Wal]:
            print (kke[0][:10],get_User(kke[0],Wal)['Balance'])
    print()
# getHOrder('0rnxLgMiv0',"SKR1");
print ('Tset_1',Test_1())
# print ('Tset_2',Test_2())
print ('Tset_3',Test_3())
#Order Remove Test

#
