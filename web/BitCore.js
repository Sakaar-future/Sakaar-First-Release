// from .Cripto import *
// import os,json
// from time import time as time_time, sleep as time_sleep
// from random import randint
// from sqlite3 import connect as sql3connect
// from shelve import open as shelve_open
// from requests import post as requests_post
// from flask import Flask, g, request, jsonify
// from base64 import b64decode, b64encode
// from pyngrok import ngrok



var conf = {}

if (!('MyIP' in conf)){
    conf['MyIP'] = null;
}
if (!('Connected' in conf)){
    conf['Connected'] = ['127.0.0.1:10101'];
}
if (!('SUPERIP' in conf)){
    conf['SUPERIP'] = ['3300945b1410.ngrok.io'];
}
if (!('OurWallets' in conf)){
    conf['OurWallets'] = [];
}
if (!('OtherWallets' in conf)){
    conf['OtherWallets'] = [];
}
if (!('InMemory' in conf)){
    conf['InMemory'] = [];
}
if (!('FullFreez' in conf)){
    conf['FullFreez'] = 0.0;
}
if (!('Comis' in conf)){
    conf['Comis'] = 0.001;
}
if (!('Voiting' in conf)){
    conf['Voiting'] = {};
}
if (!('Voited' in conf)){
    conf['Voited'] = {};
}
if (!('Version' in conf)){
    conf['Version'] = '1.000';
}

if (!('Link' in conf)){
    conf['Link'] = 'DB';
}
if (!('isServer' in conf)){
    conf['isServer'] = false;
}
if (!('isSUPER' in conf)){
    conf['isSUPER'] = false;
}
if (!('In' in conf)){
    conf['In'] = true;
}
if (!('login' in conf)){
    conf['login'] = 'StiveMan1';
}
if (!('PrivKey' in conf)){
    conf['PrivKey'] = 'b913cb344c15f753ed238c50f1bcb24493ef3e8e7b8cb28586b780d620b10c1e';
}
if (!('passw' in conf)){
    conf['passw'] = '5feceb66ffc86f38d952786c6d696c79c2dbc239dd4e91b46729d73a27fb57e9';
}
if (!('isRunning' in conf)){
    conf['isRunning'] = false;
}
if (!('Block' in conf)){
    conf['Block'] = 0;
}
if (!('MyIP' in conf)){
    conf['MyIP'] = null;
}

function getRandomInt(max) {
         return Math.floor(Math.random() * Math.floor(max));
}

