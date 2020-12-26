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
function getMonth(month){
    month++;
    if(month == 1){
        return "January";
    }else if(month == 2){
        return "February";
    }else if(month == 3){
        return "March";
    }else if(month == 4){
        return "April";
    }else if(month == 5){
        return "May";
    }else if(month == 6){
        return "June";
    }else if(month == 7){
        return "July";
    }else if(month == 8){
        return "August";
    }else if(month == 9){
        return "September";
    }else if(month == 10){
        return "October";
    }else if(month == 11){
        return "November";
    }else if(month == 12){
        return "December";
    }
}
function getMonth_Brif(month){
    month++;
    if(month == 1){
        return "Jan";
    }else if(month == 2){
        return "Feb";
    }else if(month == 3){
        return "Mar";
    }else if(month == 4){
        return "Apr";
    }else if(month == 5){
        return "May";
    }else if(month == 6){
        return "Jun";
    }else if(month == 7){
        return "Jul";
    }else if(month == 8){
        return "Aug";
    }else if(month == 9){
        return "Sept";
    }else if(month == 10){
        return "Oct";
    }else if(month == 11){
        return "Nov";
    }else if(month == 12){
        return "Deс";
    }
}
function time_sleep(ms) {
    ms *= 1000;
    return new Promise(resolve => setTimeout(resolve, ms));
}
function time_time(){
    print(new Date().toString())
    return parseFloat((new Date().getTime()))/1000;
}
var conf = {}

