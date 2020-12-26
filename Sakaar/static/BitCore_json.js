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
function getBalance_list_S(Wallet, Addresses){
    return {'Protocol':'getBalance_list','Wallet':Wallet,'Addresses':Addresses};
}
function getATran_S(Wallet, Address){
    return {'Protocol':'getATran','Wallet':Wallet,'Address':Address};
}
function getHTran_S(Wal, Address,t = null,ofPub = 1){
    return  {'Protocol':'getHTran','Wallet':Wal,'Address':Address,'Time':t,'ofPub':ofPub};
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

function generate_Private_S(password){
    return {'Protocol':'generate_Private','Password':password};
}
function PubToAdr_S(Public){
    return {'Protocol':'PubToAdr','Public':Public};
}
function AdrToPub_S(address){
    return {'Protocol':'AdrToPub','Address':address};
}
function PrivToPub_S(password){
    return {'Protocol':'PrivToPub','Password':password};
}
function PubCode_S(message, public_key){
    return {'Protocol':'PubCode','Message':message,'Public_key':public_key};
}
function PrivCode_S(message, public_key){
    return {'Protocol':'PrivCode','Message':message,'Public_key':public_key};
}