function Generator(size){
    size = parseInt(size);
    fro = 'qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM';
    res = '';
    for (let i =0 ;i<size;i++){
        lol = getRandomInt(len(fro));
        res += fro[lol%len(fro)];
    }
    return res;
}
function Server_Ent(){
    conf['isRunning'] = true;
    app.run(host= '127.0.0.1',port = 10101);
}
async function Send_T1(dat,OUT = false){
    if (OUT == false){
        for (let ip of conf['Connected']){
            try{
                res = await postData('https://' + String(ip)+ '/', data = dat);
                if (res != null){
                    return res;
                }
            }catch(e){
                return null;
            }
        }
    }else{
        for (let ip of conf['SUPERIP']){
            try{
                res = await postData('http://' + String(ip)+ '/', data = dat);
                if (res != null){
                    return res;
                }
            }catch(e){
                return null;
            }
        }
    }
}
async function postData(url = "", data = {}) {
    var myHeaders = new Headers();
    myHeaders.append("Content-Type", "application/json");

    var raw = JSON.stringify(data);

    var requestOptions = {
             method: 'POST',
             headers: myHeaders,
             body: raw,
             redirect: 'follow'
    };

    const lol =         await fetch("http://ae735302b39d.ngrok.io", requestOptions)
             .then(response => response.json())
    return lol
}
GetConf();
function End(tor = true){
    if (conf['isRunning']){
        CloseNODA();
    }
}
function Start(){
    if (conf['isRunning']){
        BecomNODA();
    }
}
function LogOut(){
    conf['login']                 = '';
    conf['passw']                 = '';
    conf['PrivKey']             = '';
    conf['PubKey']             = '';
    conf['In']                 = false;
}
function RegistrNewWallet(Wallet){
    if (conf['In']){
        PrivKey = GetUnUsedAddress(Wallet);
        // print ('lll', PrivKey)
        PubKey = PrivToPub(PrivKey);
        RegiString(PubKey, Wallet, conf['login']);
        PrivKey = decode(PrivKey, 16);
        PrivKey = (PubCode(PrivKey, conf['PubKey'] ));
        time_sleep(0.5);
        ConACC(conf['login'], Wallet, PubToAdr(PubKey), PrivKey);
        return encode(PrivKey, 16);
    }
}
function SendOUT(Wal, Address, AddressTo, Sum){//Using our Address system && external Address To
    if (conf['In']){
        kek = get_UserOF(conf['login'])['Balance'] [Wal];
        lol = null;
        i = 0;
        while (i < len(kek)){
            if (kek[i][0]== Address){
                lol = kek[i][1];
                break;
            }
        }
        if(lol== null){
            return;
        }
        kke = get_User(Address, Wal);
        BOut = getBalanceOUT(Wal, kke['AddressFrom'] );
        x = min(float(BOut), Sum);

        lol = PrivCode(lol, conf['PrivKey']);
        lol = encode(lol, 16);
        SendOUT_P(kke['AddressFrom'] , AddressTo, PrivCode(decode(kke['AddressFrom'] + AddressTo + String(x) + Wal, 256), lol), x, Wal);

        Sum -= x;
        if (Sum<=0){
            return;
        }
            // lol = decode(lol, 16)

        dat = GetDataToSendOUT(Sum, Wal);
        i = 0;
        while (i < len(dat)){
            dat[i][0] = kke['PubKey'];
            dat[i][4] = lol;
            i += 1;
        }

        SendTranzh(Tranzhs.Create(PreSendTranzh(dat), AddressTo, PrivCode(decode(kke['AddressFrom'] + AddressTo + String(Sum) + Wal, 256), lol) ));
    }
}
function CheckVer(){
    if (Send_T1(CheckVer_S()) != conf['Version']){
        GetUpDate();
    }
}
function UpDate(Ver){
    Send_T1(UpDate_S(Ver));
}
async function GetConf(){
    dat = await Send_T1(GetConf_S());
    dat = dat['Data']
    conf['Version'] = dat[0];
    conf['Connected'] = dat[1];
    conf['SUPERIP'] = dat[2];
    conf['OurWallets'] = dat[3];
    conf['OtherWallets'] = dat[4]
    conf['InMemory'] = dat[5];
    conf['FullFreez'] = dat[6];
    conf['Block'] = dat[7];
    conf['Comis'] = dat[8];
    conf['Voiting'] = dat[9];
    conf['Voited'] = dat[10];
}
function VoteFor(key,Address = null,Pass = null){
    if (Pass == null && conf['In']){
        Address = conf['login'];
        Pass = PrivCode(decode(key,256),conf['PrivKey']);
    }else if(!conf['In']){
        return
    }
    Send_T1(VoteFor_S(Address, key, Pass))
}
function ChangeVoiting(New){
    if (conf['Voiting'] != New){
        conf['Voited'] = {};
        conf['Voiting'] = New;
    }else{
        return;
    }
    Send_T1(ChangeVoiting_S(New));
}
function UpdateVoiting(){
    conf['Voiting'] = Send_T1(GetVoiting_S());
    return;
}
function CancelOrder(stk,Pass = null){
    if (Pass == null && conf['In'] && conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo']){
        Pass = PrivCode(decode(String(stk),256),conf['PrivKey']);
        SendTranzh(Tranzhs.Create(PreSendTranzh([[PrivToPub(stk['priv']), AdrToPub(get_UserOF(conf['login'])['Balance'] [stk['Wallet1']][0][0]), stk['Wallet1'], stk['Sum1'], stk['priv'], '']])));
    }else if (Pass == null &&         !(conf['In'] && conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo'])){
        return;
    }
    Send_T1(CancelOrder_S(stk,Pass));
}
function MakeOrder(Adr1, Wal1, Sum1, Adr2, Wal2, k){
    if (conf['In']){
        // print ('MakeOrder')

        Priv = null;
        usr1 = get_UserOF(conf['login']);
        for (let pop of usr1['Balance'] [Wal1]){
            if(pop[0]== Adr1){
                Priv = encode(PrivCode(pop[1], conf['PrivKey']), 16);
            }
        }
        if (Priv== null ){
            return
        }

        function COOL(TS){
            res = 1;
            mas = {};
            tor = 0;
            stk = null;
            for(let T of TS){
                if (!(T['Wal'] in mas)){
                    mas[T['Wal']] = {};
                }
                if (!(T['PubKey1'] in mas[T['Wal']])){
                    mas[T['Wal']][T['PubKey1'] ] = get_User(PubToAdr(T['PubKey1'] ), T['Wal']);
                    if (mas[T['Wal']][T['PubKey1'] ]['Func'] != ''){
                        if(tor== 1){
                            res = 0;
                            break;
                        }
                        tor = 1;
                        stk = User.getFunc(mas[T['Wal']][T['PubKey1']]);
                    }
                }
                if (!(T['PubKey2'] in mas[T['Wal']])){
                    mas[T['Wal']][T['PubKey2'] ] = get_User(PubToAdr(T['PubKey2'] ), T['Wal']);
                }
                res &= Checker(T, mas[T['Wal']][T['PubKey1'] ], mas[T['Wal']][T['PubKey2'] ]);
                mas[T['Wal']][T['PubKey1'] ]['Balance'] -= T['Sum'];
                if (len(mas[T['Wal']][T['PubKey2'] ]['AddressTo'] ) > 0 && mas[T['Wal']][T['PubKey2'] ]['AddressTo']== mas[T['Wal']][T['PubKey1'] ]['AddressTo'] ){
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'];
                }else{
                    mas[T['Wal']][T['PubKey2'] ]['Balance'] += T['Sum'] *(1-T['Comis']);
                }
                mas[T['Wal']][T['PubKey1'] ]['Hash'] = T['Hash1'];
                mas[T['Wal']][T['PubKey2'] ]['Hash'] = T['Hash2'];
            }
            res = res && (tor != 1 || Func(mas, TS, stk));
            print(res ,(tor != 1 || Func(mas, TS, stk)));
            return res;
        }

        dat = get_Order(Wal2,Wal1,1/k)
        // print (dat)
        for (let row of dat){

            row = Order.FromSQL(row);

            usr02 = get_User(row['Address1'], Wal2);

            t = time_time();

            // print (stk2.Adr1 + " " + Adr1)
            SUM1 = min (Sum1, usr02['Balance'] /k);
            SUM2 = min (Sum1*k, usr02['Balance'] );
            print ('OLOLO', row, Adr2);
            print('SUMM', SUM1, SUM2);

            TS = [[PrivToPub(row['priv']), AdrToPub(Adr2), Wal2, SUM2, row['priv'], ''], [AdrToPub(Adr1), AdrToPub(row['Address2']), Wal1, SUM1, Priv, '']];
            TS = PreSendTranzh(TS);
            print ('NOOOOO', COOL(TS));
            if (COOL(TS)){
                Sum1 -= SUM1;
                SendTranzh(Tranzhs.Create(TS));
            }
        }

        // print (Sum1)
        if(Sum1 > 0){

            PrivKey = GetUnUsedAddress(Wal1);
            PubKey = PrivToPub(PrivKey);

            // print ('lll', PrivKey, PubKey)
            t = time_time();

            Stk = Order.FromSQL((PubToAdr(PubKey), Adr2, conf['login'], Wal1, Wal2, Sum1, Sum1, k, t, t, PrivKey));
            x = User.Cofunctionunc(Stk, conf['PrivKey']);
            RegiString(PubKey, Wal1, conf['login'], x[0], x[1]);
            PrivKey = decode(PrivKey, 16);
            PrivKey = (PubCode(PrivKey, conf['PubKey'] ));
            time_sleep(0.5);
            ConACC(conf['login'], Wal1, PubToAdr(PubKey), PrivKey);
            // print (AdrToPub(Adr1)== PubKey)
            // print ('Priv :',Priv)
            TS = [[AdrToPub(Adr1), PubKey, Wal1, Sum1, Priv, '']];
            SendTranzh(Tranzhs.Create(PreSendTranzh(TS)));
            time_sleep(3);
            // print (get_User(PubToAdr(PubKey), Wal1)['Balance'] )
            // print
            Send_T1(SendOrder_S(Stk));
        }
    }
}
function Func(mas, TS, stk){
    lol = len(TS)== 1 && mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['AddressTo']== mas[TS[0]['Wal']][TS[0]['PubKey2'] ]['AddressTo'];
    // print (len(TS)== 2, mas[TS[0]['PubKey1'] ]['AddressTo'], mas[TS[1]['PubKey2'] ]['AddressTo'], stk, stk['Wallet1']== TS[0]['Wal'], stk['Wallet2']== TS[1]['Wal'], TS[0]['Sum'] / TS[1]['Sum']== stk['k'], mas[TS[0]['PubKey1'] ]['Address']== stk['Address1'])
    pop = len(TS)== 2 && mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['AddressTo']== mas[TS[1]['Wal']][TS[1]['PubKey2'] ]['AddressTo'] && stk['Wallet1']== TS[0]['Wal'] && stk['Wallet2']== TS[1]['Wal'] && TS[0]['Sum'] / TS[1]['Sum']== stk['k'] && mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['Address']== stk['Address1'];
    return lol || pop
}
function chOrder(a, b){
    [x['Address1'], x['Address2'], x['SumS'], x['k'], x['t'], x['priv']];
    return (a.Adr1== b.Adr1) && (a.Adr2== b.Adr2) && (a.t== b.t) && (a.Wal1== b.Wal1) && (a.Wal2== b.Wal2) && (a.k== b.k);
}
function SendOrder(stk){
    Send_T1(SendOrder_S(stk));
}
async function get_Order(Wallet1,Wallet2,k = 0){
    return await Send_T1(get_Order_S(Wallet1,Wallet2,k));
}
function ANConACC(Login, Wallet, AddressTo, Pass = null){
    if (Pass == null){

        console.log(Pass);
        if (conf['In'] && conf['login'] == Login){
            var x = decode(String(Login) + String(Wallet) + String(AddressTo),256)
            console.log(x);
            // Pass = PrivCode(x,conf['PrivKey']);
        }else{
        console.log('console.error();');

            return;
        }
    }
    console.log(Pass);
    // Send_T1(ANConACC_S(Login, Wallet, AddressTo,Pass));
}
function Login(login, Password){
    if (!conf['In']){
        res = get_UserOF(login)['PubKey'];
        if (res == PrivToPub(sha256_16(sha256_16(login + sha256_16(Password))))){
            conf['login']                 = login;
            conf['passw']                 = sha256_16(Password);
            conf['PrivKey']             = sha256_16(sha256_16(login + sha256_16(Password)));
            conf['PubKey']             = PrivToPub(conf['PrivKey']);
            conf['In']                 = true;
            print ('LogIN');
            if (IsServer(conf['login'])){
                print('Active');
            }
        }
    }
}
function CreateAccountS(Login, Hash){
    Send_T1(CreateAccountS_S(Login, Hash));
}
function CreateAccount(Login, Password){
    CreateAccountS(Login, PrivToPub(sha256_16(sha256_16(Login + sha256_16(Password)))));
}
async function get_UserOF(Address){
    return await Send_T1(get_UserOF_S(Address));
}
async function IsServer(Address){
    return await Send_T1(IsServer_S(Address));
}
function AddWallet(Wallet){
    if (Wallet in conf['OurWallets']){
        return;
    }
    Send_T1(AddWallet_S(Wallet));
}
function ConACC(Address, Wallet, AddressTo, PrivKey){
    Send_T1(ConACC_S(Address, Wallet, AddressTo, PrivKey));
}
function Activate(Address){
    Send_T1(Activate_S(Address));
}
function DisActivate(Address){
    Send_T1(DisActivate_S(Address));}
function SendTONODA(Address, Sum, t = none, Pass = null){
    Sum = float(Sum);
    if (Pass == null && conf['In'] && conf['login'] == Address){
        t = time_time();
        lol = get_UserOF(conf['login'])['Balance'] ['SKR'][0][1];
        // lol = decode(lol, 16)
        lol = PrivCode(lol, conf['PrivKey']);
        lol = encode(lol, 16);
        Pass = decode(sha256_16(String(Sum) + String(t)), 256);
        Pass = PrivCode(Pass, lol);
    }else if (Pass == null && !(conf['In'] && conf['login'] == Address)){
        return;
    }
    if (Sum== 0){
        return;
    }
    Send_T1(SendTONODA_S(Address, Sum, t, Pass));
}
// [[PubKey1, PubKey2, Wal, Sum, PrivKey1, MesIn]]
function Ch_Tranzh(a, b){
    res = len(a['TS'])== len(b['TS']);
    res &= json.dumps(a['TS']) == json.dumps(b['TS']);
    return res;
}
function SendTranzh(x){
    tor = 0;
    Send_T1(SendTranzh_S(x));
}
function GetUnUsedAddress(Wallet){
    PrivKey             = sha256_16(sha256_16(Generator(16)));
    while (Send_T1(GetUnUsedAddress_S(PubToAdr(PrivToPub(PrivKey)), Wallet)) != '1'){
        PrivKey = sha256_16(sha256_16(Generator(16)));
    }
    return PrivKey;
}
function PreSendTranzh(lol){
    mas = {};
    res = 1;
    TS             = [];
    for (let T of lol){
        if (!(T[2] in mas)){
            mas[T[2]] = {};
        }
        if (!(T[0] in mas[T[2]])){
            mas[T[2]][T[0]] = get_User(PubToAdr(T[0]), T[2]);
        }
        if (!(T[1] in mas[T[2]])){
            mas[T[2]][T[1]] = get_User(PubToAdr(T[1]), T[2]);
        }
        t                             = time_time();
        if (len(T)== 8){
            Comis = T[7];
        }else{
            Comis = conf['Comis'];
        }
        Pass                         = String(T[0]) + String(T[1]) + T[2] + String(T[3]) + mas[T[2]][T[0]]['Hash'] + mas[T[2]][T[1]]['Hash'] + String(t);
        print ('Pass1:',Pass );
        Pass                         = sha256_16(Pass);
        T1                             = Tranzh.Create(T[0], T[1], T[2], T[3], sha256_16(mas[T[2]][T[0]]['Hash'] + Pass), sha256_16(mas[T[2]][T[1]]['Hash'] + Pass), Pass, t, PubCode(decode(T[5], 256), T[1]), PubCode(decode(T[5], 256), T[0]), Comis);
        T1['Pass']                     = PrivCode(decode(T1['Pass'], 256), T[4]);
        mas[T[2]][T[0]]['Balance']     -= T[3];

        if (len(mas[T[2]][T[1]]['AddressTo'] ) > 0 && mas[T[2]][T[1]]['AddressTo']== mas[T[2]][T[0]]['AddressTo'] ){
            mas[T[2]][T[1]]['Balance']             += T[3];
        }else{
            mas[T[2]][T[1]]['Balance']             += T[3]*(1-Comis);
        }
        mas[T[2]][T[0]]['Hash']                 = T1['Hash1'];
        mas[T[2]][T[1]]['Hash']                 = T1['Hash2'];
        TS.push(T1);
    }
    return TS;
}
async function get_User(Address, Wallet){
    return await Send_T1(get_User_S(Address, Wallet));
}
function RegiString(PubKey, Wallet, AddressTo = '', FuncH = '', Func = '', AddressFrom = ''){
    if(Wallet in conf['OtherWallets'] && AddressFrom== ''){
        AddressFrom = RegistrOUT(Wallet, PubToAdr(PubKey));
    }
    Send_T1(Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom));
}
async function RegistrOUT(Wal, AddressTo){
    if (!(Wal in conf['OtherWallets'])){
        return;
    }
    return await Send_T1(RegistrOUT_S(Wal, AddressTo),Out = true);
}
function AddWalletOUT(Wallet){
    if (Wallet in conf['OtherWallets']){
        return;
    }
    x = conf['OtherWallets'];
    x.push(Wallet);
    conf['OtherWallets'] = x;
    Send_T1(AddWalletOUT_S(Wallet));
}
async function getBalanceOUT(Wal, Address){//exteranl Address
    return await Send_T1(getBalanceOUT_S(Wal, Address),OUT = true);
}
async function SendOUT_P(Address, AddressTo, Pass, Sum, Wal){
    Wal1 = Wal;
    Wal = Wal.toLowerCase();
    return await Send_T1(SendOUT_P_S(Address, AddressTo, Pass, Sum, Wal1),OUT = true);
}
async function GetDataToSendOUT(Sum, Wal){
    symbol = Wal.toLowerCase();
    return await Send_T1(GetDataToSendOUT_S(Sum, Wal),OUT = true);
}
async function getBalance(Wal, Address){//exteranl Address
    return await Send_T1(getBalance_S(Wal, Address));
}
async function getATran(Wal, Address){//exteranl Address
    return await Send_T1(getATran_S(Wal, Address));
}
async function getHTran(Wal, Address,Adr2 = null,t = null){//exteranl Address
    return await Send_T1(getHTran_S(Wal, Address));
}
async function getAOrder(Wal, Address){//exteranl Address
    return await Send_T1(getAOrder_S(Wal, Address));
}
async function getHOrder(Wal, Address){//exteranl Address
    return await Send_T1(getHOrder_S(Wal, Address));
}
async function getDataForGraf(Wallet1, Wallet2,Time,lastTime){//exteranl Address
    return await Send_T1(getDataForGraf_S(Wallet1, Wallet2,Time,lastTime));
}
async function GetPricesF(Wallet1,data){//exteranl Address
    return await Send_T1(GetPricesF_S(Wallet1, data));
}