if (!('MyIP' in conf)){
    conf['MyIP'] = null;
}
if (!('Connected' in conf)){
    conf['Connected'] = ['2de0e412453b.ngrok.io'];
}
if (!('SUPERIP' in conf)){
    conf['SUPERIP'] = [];
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

if (!('In' in conf)){
    conf['In'] = false;
}
if (!('login' in conf)){
    conf['login'] = '';
}
if (!('PrivKey' in conf)){
    conf['PrivKey'] = '';
}
if (!('passw' in conf)){
    conf['passw'] = '';
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
conf['PubKey'] = ""
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

    const lol =         await fetch("http://2de0e412453b.ngrok.io", requestOptions)
             .then(response => response.json())
    return lol
}
// GetConf();

function LogOut(){
    conf['login']                 = '';
    conf['passw']                 = '';
    conf['PrivKey']             = '';
    conf['PubKey']             = '';
    conf['In']                 = false;
}
async function SendOUT(Wal, Address, AddressTo, Sum){//Using our Address system && external Address To
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

        lol = await PrivCode(lol, conf['PrivKey']);
        lol = encode(lol, 16);
        SendOUT_P(kke['AddressFrom'] , AddressTo, await PrivCode(await decode(kke['AddressFrom'] + AddressTo + String(x) + Wal, 256), lol), x, Wal);

        Sum -= x;
        if (Sum<=0){
            return;
        }
            // lol = await await decode(lol, 16)

        dat = GetDataToSendOUT(Sum, Wal);
        i = 0;
        while (i < len(dat)){
            dat[i][0] = kke['PubKey'];
            dat[i][4] = lol;
            i += 1;
        }

        SendTranzh(Tranzhs.Create(await PreSendTranzh(dat), AddressTo, await PrivCode(await decode(kke['AddressFrom'] + AddressTo + String(Sum) + Wal, 256), lol) ));
    }
}
async function GetConf(){
    dat = await Send_T1(GetConf_S());
    console.log(dat);
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
    conf['VoitingTime'] = dat[11]
    conf['VoitingTitle'] = dat[12]
    conf['VoitingDescription'] = dat[13]
    conf['Connected_TCP'] = dat[14]
    conf['SUPERIP_TCP'] = dat[15]
}
function UpdateVoiting(){
    conf['Voiting'] = Send_T1(GetVoiting_S());
    return;
}
async function CancelOrder(stk,Pass = null){
    if (Pass == null && conf['In'] && conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo']){
        Pass = await PrivCode(await decode(String(stk),256),conf['PrivKey']);
        SendTranzh(Tranzhs.Create(await PreSendTranzh([[await PrivToPub(stk['priv']), await AdrToPub(get_UserOF(conf['login'])['Balance'] [stk['Wallet1']][0][0]), stk['Wallet1'], stk['Sum1'], stk['priv'], '']])));
    }else if (Pass == null &&         !(conf['In'] && conf['login'] == get_User(stk['Address1'],stk['Wallet1'])['AddressTo'])){
        return;
    }
    Send_T1(CancelOrder_S(stk,Pass));
}
async function MakeOrder(Adr1, Wal1, Sum1, Adr2, Wal2, k){
    if (conf['In']){
        // console.log ('MakeOrder')

        Priv = null;
        usr1 = get_UserOF(conf['login']);
        for (let pop of usr1['Balance'] [Wal1]){
            if(pop[0]== Adr1){
                Priv = encode(await PrivCode(pop[1], conf['PrivKey']), 16);
            }
        }
        if (Priv== null ){
            return
        }

        async function COOL(TS){
            res = 1;
            mas = {};
            tor = 0;
            stk = null;
            for(let T of TS){
                if (!(T['Wal'] in mas)){
                    mas[T['Wal']] = {};
                }
                if (!(T['PubKey1'] in mas[T['Wal']])){
                    mas[T['Wal']][T['PubKey1'] ] = get_User(await PubToAdr(T['PubKey1'] ), T['Wal']);
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
                    mas[T['Wal']][T['PubKey2'] ] = get_User(await PubToAdr(T['PubKey2'] ), T['Wal']);
                }
                res &= await Checker(T, mas[T['Wal']][T['PubKey1'] ], mas[T['Wal']][T['PubKey2'] ]);
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
            console.log(res ,(tor != 1 || Func(mas, TS, stk)));
            return res;
        }

        dat = get_Order(Wal2,Wal1,1/k)
        // console.log (dat)
        for (let row of dat){

            row = Order.FromSQL(row);

            usr02 = get_User(row['Address1'], Wal2);

            t = time_time();

            // console.log (stk2.Adr1 + " " + Adr1)
            SUM1 = min (Sum1, usr02['Balance'] /k);
            SUM2 = min (Sum1*k, usr02['Balance'] );
            console.log ('OLOLO', row, Adr2);
            console.log('SUMM', SUM1, SUM2);

            TS = [[await PrivToPub(row['priv']), await AdrToPub(Adr2), Wal2, SUM2, row['priv'], ''], [await AdrToPub(Adr1), await AdrToPub(row['Address2']), Wal1, SUM1, Priv, '']];
            TS = await PreSendTranzh(TS);
            console.log ('NOOOOO', COOL(TS));
            if (COOL(TS)){
                Sum1 -= SUM1;
                SendTranzh(Tranzhs.Create(TS));
            }
        }

        // console.log (Sum1)
        if(Sum1 > 0){

            PrivKey = GetUnUsedAddress(Wal1);
            PubKey = await PrivToPub(PrivKey);

            // console.log ('lll', PrivKey, PubKey)
            t = time_time();

            Stk = Order.FromSQL((await PubToAdr(PubKey), Adr2, conf['login'], Wal1, Wal2, Sum1, Sum1, k, t, t, PrivKey));
            x = User.Cofunctionunc(Stk, conf['PrivKey']);
            Registr(PubKey, Wal1, conf['login'], x[0], x[1]);
            PrivKey = await decode(PrivKey, 16);
            PrivKey = (await PubCode(PrivKey, conf['PubKey'] ));
            await time_sleep(0.5);
            ConACC(conf['login'], Wal1, await PubToAdr(PubKey), PrivKey);
            // console.log (await AdrToPub(Adr1)== PubKey)
            // console.log ('Priv :',Priv)
            TS = [[await AdrToPub(Adr1), PubKey, Wal1, Sum1, Priv, '']];
            SendTranzh(Tranzhs.Create(await PreSendTranzh(TS)));
            await time_sleep(3);
            // console.log (get_User(PubToAdr(PubKey), Wal1)['Balance'] )
            // console.log
            Send_T1(SendOrder_S(Stk));
        }
    }
}
async function Checker(T, kke1, kke2){
    Pass = sha256_16(str(T['PubKey1'] ) + str(T['PubKey2'] ) + T['Wal'] + str(T['Sum']) + kke1['Hash'] + kke2['Hash'] + str(T['time']));
    res1 = 1;
    if(T['Wal'] in conf['OurWallets']){
        res1 = (kke1['Balance'] - T['Sum']>=0) && (kke2['Balance']>=0);
    }else if(T['Wal'] in conf['OtherWallets']){
        res1 = (kke1['Balance'] + float(getBalanceOUT(kke1['Wallet'].lower(), kke1['AddressFrom'] )) -T['Sum']);
    }else{
        res1 = 0;
    }
    tor = T['Comis']>=conf['Comis'] && await Check(kke1, Pass, T['Pass']) && sha256_16(kke1['Hash'] + Pass)== T['Hash1'] && sha256_16(kke2['Hash'] + Pass)== T['Hash2'] && T['Sum'] > 0;
    console.log ('Checker', T['Comis']>=conf['Comis'] , await Check(kke1, Pass, T['Pass']) , sha256_16(kke1['Hash'] + Pass)== T['Hash1'] , sha256_16(kke2['Hash'] + Pass)== T['Hash2'] , T['Sum'] > 0,T['Sum']);
    console.log ('Checker', res1,tor);
    return (tor && res1);
}
function Func(mas, TS, stk){
    lol = len(TS)== 1 && mas[TS[0]['Wal']][TS[0]['PubKey1'] ]['AddressTo']== mas[TS[0]['Wal']][TS[0]['PubKey2'] ]['AddressTo'];
    // console.log (len(TS)== 2, mas[TS[0]['PubKey1'] ]['AddressTo'], mas[TS[1]['PubKey2'] ]['AddressTo'], stk, stk['Wallet1']== TS[0]['Wal'], stk['Wallet2']== TS[1]['Wal'], TS[0]['Sum'] / TS[1]['Sum']== stk['k'], mas[TS[0]['PubKey1'] ]['Address']== stk['Address1'])
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
//done
async function Login(login, Password){
    if (!conf['In']){
        res = (await get_UserOF(login))['PubKey'];
        if (res == await PrivToPub(await sha256_16(await sha256_16(login + await sha256_16(Password))))){
            conf['login']                 = login;
            conf['passw']                 = await sha256_16(Password);
            conf['PrivKey']             = await sha256_16(await sha256_16(login + await  sha256_16(Password)));
            conf['PubKey']             = await PrivToPub(conf['PrivKey']);
            conf['In']                 = true;
            Start();
            onAccount()
            document.getElementById('filter_none_clicable').style.display ='none';
            document.getElementById('Registr_form').style.display ='none';
        }
    }
}
async function IsServer(Address){
    return await Send_T1(IsServer_S(Address));
}
function ConACC(Address, Wallet, AddressTo, PrivKey){
    Send_T1(ConACC_S(Address, Wallet, AddressTo, PrivKey));
}
function Activate(Address){
    Send_T1(Activate_S(Address));
}
function DisActivate(Address){
    Send_T1(DisActivate_S(Address));}
async function SendTONODA(Address, Sum, t = none, Pass = null){
    Sum = float(Sum);
    if (Pass == null && conf['In'] && conf['login'] == Address){
        t = time_time();
        lol = get_UserOF(conf['login'])['Balance'] ['SKR'][0][1];
        // lol = await decode(lol, 16)
        lol = await PrivCode(lol, conf['PrivKey']);
        lol = encode(lol, 16);
        Pass = await decode(sha256_16(String(Sum) + String(t)), 256);
        Pass = await PrivCode(Pass, lol);
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
async function Registr(PubKey, Wallet, AddressTo = '', FuncH = '', Func = '', AddressFrom = ''){
    if(Wallet in conf['OtherWallets'] && AddressFrom== ''){
        AddressFrom = RegistrOUT(Wallet, await PubToAdr(PubKey));
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
async function getDataForGraf(Wallet1, Wallet2,Time,lastTime){//exteranl Address
    return await Send_T1(getDataForGraf_S(Wallet1, Wallet2,Time,lastTime));
}
async function GetPricesF(Wallet1,data){//exteranl Address
    return await Send_T1(GetPricesF_S(Wallet1, data));
}
async function getHOrder(Wal, Address){//exteranl Address
    return await Send_T1(getHOrder_S(Wal, Address));
}
async function getAOrder(Wal, Address){//exteranl Address
    return await Send_T1(getAOrder_S(Wal, Address));
}

async function RegistrNewWallet(Wallet){
    if (conf['In']){
        PrivKey = await GetUnUsedAddress(Wallet);
        PubKey = await PrivToPub(PrivKey);
        Registr(PubKey, Wallet, conf['login']);
        PrivKey = await decode(PrivKey, 16);
        PrivKey = await PubCode(PrivKey, conf['PubKey'] );
        await time_sleep(0.5);
        ConACC(conf['login'], Wallet, await PubToAdr(PubKey), PrivKey);
    }
}
//done
function CreateAccountS(Login, Hash){
    Send_T1(CreateAccountS_S(Login, Hash));
}
async function CreateAccount(Login, Password){
    CreateAccountS(Login, await PrivToPub(await sha256_16(await sha256_16(Login + await sha256_16(Password)))));
}
async function VoteFor(key,Address = null,Pass = null){
    if (Pass == null && conf['In']){
        Address = conf['login'];
        Pass = await PrivCode(await decode(key,256),conf['PrivKey']);
    }else if(!conf['In']){
        return
    }
    Send_T1(VoteFor_S(Address, key, Pass))
}
function SendTranzh(x){
    Send_T1(SendTranzh_S(x));
}
async function PreSendTranzh(lol){
    mas = {};
    res = 1;
    TS             = [];
    for (let T of lol){
        if (!(T[2] in mas)){
            mas[T[2]] = {};
        }
        if (!(T[0] in mas[T[2]])){
            mas[T[2]][T[0]] = await get_User(await PubToAdr(T[0]), T[2]);
        }
        if (!(T[1] in mas[T[2]])){
            mas[T[2]][T[1]] = await get_User(await PubToAdr(T[1]), T[2]);

        }
        t                             = time_time();
        if (len(T)== 8){
            Comis = T[7];
        }else{
            Comis = conf['Comis'];
        }
        var Pass                         = T[0] + T[1] + T[2] + String(T[3]) + mas[T[2]][T[0]]['Hash'] + mas[T[2]][T[1]]['Hash'] + String(t);
        Pass                         = await sha256_16(Pass);
        T1                             = Tranzh.Create(T[0], T[1], T[2], T[3], await sha256_16(mas[T[2]][T[0]]['Hash'] + Pass), await sha256_16(mas[T[2]][T[1]]['Hash'] + Pass), Pass, t, await PubCode(await decode(T[5], 256), T[1]), await PubCode(await decode(T[5], 256), T[0]), Comis);
        T1['Pass']                     = await PrivCode(await decode(T1['Pass'], 256), T[4]);
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
async function GetUnUsedAddress(Wallet){
    PrivKey             = await sha256_16(await sha256_16(await Generator(16)));
    while (await Send_T1(GetUnUsedAddress_S(await PubToAdr(await PrivToPub(PrivKey)), Wallet)) != '1'){
        PrivKey = await sha256_16(await sha256_16(await Generator(16)));
    }
    return PrivKey;
}
async function ANConACC(Login, Wallet, AddressTo, Pass = null){
    if (Pass == null){
        if (conf['In'] && conf['login'] == Login){
            var x = await decode(Login + Wallet + AddressTo,256)
            Pass = await PrivCode(x,conf['PrivKey']);
        }else{
            return;
        }
    }
    Send_T1(ANConACC_S(Login, Wallet, AddressTo,Pass));
}
async function getATran(Wal, Address){//exteranl Address
    return await Send_T1(getATran_S(Wal, Address));
}
async function getBalance(Wal, Address){//exteranl Address
    return await Send_T1(getBalance_S(Wal, Address));
}
async function getBalance_list(Wal, Address){//exteranl Address
    return await Send_T1(getBalance_list_S(Wal, Address));
}
async function getHTran(Wal1, Address,t = 0,ofPub = 1){//exteranl Address
    return await Send_T1(getHTran_S(Wal1, Address,t ,ofPub));
}
async function get_User(Address, Wallet){
    return await Send_T1(get_User_S(Address, Wallet));
}
async function get_UserOF(Address){
    return await Send_T1(get_UserOF_S(Address));
}

//remace
async function PubToAdr(Public){
    return await Send_T1(PubToAdr_S(Public));
}
async function AdrToPub(address){
    return await Send_T1(AdrToPub_S(address));
}
async function PrivToPub(password){
    var lol = await Send_T1(PrivToPub_S(password));
    return await Send_T1(PrivToPub_S(password));
}
async function PubCode(message, public_key){
    return await Send_T1(PubCode_S(message.toString(),public_key));
}
async function PrivCode(message, public_key){
    return await Send_T1(PrivCode_S(message.toString(),public_key));
}



async function Check(AC, a, RES){
    a = await decode(a, 256);
    RES = await PubCode(RES, AC['PubKey'] );
    return RES== a;
}
async function getFunc(AC){
    if(AC['AddressTo'] != ''){
        PubKey = get_UserOF(AC['AddressTo'])['PubKey'];
        return json.loads(encode(await PubCode(AC['Func'], PubKey), 256));
    }
}
async function Cofunctionunc(Func, PrivKey){
    Func = json.dumps(Func);
    Func1 = await decode(Func, 256);
    return await PrivCode(Func1, PrivKey), Func1;
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
            // return encode(await PubCode(self['Func'] , PubKey), 256)
}
class Tranzh{
    static Create (PubKey1, PubKey2, Wal, Sum, Hash1, Hash2, Pass, time, MesIn = '',MesOut = '', Comis = null){
        let x = {
            'PubKey1'     : PubKey1,
            'PubKey2'     : PubKey2,
            'Sum'         : Sum,
            'Wal'         : Wal,
            'Hash1'       : Hash1,
            'Hash2'       : Hash2,
            'Pass'        : Pass,
            'MesIn'       : MesIn,
            'MesOut'      : MesOut,
            'time'        : time,
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
        let x = {
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

}
class Order{
    static FromSQL(x){
        return {'Address1' : x[0], 'Address2':x[1], 'AddressFrom':x[2], 'Wallet1':x[3], 'Wallet2':x[4], 'Sum1':x[5], 'SumS':x[6], 'k':x[7], 't':x[8], 't1':x[9], 'priv':x[10]};
    }

    static ToSQL(x){
        return [x['Address1'], x['Address2'], x['AddressFrom'], x['Wallet1'], x['Wallet2'], x['Sum1'], x['SumS'], x['k'], x['t'], x['t1'], x['priv']];
    }
}


//done
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
    64: 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/',
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
async function decode(string, base){
    base = parseInt(base);
    if(base == 16){
        return BigInt('0x' + string);
    }else if(base == 2){
        return BigInt('0b' + string);
    }else if(base == 256){
        base = BigInt(base);
        res = BigInt(0);
        let code_string = get_code_string(base);
        for (let i =0;i < len(string);i++){
            res =res * base;
            res =res + BigInt(code_string.indexOf(string[i]));
        }
        return res;
    }
}
async function sha256_16(message) {
    // print(sha256(message))
    return sha256(message);
    // encode as UTF-8
    const msgBuffer = new TextEncoder('utf-8').encode(message);

    // hash the message
    const hashBuffer = await crypto.subtle.digest('SHA-256', msgBuffer);

    // convert ArrayBuffer to Array
    const hashArray = Array.from(new Uint8Array(hashBuffer));

    // convert bytes to hex string
    const hashHex = hashArray.map(b => ('00' + b.toString(16)).slice(-2)).join('');
    // console.log(hashHex);
    return hashHex;
}

async function encode(val, base, minlen=0){
    val = BigInt(val);
    base = BigInt(base);
    code_string = get_code_string(base);
    result = '';
    while (val>0){
        result = code_string[val % base] + result;
        val = val/base;
    }
    return code_string[0].repeat(Math.max(minlen - len(result), 0)) + result;
}
function max(a,b){
    if(a>=b){
        return a;
    }
    return b;
}
function min(a,b){
    if(a>=b){
        return b;
    }
    return a;
}