class User{
    static FromSQL(kek){
        let pop =         {'Address' : kek[0], 'AddressTo':kek[1], 'PubKey':kek[2], 'FuncH':kek[3], 'Func':kek[4], 'Time':kek[5], 'Freez':kek[6], 'Balance':kek[7], 'Hash':kek[8], 'AddressFrom':kek[9], 'Wallet':kek[10]};
        return pop;
    }

    static ToSQL(x){
        let pop = [x['Address'], x['AddressTo'], x['PubKey'], x['FuncH'], x['Func'], x['Time'], x['Freez'], x['Balance'], x['Hash'], x['AddressFrom'], x['Wallet']];
        return pop;
    }

    static Check(AC, a, RES){
        a = decode(a, 256);
        RES = PubCode(RES, AC['PubKey'] );
        return RES== a;
    }

    static getFunc(AC){
        if(AC['AddressTo'] != ''){
            PubKey = get_UserOF(AC['AddressTo'])['PubKey'];
            return json.loads(encode(PubCode(AC['Func'], PubKey), 256));
        }
    }
            // return encode(PubCode(self['Func'] , PubKey), 256)

    static Cofunctionunc(Func, PrivKey){
        Func = json.dumps(Func);
        Func1 = decode(Func, 256);
        return PrivCode(Func1, PrivKey), Func1;
    }
}
class Tranzh{
    static Create (PubKey1, PubKey2, Wal, Sum, Hash1, Hash2, Pass, time, MesIn = '',MesOut = '', Comis = null){
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
        };
        if (Comis== null || Comis < conf['Comis']){
            x['Comis'] = conf['Comis'];
        }else{
            x['Comis'] = Comis;
        }
        return x;
    }
}
class Tranzhs{
    static Create (TS, AddressTo = null, AddressHashed = null){
        x= {
            'TS'                 : TS,
            'Users'             : [],
            'resTO'             : 0.0,
            'resAnti'             : 0.0,
            'AddressTo'         : AddressTo,
            'AddressHashed'     : AddressHashed
        };
        return x;
    }
    static FromSQL(x){
        return {'Address' : x[0], 'PubKey':x[1], 'Active':x[2], 'Masseges':json.loads(x[3]), 'Balance':json.loads(x[4]), 'Time':x[5]};
    }

    static ToSQL(x){
        return [x['Address'], x['PubKey'], x['Active'], json.dumps(x['Masseges']), json.dumps(x['Balance']), x['Time']];
    }
}
class UserOF{
    static Check(AC, a, RES){
        a = decode(a, 256);
        RES = PubCode(RES, AC['PubKey'] );
        return RES== a;
    }
}
class Order{
    static FromSQL(x){
        return {'Address1' : x[0], 'Address2':x[1], 'AddressFrom':x[2], 'Wallet1':x[3], 'Wallet2':x[4], 'Sum1':x[5], 'SumS':x[6], 'k':x[7], 't':x[8], 't1':x[9], 'priv':x[10]};
    }

    static ToSQL(x){
        return [x['Address1'], x['Address2'], x['AddressFrom'], x['Wallet1'], x['Wallet2'], x['Sum1'], x['SumS'], x['k'], x['t'], x['t1'], x['priv']];
    }
}






function DelIP_S(ip){
    return {'Protocol':'DelIP','IP':ip};
}
function NewIP_S(ip){
    return {'Protocol':'NewIP','IP':ip};
}
function DisActivate_S(Address){
    return {'Protocol':'DisActivate','Address':Address};
}
function ResTranzh_S(Address, Tranzh, res,Pass){
    return {'Protocol':'ResTranzh','Address':Address,'Tranzh':Tranzhs.ToJSON(Tranzh),'res':res,'Pass':Pass};
}
function SendTONODA_S(Address, Sum, time, Pass){
    return {'Protocol':'SendTONODA','Address':Address,'Sum':Sum,'Time':time,'Pass':Pass};
}
function SendTranzh_S(x){
    return {'Protocol':'SendTranzh','Tranzh':x};
}
function GetUnUsedAddress_S(Address, Wallet){
    return {'Protocol':'GetUnUsedAddress','Wallet':Wallet,'Address':Address};
}
function get_User_S(Address, Wallet = 'SKR'){
    return {'Protocol':'get_User','Wallet':Wallet,'Address':Address};
}
function Registr_S(PubKey, Wallet, AddressTo, FuncH, Func, AddressFrom){
    return {'Protocol':'Registr','PubKey':PubKey,'Wallet':Wallet,'AddressTo':AddressTo,'FuncH':FuncH,'Func':Func,'AddressFrom':AddressFrom};
}
function RegistrOUT_S(Wallet, AddressTo){
    return {'Protocol':'RegistrOUT','Wallet':Wallet,'AddressTo':AddressTo};
}
function DelSUPERIP_S(ip){
    return {'Protocol':'DelSUPERIP','IP':ip};
}
function NewSUPERIP_S(ip){
    return {'Protocol':'NewSUPERIP','IP':ip};
}
function AddWalletOUT_S(Wallet){
    return {'Protocol':'AddWalletOUT','Wallet':Wallet};
}
function getBalanceOUT_S(Wallet, Address){
    return {'Protocol':'getBalanceOUT','Address':Address,'Wallet':Wallet};
}
function SendOUT_P_S(Address, AddressTo, Pass, Sum, Wallet){
    return {'Protocol':'SendOUT_P','Address':Address,'AddressTo':AddressTo,'Pass':Pass,'Sum':Sum,'Wallet':Wallet};
}
function GetDataToSendOUT_S(Sum, Wallet){
    return {'Protocol':'GetDataToSendOUT','Wallet':Wallet,'Sum':Sum};
}
function getBalance_S(Wallet, Address){
    return {'Protocol':'getBalance','Wallet':Wallet,'Address':Address};
}
function getATran_S(Wallet, Address){
    return {'Protocol':'getATran','Wallet':Wallet,'Address':Address};
}
function getHTran_S(Wallet, Address){
    return {'Protocol':'getHTran','Wallet':Wallet,'Address':Address};
}
function getAOrder_S(Wallet, Address){
    return {'Protocol':'getAOrder','Wallet':Wallet,'Address':Address};
}
function getHOrder_S(Wallet, Address){
    return {'Protocol':'getHOrder','Wallet':Wallet,'Address':Address};
}
function getDataForGraf_S(Wallet1, Wallet2,Time,lastTime){
    return {'Protocol':'getDataForGraf','Wallet1':Wallet1,'Wallet2':Wallet2,'Time':Time,'lastTime':lastTime};
}
function GetPricesF_S(Wallet1, data){
    return {'Protocol':'GetPricesF','Wallet1':Wallet1,'data':data};
}
function ConACC_S(Address, Wallet, AddressTo, PrivKey){
    return {'Protocol':'ConACC','Address':Address,'Wallet':Wallet,'AddressTo':AddressTo,'PrivKey':PrivKey};
}
function Activate_S(Address){
    return {'Protocol':'Activate','Address':Address};
}
function AddWallet_S(Wallet){
    return {'Protocol':'AddWallet','Wallet':Wallet};
}
function IsServer_S(Address){
    return {'Protocol':'IsServer','Address':Address};
}
function get_UserOF_S(Address){
    return {'Protocol':'get_UserOF','Address':Address};
}
function CreateAccountS_S(Login, Hash){
    return {'Protocol':'CreateAccountS','Login':Login,'Hash':Hash};
}
function ANConACC_S(Login, Wallet, AddressTo,Pass){
    return {'Protocol':'ANConACC','Address':Login,'Wallet':Wallet,'AddressTo':AddressTo,'Pass':Pass};
}
function get_Order_S(Wallet1,Wallet2,k){
    return {'Protocol':'get_Order','Wallet1':Wallet1,'Wallet2':Wallet2,'k':k};
}
function SendOrder_S(Stk){
    return {'Protocol':'SendOrder','Stk':Stk};
}
function CancelOrder_S(stk,Pass){
    return {'Protocol':'CancelOrder','Stk':stk,'Pass':Pass};
}
function GetAllData_S(){
    return {'Protocol':'GetAllData'};
}
function ChangeVoiting_S(New){
    return {'Protocol':'ChangeVoiting','new':New};
}
function UpdateVoiting_S(){
    return {'Protocol':'UpdateVoiting'};
}
function VoteFor_S(Address,key,Pass){
    return {'Protocol':'VoteFor','Address':Address,'key':key,'Pass':Pass};
}
function GetConf_S(){
    return {'Protocol':'GetConf'};
}
function UpDate_S(Ver){
    return {'Protocol':'UpDate','Version':Ver};
}
function GetUpDate_S(){
    return {'Protocol':'GetUpDate'};
}
function CheckVer_S(){
    return {'Protocol':'CheckVer'};
}

function len(arc){
    return arc.length;
}




// BigInt === String

let ver = 1
let systems = {
    2: '01',
    10: '0123456789',
    16: '0123456789abcdef',
    32: 'abcdefghijklmnopqrstuvwxyz234567',
    33: 'abcdefghijklmnopqrstuvwxyz2345670',
    64: '-0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_',
    256: ''
}
for(let i = 0 ;i<256;i++){
    systems[256]+=String.fromCharCode(i);
}
function get_code_string(base){
    if (base in systems){
        return systems[base];
    }
}
var div = function (n, d) {
    n+='';
    d+='';
    var num = String(n),
    numLength = num.length,
    remainder = 0,
    answer = '',
    i = 0;
    while (i < numLength) {
        var digit = i < numLength ? parseInt(num[i]) : 0;
        answer = answer + Math.floor((digit + (remainder * 10)) / d);
        remainder = (digit + (remainder * 10)) % d;
        i++;
    }
    i = 0;
    res = '';
    tor =0;
    for(let i = 0 ;i < answer.length;i++){
        if (answer[i] != '0' || tor){
            tor = 1;
            res+=answer[i];
        }
    }
    if (res.length == 0 ){
        return '0';
    }
    return res;
}
var reminder = function (n, d) {
    n+='';
    d+='';
    var num = String(n),
    numLength = num.length,
    remainder = 0,
    answer = '',
    i = 0;
    while (i < numLength) {
        var digit = i < numLength ? parseInt(num[i]) : 0;
        answer = answer + Math.floor((digit + (remainder * 10)) / d);
        remainder = (digit + (remainder * 10)) % d;
        i++;
    }
    remainder+='';
    i = 0;
    res = '';
    tor =0;
    for(let i = 0 ;i < remainder.length;i++){
        if (remainder[i] != '0' || tor){
            tor = 1;
            res+=remainder[i];
        }
    }
    if (res.length ==0 ){
        return '0';
    }
    return res;
}
var more = function (a, b) {
    a+='';
    b+='';
    if (a.length > b.length){
        return true;
    }else if(a.length < b.length){
        return false;
    }
    for (let i=0;i<a.length;i++){
        if (a[i] > b[i]){
            return true;
        }else if(b[i] > a[i]){
            return false;
        }
    }
    return false;
}
var more_eq = function (a, b) {
    a+='';
    b+='';
    if (a.length > b.length){
        return true;
    }else if(a.length < b.length){
        return false;
    }
    for (let i=0;i<a.length;i++){
        if (a[i] > b[i]){
            return true;
        }else if(b[i] > a[i]){
            return false;
        }
    }
    return true;
}
var sum = function (a, b) {
    a+='';
    b+='';
    let tor = 0;
    let sum = "";
    for(let i=1;i<=Math.max(a.length,b.length)|| tor;i++){
        if (a.length >= i){
            tor+= parseInt(a[a.length-i]);
        }
        if (b.length >= i){
            tor+=parseInt( b[b.length-i]);
        }
        sum =tor%10 + sum;
        tor = parseInt(tor/10);
    }
    if (sum.length ==0 ){
        return '0';
    }
    return sum;
}
var minus = function (a, b) {
    a+='';
    b+='';
    let tor = 0;
    let res = "";
    for(let i=1;i<=Math.min(a.length,b.length)|| tor;i ++){
        let arc = tor;
        tor=0;
        if (b.length >= i){
            arc+= parseInt(b[b.length-i]);
        }
        if (a.length >= i){
            arc-= parseInt(a[a.length-i]);
        }
        if (arc >0){
            tor = 1;
            arc-=10;
        }
        arc*=-1;
        res = arc + res;
    }
    let answer = '';
    for(let i = 0 ;i < res.length;i++){
        if (res[i] != '0' || tor){
            tor = 1;
            answer+=res[i];
        }
    }
    if (answer.length ==0 ){
        return '0';
    }
    return answer;
}
var multiply = function (a, b) {
    a+='';
    b+='';
    let res1 = new Array(a.length+b.length).fill(0)
    for(let i=1;i<=a.length;i++){
        for(let j=1;j<=b.length;j++){
            let I = a.length-i;
            let J = b.length-j;
            res1[I+J+1] += parseInt(a[I])*parseInt(b[J]);
        }
    }
    for(let i = a.length+b.length-1;i>=0;i--){
        if (res1[i] >= 10 && i>0){
            res1[i-1] += parseInt(res1[i]/10);
            res1[i] %=10;
        }
    }
    let res ="";
    let tor = 0;
    for(let i =0;i<a.length+b.length;i++){
        if (res1[i] != 0 || tor){
            tor = 1;
            res+= res1[i];
        }
    }
    if (res.length ==0 ){
        return '0';
    }
    return res;
}
var pow = function(a, n ,mod = null){
    a += '';
    n += '';
    var res = '0';
    while(len(n) > 0){
        if(reminder(n,2) == '1'){
            res = multiply(res,a);
            if (mod != null){
                res = reminder(res,mod);
            }
        }
        a = multiply(a,a);
        if (mod != null){
            a = reminder(a,mod);
        }
        n = div(n,2);
    }
    return res;
}


async function sha256_16(message) {
    // encode as UTF-8
    const msgBuffer = new TextEncoder('utf-8').encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    return hashHex;
}

function encode(val, base, minlen=0){
    val+='';
    base = parseInt(base);
    code_string = get_code_string(base);
    result = '';
    base+=''
    while (more(val , 0)){
        result = code_string[reminder(val , base)] + result;
        val = div(val, base);
    }
    return code_string[0].repeat(Math.max(minlen - len(result), 0)) + result;
}
function decode(string, base){
    string += '';
    base = parseInt(base);
    let code_string = get_code_string(base);
    base+='';
    let result = '0';
    if (base == '16'){
        string = string.toLowerCase();
    }
    let i = 0;
    while (i < len(string)){
        result =multiply( result , base);
        result =sum(result , code_string.indexOf(string[i]));
                      // console.log(string[i],code_string.indexOf(string[i]),result));
        i++;
    }
    return result;
}

class RsaKey{
    construct(n=null, e=null, d=null, p=null, q=null, u=null){
        this._n=n;
        this._e=e;
        this._d=d;
        this._p=p;
        this._q=q;
        this._u=u;
    }
    encrypt(plaintext){
        var res = '';
        plaintext += '';
        while (plaintext > 0){
            res=multiply(res,this._n);
            res= sum(res,pow(reminder(plaintext,this._n), this._e, this._n));
            plaintext=div(plaintext,this._n);
        }
        return res;
    }
    decrypt(plaintext){
        var res = '';
        plaintext += '';
        while (plaintext > 0){
            res=multiply(res,this._n);
            res= sum(res,pow(reminder(plaintext,this._n), this._d, this._n));
            plaintext=div(plaintext,this._n);
        }
        return res;
    }
}
function tobytes(arc){
    return new TextEncoder("utf-8").encode(arc);
}
var encoded = new TextEncoder("utf-8").encode("Γεια σου κόσμε");
var decoded = new TextDecoder("utf-8").decode(encoded);
console.log(encoded, decoded);

// The passphrase used to repeatably generate this RSA key.
var PassPhrase = "The Moon is a Harsh Mistress.";

// The length of the RSA key, in bits.
var Bits = 1024;
var key = "ssh-rsa AAAAgQDQ7Ekamd8gu6yJVHhYrFNtGco3/LP7I54zjPh0Y77R5B/aiDDxrB13b5y6iLW/rO0VKbYCZ8aDXPM8KbUcLOmOvbClUchscWCku7gaEEdQBGwdzMUeAASMZaQDBQ4/pR8hcgQ3wEe4vbFSJvZyt7PyJazE1a/7m50YCxSb6Ohq4w==";
// var MattsRSAkey = cryptico.generateRSAKey(PassPhrase, Bits);
// var MattsPublicKeyString = cryptico.publicKeyString(MattsRSAkey);
// console.log(KJUR.asn1.ASN1Util.getPEMStringFromHex('MIGkMA0GCSqGSIb3DQEBAQUAA4GSADCBjgKBgQDQ7Ekamd8gu6yJVHhYrFNtGco3/LP7I54zjPh0Y77R5B/aiDDxrB13b5y6iLW/rO0VKbYCZ8aDXPM8KbUcLOmOvbClUchscWCku7gaEEdQBGwdzMUeAASMZaQDBQ4/pR8hcgQ3wEe4vbFSJvZyt7PyJazE1a/7m50YCxSb6Ohq4wIIIcx7DABdfd0=', 'RSA PRIVATE KEY'));
// function PBKDF2(password, salt, dkLen=16, count=1000, prf=None, hmac_hash_module=None){
//     password = tobytes(password)
//     salt = tobytes(salt)
//     if (prf == null && hmac_hash_module == null){
//         hmac_hash_module = SHA1;
//     }
//
//     if prf or not hasattr(hmac_hash_module, "_pbkdf2_hmac_assist"):
//         if (prf == null){
//             prf = lambda p,s: HMAC.new(p, s, hmac_hash_module).digest();
//         }
//
//         function link(s){
//             s[0], s[1] = s[1], prf(password, s[1]);
//             return s[0];
//         }
//
//         key = b'';
//         i = 1
//         while len(key) < dkLen:
//             s = [ prf(password, salt + struct.pack(">I", i)) ] * 2
//             key += reduce(strxor, (link(s) for j in range(count)) )
//             i += 1
//
//     else:
//         # Optimized implementation
//         key = b''
//         i = 1
//         while len(key)<dkLen:
//             base = HMAC.new(password, b"", hmac_hash_module)
//             first_digest = base.copy().update(salt + struct.pack(">I", i)).digest()
//             key += base._pbkdf2_hmac_assist(first_digest, count)
//             i += 1
//
//     return key[:dkLen]
// }
function parsePublicKey(s) {
    function stringToArray(s) {
        return s.split('').map(function (c) {
            return c.charCodeAt();
        });
    }
    function arrayToString(a) {
        return String.fromCharCode.apply(null, a);
    }
    function pemToArray(pem) {
        return stringToArray(window.atob(pem));
    }
    function arrayToLen(a) {
        var result = 0, i;
        for (i = 0; i < a.length; i += 1) {
            result = result * 256 + a[i];
        }
        return result;
    }
    var split = s.split(" ");
    var buffer = pemToArray(split[1]);
    var keyLen = arrayToLen(buffer.splice(0, 4));
    var key = buffer.splice(0, keyLen);
    var type = arrayToString(key);
    return decode(type,256);
}
function parseOpenSSH(s){
    function stringToArray(s) {
        return s.split('').map(function (c) {
            return c.charCodeAt();
        });
    }
    function LenToArray(l) {
        var result = [0,0,0,0], i;
        for (i = 3; i >= 0; i -= 1) {
            result[i] = l%256;
            l = parseInt(l/256);
        }
        return result;
    }
    function arrayToString(a) {
        return String.fromCharCode.apply(null, a);
    }
    function arrayToPem(s) {
        return window.btoa(arrayToString(s));
    }
    s = ''+encode(s,256);
    s = stringToArray(s);
    s.unshift(0);
    var l = LenToArray(len(s));
    l = arrayToPem(l.concat(s));
    return l;
}


lol = parsePublicKey(key);
console.log(lol);
console.log(parseOpenSSH(lol));
function generateKey(password,iterations) {
    // salt should be Uint8Array or ArrayBuffer

    var saltBuffer = crypto.getRandomValues(new Uint8Array(8));
    console.log(saltBuffer);
    var encoder = new TextEncoder('utf-8');
    var passphraseKey = encoder.encode("password");

    // You should firstly import your passphrase Uint8array into a CryptoKey
window.crypto.subtle.importKey(
  'raw',
  passphraseKey,
  {name: 'PBKDF2'},
  false,
  ['deriveBits', 'deriveKey']
).then(function(key) {

  return window.crypto.subtle.deriveKey(
    { "name": 'PBKDF2',
      "salt": saltBuffer,
      // don't get too ambitious, or at least remember
      // that low-power phones will access your app
      "iterations": iterations,
      "hash": 'SHA-256'
    },
    key,

    // Note: for this demo we don't actually need a cipher suite,
    // but the api requires that it must be specified.
    // For AES the length required to be 128 or 256 bits (not bytes)
    { "name": 'AES-CBC', "length": 1024 },

    // Whether or not the key is extractable (less secure) or not (more secure)
    // when false, the key can only be passed as a web crypto object, not inspected
    true,

    // this web crypto object will only be allowed for these functions
    [ "encrypt", "decrypt" ]
  )
}).then(function (webKey) {

  return crypto.subtle.exportKey("raw", webKey);

}).then(function(exportedPrivateKey) {
    console.log(exportedPrivateKey);
    var pem = toPem(exportedPrivateKey);
    console.log(pem);
}).catch(function(err) {
    console.log(err);
});

}
generateKey('lol',10000);



async function generate_Private(password,bits = 1024){
    var salt = await sha256_16(password);
    var master_key = PBKDF2(password, salt, count=10000);
    function my_rand(n){
        my_rand.counter += 1;
        return PBKDF2(master_key, "my_rand:%d" % my_rand.counter, dkLen=n, count=1);
    }
    my_rand.counter = 0;
    var RSA_key = RSA.generate(bits, randfunc=my_rand);
    return RSA_key;
}
function get_Public(private_key){
    return private_key.publickey();
}
function get_string(key, format = 'PEM'){
    return key.exportKey(format).decode();
}
function get_Private(arc){
    return get_string(generate_Private(arc));
}
function PrivToPub(password){
	var priv = generate_Private(password);
	var lol = get_string(get_Public(priv));
	return lol;
}
function PubToAdr(Public){
	Public = str(Public).encode();
	var public_key = RSA.importKey(Public);
	var Adress = parseOpenSSH(public_key.n);
	return Adress;
}
function AdrToPub(Adress){
	Adress = 'Sakaar: ' + str(Adress).encode();
	public_key = RSA.importKey(n = parsePublicKey(Adress));
	Public = get_string(public_key);
	return Public;
}
function PubCode(message, public_key){
	message += '';
	public_key += '';
	public_key = RSA.importKey(public_key.encode());
	return public_key.encrypt(message);
}
function PrivCode(ciphertext, private_key){
	ciphertext += '';
	private_key = generate_Private(private_key)
	ciphertext += '';
	return private_key.decrypt(ciphertext);
}
