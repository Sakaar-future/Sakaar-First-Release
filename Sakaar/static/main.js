var Display = 1;
var nowInBarUS = 0;
var nowInBar_b;
var nowInBar;

let Wallet ={
	'Bitcoin : BTC':'BTC',
	'Ethereum : ETH':'ETH',
	'Tether : USDT':'USDT',
	'Bitcoin Cash : BCH':'BCH',
	'Bitcoin SV : BSV':'BSV',
	'Litecoin : LTC':'LTC',
	'Monero : XMR':'XMR',
	'Verge : XVG':'XVG',
	'Zilliqa : ZIL':'ZIL',
	'Cardano : ADA':'ADA',
	'TRON : TRX':'TRX',
	'Dash : DASH':'DASH',
	'Ethereum Classic : ETC':'ETC',
	'Zcash : ZEC':'ZEC',
	'Dogecoin : DOGE':'DOGE',
	'Bitcoin Gold : BTG':'BTG',
	'Decred : DCR':'DCR',
	'Ravencoin : RVN':'RVN',
	'DigiByte : DGB':'DGB',
	'Sakaar : SKR':'SKR',
};
var WalletsPrice ={};
var data =[[]];
let GWal1 = '';
let GWal2 = '';
var run =1;
var t;
var USEGRAF_Type = 2;
var Graf_k = 1000;
var Graf_tm = 60;
var USEGRAF;
var user = null;

var Wallets_We_have = [];
var Update_lastTime = 0;
var Update_Time = 1000;
var Update_Active = true;

var Chat_data={}
var Page_Type = "";
var Chat_Open_From = '';
var Chat_Open_Adr = '';
var Chat_Wallet = '';
var Chat_Date_num = 0;

var Choosen_First = "";
var Choosen_Second = "";

print = console.log;



async function Start(){
	setLogin(conf['login']);
	user = await get_UserOF(conf['login']);
	for(var i in user['Balance']){
		setWallet(i);
		Chat_data[i] = {'Order':[],'Count':0};
		Wallets_We_have.push(i);
		for(let kke of user['Balance'][i]){
			Chat_data[i][kke[0]] = {"PrivKey" : await encode(await PrivCode(kke[1], conf['PrivKey']), 16),'From':{},'Order':[],'Count':0};
		}
	}
	Update_data();
}

function AddWallet(){
	document.getElementById('filter').style.display='block';
	document.getElementById('window').style.display='block';
	document.getElementById("window").innerHTML = '<div style="width : 100%;height : 55px;"><input class="search" id="search"></input></div><div class="body_wind" id ="body_wind"><div  id ="body_wind_l"></div></div>';
	document.getElementById('search').onkeyup = function(){
		document.getElementById('body_wind_l').innerHTML = '';
		var str = document.getElementById('search').value;
		str = str.toLowerCase();
		for (let arc of Object.keys(Wallet)){
			if(arc.toLowerCase().includes(str)){
				var item = createItem();
				item.innerHTML = arc + ' ';
				item.style.height = "45px";
				item.onclick = function() {
					RegistrNewWallet(Wallet[arc]);
					document.getElementById('nav_wal_l').innerHTML = '<hr align="center" width="75%" size="3" color="purple"><div class="nav_element" align="center" onclick="World()">Search</div><hr align="center" width="75%" size="3" color="purple"><div class="nav_element" align="center" onclick="AddWallet()">Add Wallet</div>';
					Start();
					HideWindow();

				};
				document.getElementById('body_wind_l').appendChild(createLinear());
				document.getElementById('body_wind_l').appendChild(item);
				// h = 50;
				// w = 100;
			}
		}
	}
	for (let arc of Object.keys(Wallet)){
		var item = createItem();
		item.innerHTML = arc + ' ';
		item.style.height = "45px";
		item.onclick = function() {
			RegistrNewWallet(Wallet[arc]);
			document.getElementById('nav_wal_l').innerHTML = '<hr align="center" width="75%" size="3" color="purple"><div class="nav_element" align="center" onclick="World()">Search</div><hr align="center" width="75%" size="3" color="purple"><div class="nav_element" align="center" onclick="AddWallet()">AddWallet</div>';
			Start();
			HideWindow();
		};
		document.getElementById('body_wind_l').appendChild(createLinear());
		document.getElementById('body_wind_l').appendChild(item);
	}
}
function SearchWallets(list = 'window',type = 1,func = null){
	if (type == 1){
		document.getElementById('filter').style.display='block';
	}
	document.getElementById(list).style.display='block';
	document.getElementById(list).innerHTML = '<div style="width : 100%;height : 55px;"><input class="search" id="search'+list+'"></input></div><div class="body_wind" id ="body_wind"><div  id ="body_wind_l'+list+'"></div></div>';
	document.getElementById('search'+list).onkeyup = function(){
		document.getElementById('body_wind_l'+list).innerHTML = '';
		WalletsPrice = {};
		var str = document.getElementById('search'+list).value;
		str = str.toLowerCase();
		for (let arc of Object.keys(Wallet)){
			if(arc.toLowerCase().includes(str) && GWal1 != Wallet[arc]){
				var item = createItem();
				item.innerHTML = Wallet[arc] + ' ';
				item.id = Wallet[arc]+list;
				item.style.height = "45px";
				WalletsPrice[Wallet[arc]] = 0;
				item.onclick = function() {
					GWal2 = Wallet[arc];
					if (type == 1){
						HideWindow();
					}
					if (func != null){
						func(GWal1,GWal2)
					}

				};
				document.getElementById('body_wind_l'+list).appendChild(createLinear());
				document.getElementById('body_wind_l'+list).appendChild(item);
				// h = 50;
				// w = 100;
			}
		}
	}
	for (let arc of Object.keys(Wallet)){
		var item = createItem();
		item.innerHTML = Wallet[arc] + ' ';
		item.id = Wallet[arc]+list;
		item.style.height = "45px";
		WalletsPrice[Wallet[arc]] = 0;
		item.onclick = function() {
			GWal2 = Wallet[arc];
			if (type == 1){
				HideWindow();
			}
			if (func != null){
				func(GWal1,GWal2)
			}

		};
		document.getElementById('body_wind_l'+list).appendChild(createLinear());
		document.getElementById('body_wind_l'+list).appendChild(item);
	}
}
function ShowPrices(dat){
	for (var arc of dat){
		document.getElementById(arc+'nav_menu_l').innerHTML = (arc + ' ' + dat[arc]);
	}
	// document.getElementById(Name).innerHTML = document.getElementById(Name).innerHTML + price;
}
function HideWindow(){
	document.getElementById('filter').style.display='none';
	document.getElementById('window').innerHTML = '';
	document.getElementById('window').style.display='none';
}

function bignav(){
	document.getElementById("nav_wal").style.width = "200px";
	document.getElementById("main_1").style.left = "200px";
}
function normalnav(){
	document.getElementById("nav_wal").style.width = "65px";
	document.getElementById("main_1").style.left = "65px";
}
function createItem(){
	var item = document.createElement( 'div' );
	item.className = "nav_element";
	item.setAttribute('align','center');
	return item;
}
function createCanvas(height, width){
	var item = document.createElement( 'canvas' );
	item.id="myCanvas";
	// item.width="1000";
	// item.height="500";

	item.width="1000";
	item.height= "1000";
	item.style="position:absolute; border:1px solid #000000;width: " + width+"%; height: " + height+"%;left =0;top =0";
	return item;
}
function createLinear(){
	var item = document.createElement('hr');
	item.align = "center";
	item.size = 3;
	item.width = "75%";
	item.color="purple";
	return item;
}



function World(){
	document.getElementById("main").appendChild(createItem());
	var it = createItem();
	document.getElementById("display").appendChild(it);
	document.getElementById("display").height += it.height;
	document.getElementById("nav_menu_l").appendChild(createItem());
}
// 1) SKR(статус, положение)
// 2) Мои кошельки(Добавить, перейти на них)
// 3) Голосование
// 4) Активные ордера всех валют
// 5) История всех Ордеров
// 6) Создание Ноды
// 7) Настроики

async function onAccount(){
	// SearchWallets();
	try{
		USEGRAF.run =0;
		await time_sleep(500);
	}catch(e){
	}
	GWal1 = '';

	document.getElementById("main").innerHTML = 'SKR';
	const myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	//1
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Main';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Main";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		SKR();
	};
	myNode.appendChild(item);
	//2
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = MyWallets;
	item.id = 'MyWallets';
	item.innerHTML = 'My Wallets';
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "MyWallets";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		MyWallets();
	};
	myNode.appendChild(item);
	//3
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Voiting';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Voiting";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Voiting();
	};
	myNode.appendChild(item);
	//4
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Order';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Order";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Order_A();
	};
	myNode.appendChild(item);
	//5
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Order_H';
	item.innerHTML = "Order History";
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Order_H";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Order_H();
	};
	myNode.appendChild(item);
	//6
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Setings';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Setings";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Setings();
	};
	myNode.appendChild(item);


	Choosen_Second = "Main";
	document.getElementById(Choosen_Second).className = "nav_element_Choosen";
}



//done
async function getMyWallets(){
	user = await get_UserOF(conf['login']);
	for (var Wallet in user['Balance']){
		list = [];
		for (let Address of user['Balance'][Wallet]){
			list.push(Address[0]);
		}
		dat = await getBalance_list(Wallet,list);
		i =0;
		Wallet_ = String(Wallet)
		var sum = 0;
		tr = '<div class="ALL_Wallet_Adresses" id="ALL_' + Wallet_ + '">';
		for (let Address of user['Balance'][Wallet]){
			Address_ = String(Address[0])
			sum+=parseFloat(dat[i]);
			tr += '<div>';
			tr += '<div class="el_table" onclick = "onWallet(\''+Wallet_ +'\')" id ="' + Wallet_+ '">' + Wallet_ + '</div>';
			tr += '<div class="el_table" onclick = "showWallet(\''+Wallet_+'\', \'' + Address_ +'\')">' + String(dat[i]) + '</div>';
			tr += '<div class="el_table" onclick = "showWallet(\''+Wallet_+'\', \'' + Address_ +'\')">' + Address_ + '</div>';
			tr += '<div class="el_table" onclick = "showWallet(\''+Wallet_+'\', \'' + Address_ +'\')">Submit</div>';
			tr += '<div class="el_table" onclick = "Wallet_D(\''+Wallet_+'\', \'' + Address_ +'\')">Delete</div>';
			tr += '</div>';
			tr += '<hr align="center" size="3" width="75%" color="purple">';
			i ++;
		}
		tr += "</div";
		document.getElementById('main_t').innerHTML +='<div class="ALL_Wallet"  onclick = "Hide_Wallets(\'ALL_'+Wallet_ +'\')"><div class="ALL_Wallet_Name">' + Wallet_ + '</div><div class="ALL_Wallet_Sum">' + sum + '</div></div>';
		document.getElementById('main_t').innerHTML += tr;

		document.getElementById('ALL_'+Wallet_).style.opacity = 0;
		document.getElementById('ALL_'+Wallet_).style.height = "0px";
	}
}
function Hide_Wallets(Wallet){
	if(document.getElementById(Wallet).style.opacity != 0.0){
		document.getElementById(Wallet).style.opacity = 0;
		document.getElementById(Wallet).style.height = "0px";
	}else{
		document.getElementById(Wallet).style.opacity = 1;
		document.getElementById(Wallet).style.height = "auto";
	}
}
async function MyWallets(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	getMyWallets()
}

function Wallet_D(Wallet,Address){
	ANConACC(conf['login'], Wallet, Address)
}
async function GetAddrisesOfWallet(Wal,tor = 0){
	dat = [];
	if (tor == 0){
		for (let i of user['Balance'][String(Wal)]){
			dat.push(i[0]);
		}
	}else{
		for (let i of user['Balance'][String(Wal)]){
			dat.push([i[0],await getBalance(Wal,i[0])]);
		}
	}
	return dat;
}


function Voiting(){
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	tr = '';
	tor = (conf['login'] in conf['Voited']);
	for (let i of Object.keys(conf['Voiting'])){
		if (tor){
			tr += '<div>';
			tr+='<div class="el_table">'+String(conf['Voiting'][i][1])+'</div>';
			tr += '<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="' + String(100 *conf['Voiting'][i][0]/conf['FullFreez'])+ '" aria-valuemin="0" aria-valuemax="100" style="margin-left: 0; width:' + String(100 *conf['Voiting'][i][0]/conf['FullFreez'])+ '%"></div></div>';
		}else{
			tr += '<div onclick="Voit(\''+ String(i)+'\')">';
			tr+='<div class="el_table">'+String(conf['Voiting'][i][1])+'</div>';
		}

		tr += '</div>';
		tr += '<hr align="center" size="3" width="' + 100 *conf['Voiting'][i][0]/conf['FullFreez'] + '%" color="purple" style="margin-left: 0;">';
	}
	setMenu(tr);
}
function Voit(key){
	HDisplay();
	VoteFor(key);
}


function SKR(){

	SDisplay();
}

function setMenu(tr){
	document.getElementById('main_t').innerHTML += tr;
}

function CreateNODA(){

	HDisplay();
}

function Setings(){

	SDisplay();
}

function Registr_M(){
	var username = document.getElementById("UserName_R").value;
	var password = document.getElementById("Password_R").value;
	CreateAccount(username, password);
}
function Login_M(){
	var username = document.getElementById("UserName_R").value;
	var password = document.getElementById("Password_R").value;
	Login(username, password);
}



//done
function setLogin(name){
	if (name.length > 10){
		name = name.substring(0, 10);
		name += '...';
	}
	document.getElementById("user_name").innerHTML = name;
	document.getElementById("user_logo").src = "http://127.0.0.1:10101/user_logo/"+name;
}

function setWallet(name){
	document.getElementById("nav_wal_l").appendChild(createLinear());
	var item = createItem();
	item.onclick = function() {onWallet(name)};
	item.id = name;
	item.innerHTML = item.id;
	document.getElementById("nav_wal_l").appendChild(item);
}


async function onWallet(name){
	try{
		USEGRAF.run =0;
		await time_sleep(500);
	}catch(e){
		console.log(e);
	}
	GWal1 = name;
	Chat_Wallet = name;
	// Chat_0();
	document.getElementById("main").innerHTML = '';
	const myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	//1
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Chat';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Chat";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Chat_0();
	};
	myNode.appendChild(item);
	//2
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Graph';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Graph";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Graph();
	};
	myNode.appendChild(item);
	//3
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Tranzh_P';
	item.innerHTML = "Active Transactions";
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Tranzh_P";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Tranzh_P();
	};
	myNode.appendChild(item);
	//4
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Order';
	item.innerHTML = item.id;
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Order";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Order_A();
	};
	myNode.appendChild(item);
	//5
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Order_H';
	item.innerHTML = "Oredr History";
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Order_H";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Order_H();
	};
	myNode.appendChild(item);
	//6
	myNode.appendChild(createLinear());
	var item = createItem();
	item.id = 'Tranzh_H';
	item.innerHTML = "Transactions History";
	item.onclick =async function(){
		if(Choosen_Second != ""){
			document.getElementById(Choosen_Second).className = "nav_element";
		}
		Choosen_Second = "Tranzh_H";
		document.getElementById(Choosen_Second).className = "nav_element_Choosen";
		Tranzh_H();
	};
	myNode.appendChild(item);

	Choosen_Second = "Chat";
	document.getElementById(Choosen_Second).className = "nav_element_Choosen";
	Chat_0();
}

async function Graph(){
	HDisplay();
	SearchWallets(list = 'nav_menu_l',type = 0,func = async function(GWal1,GWal2) {
		console.log(GWal1);
		document.getElementById("TypeOfOperstion").innerHTML = '<option value="1">Buy ' + GWal1 + '</option><option value="2">Buy ' + GWal2 + '</option>';

		document.getElementById("div_AdrFrom").innerHTML = GWal1 + ' Address : <select id="AdrFrom"></select>';
		let x = await GetAddrisesOfWallet(GWal1);
		for (let arc of x){
			let le = arc.length;
			if(20<le){le = 20}
			document.getElementById("AdrFrom").innerHTML += '<option value="'+ arc +'">' + arc.substr(0, le) + '</option>';
		}

		// document.getElementById("TypeOfOperstion").innerHTML
		document.getElementById("div_AdrTo").innerHTML = GWal2 + ' Address : <select id="AdrTo" value="Receiving Address"></select>';
		x = await GetAddrisesOfWallet(GWal2);
		for (let arc of x){
			let le = arc.length;
			if(20<le){le = 20}
			document.getElementById("AdrTo").innerHTML += '<option value="'+ arc +'">' + arc.substr(0, le) + '</option>';
		}
	});
	document.getElementById("main").innerHTML = '';


	// div for item for upper
	var item = document.createElement( 'div' );
	item.id = 'upper_navbar';
	document.getElementById("main").appendChild(item);

	var item = document.createElement( 'input' );
	item.type="button";
	item.id = 'Type_0';
	item.value = 'Lineal Graf';
	document.getElementById("upper_navbar").appendChild(item);
	document.getElementById('Type_0').onclick = function(){
		USEGRAF_Type = 0;
	}

	var item = document.createElement( 'input' );
	item.type="button";
	item.id = 'Type_1';
	item.value = 'Candle Graf';
	document.getElementById("upper_navbar").appendChild(item);
	document.getElementById('Type_1').onclick = function(){
		USEGRAF_Type = 2;
	}

	var item = document.createElement( 'input' );
	item.type="number";
	item.id = 'Graf_tm';
	item.value = 10;
	document.getElementById("upper_navbar").appendChild(item);
	document.getElementById('Graf_tm').onkeyup = function(){
		var num = document.getElementById('Graf_tm').value;
		Graf_tm = num;
	}

	var item = document.createElement( 'input' );
	item.type="number";
	item.id = 'Graf_k';
	item.value = 1000;
	document.getElementById("upper_navbar").appendChild(item);
	document.getElementById('Graf_k').onkeyup = function(){
		var num = document.getElementById('Graf_k').value;
		Graf_k = num;
	}


	// div for Canvas
	var item = document.createElement( 'div' );
	item.className = 'forGrafC';
	item.id = 'forGrafC';
	item.style.position = "absolute";
	document.getElementById("main").appendChild(item);
	// Create Canvas
	var h = $(".forGrafC").height();
	h=(h -30)/ h * 100;
	var w = $(".forGrafC").width();
	w=(w -80)/ w * 100;
	var c = createCanvas(h, w);
	document.getElementById("forGrafC").appendChild(c);
	var item = createCanvas(100, 100);
	item.id = 'ScalarLine';
	document.getElementById("forGrafC").appendChild(item);
	var item = createCanvas(100, 100);
	item.id = 'cursor';
	document.getElementById("forGrafC").appendChild(item);


	var item = document.createElement( 'div' );
	item.id = 'PriceBar';
	document.getElementById("main").appendChild(item);

	var item = document.createElement( 'div' );
	item.id = 'SendOrdaer';
	document.getElementById("main").appendChild(item);

	document.getElementById("SendOrdaer").innerHTML = '<div>Type Of Operstion : <select id="TypeOfOperstion"></select></div>';
	document.getElementById("SendOrdaer").innerHTML += '<div id = "div_AdrFrom"></div>';
	document.getElementById("SendOrdaer").innerHTML += '<div id = "div_AdrTo"></div>';
	document.getElementById("SendOrdaer").innerHTML += '<div style="display: inline-block;"><div>Price : </div><input type="text" id="Price" value="Price"></div>';
	document.getElementById("SendOrdaer").innerHTML += '<div style="display: inline-block;"><div>Sum To Send : </div><input type="text" id="SumToSend" value="Sum To Send"></div>';
	document.getElementById("SendOrdaer").innerHTML += '<input style="display: inline-block;" type="button" id="SendOrder_B" value="Send">';

	document.getElementById('SendOrder_B').onclick = function(){
		var e = document.getElementById("TypeOfOperstion");
		var x = e.options[e.selectedIndex].value;
		var adrfrom;
		var adrto;
		if (x == 1){
			var e = document.getElementById("AdrTo");
			var adrfrom = e.options[e.selectedIndex].value;
			var e = document.getElementById("AdrFrom");
			var adrto = e.options[e.selectedIndex].value;
		}else if(x == 2){
			var e = document.getElementById("AdrFrom");
			var adrfrom = e.options[e.selectedIndex].value;
			var e = document.getElementById("AdrTo");
			var adrto = e.options[e.selectedIndex].value;
		}
		var adrfrom = document.getElementById('AdrFrom').value;
		var adrto = document.getElementById('AdrTo').value;
		var price = parseFloat(document.getElementById('Price').value);
		var sum = parseFloat(document.getElementById('SumToSend').value);
		MakeOrder(adrfrom,GWal1,sum,adrto,GWal2,price);
	};

	// connectConvas('myCanvas');

	// Create Order

	// var item = document.createElement( 'div' );
	// item.style.width = "100%";
	// item.style.height = "40%";
	// item.style.background = "#123456";
	// item.style.position = "absolute";
	// item.id = "ORDES_C_Case";
	// h = $(".cursor").height() + "px";
	// item.style.top = h;
 //  item.style.margin = 0;
	// document.getElementById("forGrafC").appendChild(item);
	// CreateORDER_L();

	USEGRAF= new Graf(2, 'myCanvas');
	USEGRAF.ShowGraf();
}
// Пара цена ОбьемВОчереди Дата добавления Закончено
//done

//done
var dat_ActiveOrders = null;
async function Order_A_1(Wallet){
	let dat = await getAOrder(Wallet,conf['login'])
	dat_ActiveOrders = dat;
	tr = '';
	i = 0;
	for (let arc of dat){
		tr += '<div>';
		tr += '<div class="el_table">' +String(arc[3]) + '</div>';
		tr += '<div class="el_table">' +String(arc[4]) + '</div>';
		tr += '<div class="el_table">' +String(arc[0]) + '</div>';
		tr += '<div class="el_table">' +String(arc[1]) + '</div>';
		tr += '<div class="el_table">' +String(arc[5]) + '</div>';
		tr += '<div class="el_table">' +String(arc[5]/arc[6]) + '</div>';
		tr += '<div class="el_table">' +String(arc[7]) + '</div>';
		tr += '<div class="el_table">' +String(arc[8]) + '</div>';
		tr += '<div class="el_table" onclick="Order_D(' + String(i) + ')">remove</div>';
		tr += '</div>';
		tr += '<hr align="center" size="3" width="75%" color="purple">';
		i += 1;
	}
	return tr;
}
async function Order_A(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	if (GWal1 == ''){
		SearchWallets(list = 'window',type = 1,func = function(GWal1,GWal2) {setMenu(Order_A_1(GWal2))});
	}else{
		setMenu(await Order_A_1(GWal1));
	}
}
async function Order_H_1(Wallet){
	let dat = await getHOrder(Wallet,conf['login'])
	dat_ActiveOrders = dat;
	tr = '';
	i = 0;
	for (let arc of dat){
		tr += '<div>';
		tr += '<div class="el_table">' +String(arc[4]) + '</div>';
		tr += '<div class="el_table">' +String(arc[2]) + '</div>';
		tr += '<div class="el_table">' +String(arc[3]) + '</div>';
		tr += '<div class="el_table">' +String(arc[5]) + '</div>';
		tr += '<div class="el_table">' +String(arc[0]) + '</div>';
		tr += '<div class="el_table">' +String(arc[1]) + '</div>';
		tr += '<div class="el_table" onclick="Order_D(' + String(i) + ')">remove</div>';
		tr += '</div>';
		tr += '<hr align="center" size="3" width="75%" color="purple">';
		i += 1;
	}
	return tr;
}
async function Order_H(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	if (GWal1 == ''){
		SearchWallets(list = 'window',type = 1,func = function(GWal1,GWal2) {setMenu(Order_H_1(GWal2))});
	}else{

		setMenu(await Order_H_1(GWal1));
	}
}
async function Order_D(stk){
	CancelOrder(await Order.FromSQL(dat_ActiveOrders[stk]));
}

async function Tranzh_H(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	let dat = await getHTran(GWal1,conf['login'],null,0);
	tr = '';
	for (let arc of dat.reverse()){
		tr += '<div>';
		tr += '<div class="el_table">' +String(arc[0]) + '</div>';
		tr += '<div class="el_table">' +String(arc[1]) + '</div>';
		tr += '<div class="el_table">' +String(arc[2]) + '</div>';
		tr += '<div class="el_table">' +String(arc[3]) + '</div>';
		tr += '<div class="el_table">' +String(arc[4]) + '</div>';
		tr += '</div>';
		tr += '<hr align="center" size="3" width="75%" color="purple">';
	}

	setMenu(tr);
}
async function Tranzh_P(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	let dat = await getATran(GWal1,conf['login']);
	tr = '';
	for (let arc of dat){
		tr += '<div>';
		tr += '<div class="el_table">' +String(arc[0]) + '</div>';
		tr += '<div class="el_table">' +String(arc[1]) + '</div>';
		tr += '<div class="el_table">' +String(arc[2]) + '</div>';
		tr += '<div class="el_table">' +String(arc[3]) + '</div>';
		tr += '</div>';
		tr += '<hr align="center" size="3" width="75%" color="purple">';
	}
	setMenu(tr);
}


function SDisplay(){
	Page_Type = "";
	if(Display == 0){
		Display = 1;
		var link = document.getElementById('display');
		// link.style.display = 'none'; //or
		link.style.opacity = 1.0;
	}
}
function HDisplay(){
	Page_Type = "";
	if(Display == 1){
		Display = 0;
		var link = document.getElementById('display');
		// link.style.display = 'none'; //or
		link.style.opacity = 0.0;
	}
}
function UDispaly(){
}

// 1. Мой аккаунт:
	// 1) SKR(статус, положение)
	// 2) Мои кошельки(Добавить, перейти на них)
	// 3) Голосование
	// 4) Активные ордера всех валют
	// 5) История всех Ордеров
	// 6) Создание Ноды
	// 7) Настроики
// 2-inf. кошелькт
	// 1) Чат(выбор пользователя для отправки этой валюты и видимые сообшения в виде чат месенджера)
	// 2) Графики зависимости с другими валютами
	// 3) Призводимые транзакций с этой валютой
	// 4) активные Ордера от этой валюты
	// 5) История Ордеров от этой валюты ( можно посмотреть и потелится отдельнвми трагзакциями)
	// 6) История транзакций с этой валютой ( можно посмотреть и потелится отдельнвми трагзакциями)




function SNEW(id, id_b){
	if(nowInBarUS == 1){
		document.getElementById(nowInBar_b).style.backgroundColor = "#ee6620";
		document.getElementById(nowInBar).style.opacity = "0.0";

		if(nowInBar == id){
			nowInBarUS =0
			document.getElementById('display').style.height = "120px";
			return
		}
	}
	document.getElementById(id_b).style.backgroundColor = "#f38c59";
	document.getElementById(id).style.opacity = "1.0";
	nowInBarUS=1;
	nowInBar_b = id_b;
	nowInBar = id;
	document.getElementById('display').style.height = "80%";
}
function SNEW_Send(){
	var Wal = document.getElementById('send_Wall').value;
	var Adr1 = document.getElementById('send_From').value;
	var Adr2 = document.getElementById('send_To').value;
	var Sum = document.getElementById('send_Sum').value;
	var Msg = document.getElementById('send_Msg').value;
	Send(Wal,Adr1,Adr2,Sum,Msg,0)();
}


async function Chat_0(){
	SDisplay();
	Page_Type = "Chat_0";
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"><h3 align="center" style="margin-top: 16px;">Your Wallets</h3></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div></div>';
	const myNode = document.getElementById("Chat_SKR");
	myNode.innerHTML = '';
	index =Chat_data[Chat_Wallet];
	for (let Adr of index['Order']){
		myNode.appendChild(createLinear());
		var item = createItem();
		item.onclick = async function (){
			Chat_Open_Adr = Adr;
			Chat_1();
		};
		item.innerHTML = '<div class="Chat_Label" id="Big_Chat">' + Adr.slice(0, 50) + '</div>';
		if(index[Adr]['Count'] > 0){
			item.innerHTML +='<div class="Chat_Notion" id="Big_Chat">' + index[Adr]['Count'] + '</div>'
		}
		myNode.appendChild(item);
	}
}
async function Chat_1() {
	Page_Type = "Chat_1";
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"><h3 align="center" style="margin-top: 16px;">Chats</h3><div id="Chat_Back">Back</div></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div></div>';
	var myNode = document.getElementById("Chat_SKR");
	document.getElementById('Chat_Back').onclick = async function(){
		onWallet(Chat_Wallet);
	};
	myNode.innerHTML = '';
	index = Chat_data[Chat_Wallet][Chat_Open_Adr];
	for (let Adr2 of index['Order'].slice(0, 100)){
		myNode.appendChild(createLinear());
		var item = createItem();
		item.onclick = async function (){
			Chat_Open_From = Adr2;
			Chat_2();
		};
		item.removeAttribute('align');
		if(len(index['From'][Adr2]['From']) > 0){
			item.innerHTML = '<div class="Chat_Label" id="Big_Chat">' + index['From'][Adr2]['From'] + '</div>';
		}else{
			item.innerHTML = '<div class="Chat_Label" id="Big_Chat">' + Adr2.slice(0,50) + '</div>';
		}
		var date_a;
		var date = new Date(parseFloat(index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2])*1000);
		if(Update_Time - index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2] < 86400){
			date_a = date.getHours() + ":" + date.getMinutes();
		}else{
			date_a = date.getDate() +  ' ' + getMonth_Brif(date.getMonth())
		}
		item.innerHTML += '<div class="Chat_Time" id="Big_Chat">'+ date_a + '</div><div class="Chat_Text" id="Big_Chat">'+ index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][0] +'</div>';
		if((len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) > 0){
			item.innerHTML +='<div class="Chat_Notion" id="Big_Chat">' + (len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) + '</div>'
		}
		myNode.appendChild(item);
	}


	myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	index = Chat_data[Chat_Wallet];
	for (let Adr of index['Order'].slice(0, 100)){
		myNode.appendChild(createLinear());
		var item = createItem();

		if(Adr == Chat_Open_Adr){
			item.className = "nav_element_Choosen";
		}
		item.onclick = async function (){
			Chat_Open_Adr = Adr;
			Chat_1();
		};
		item.innerHTML = '<div class="Chat_Label" id="Name_Chat_Wallet">' + Adr.slice(0, 50) + '</div>';
		if(index[Adr]['Count'] > 0){
			item.innerHTML +='<div class="Chat_Notion" id="Big_Chat">' + index[Adr]['Count'] + '</div>'
		}
		myNode.appendChild(item);
	}
}
async function Chat_2() {
	Page_Type = "Chat_2";
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"><div id="Chat_Back">Back</div></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div><div class = "Send"><div class = "Send_Msg"><input class ="Send" id="Send_Msg" placeholder="Text" type ="text"></div><div class = "Send_Sum"><input id="Send_Sum" class ="Send" placeholder="Sum" type ="text"></div><input class ="Send_Btn" id="Send_Btn" value="Send" type ="button"></div></div>';
	document.getElementById("Chat_SKR_l").style.overflow = 'scroll';
	document.getElementById("Chat_SKR_l").style.bottom = '23px';
	document.getElementById("Chat_Window").style.overflow = 'hidden';
	document.getElementById('Send_Btn').onclick = function(){
		var Msg = document.getElementById("Send_Msg").value;
		var Sum = document.getElementById("Send_Sum").value;
		// document.getElementById("Send_Sum").value = document.getElementById("Send_Msg").value = "";
		Send(Chat_Wallet,Chat_Open_Adr,Chat_Open_From,Sum,Msg);
	};
	document.getElementById('Chat_Back').onclick = async function(){
		Chat_1();
	};

	var myNode = document.getElementById("Chat_SKR");
	myNode.innerHTML = '';
	var index = Chat_data[Chat_Wallet][Chat_Open_Adr]['From'][Chat_Open_From];
	var from = max(index['Last']-50,0)
	var step = min(len(index['Msgs']) - from,100);

	for (let msg of index['Msgs'].slice(from, step)){
		var date = new Date(parseFloat(msg[2])*1000);
		if(date.getDate() != Chat_Date_num){
			Chat_Date_num = date.getDate();
			var item_D = document.createElement( 'div' );
			myNode.innerHTML += '<div class="Chat_Date" align="center"><div class="Chat_Date_Content">' + date.getDate() +  ' ' + getMonth_Brif(date.getMonth()) + '</div></div>'
		}
		var item = document.createElement( 'div' );
		if(msg[3]){
			item.innerHTML = "<div class = 'Msg_Cont' id = 'in' ><div class = 'Msg_Text'>" + msg[0] + "</div><div class = 'Msg_Sum'>" + msg[1] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + date.getHours() + ":" + date.getMinutes() + "</div></div>";
		}else{
			item.innerHTML = "<div class = 'Msg_Cont' id = 'out' ><div class = 'Msg_Text'>" + msg[0] + "</div><div class = 'Msg_Sum'>" + msg[1] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + date.getHours() + ":" + date.getMinutes() + "</div></div>";
		}
		myNode.appendChild(item);
	}
	Chat_data[Chat_Wallet][Chat_Open_Adr]['Count']-=from + step - index['Last'];
	Chat_data[Chat_Wallet]['Count']-=from + step - index['Last'];

	index['Last'] += from + step;

	myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	index = Chat_data[Chat_Wallet][Chat_Open_Adr];
	for (let Adr2 of index['Order'].slice(0, 100)){
		myNode.appendChild(createLinear());
		var item = createItem();
		if(Adr2 == Chat_Open_From){
			item.className = "nav_element_Choosen";
		}
		item.onclick = async function (){
			Chat_Open_From = Adr2;
			Chat_2();
		};
		item.removeAttribute('align');
		if(len(index['From'][Adr2]['From']) > 0){
			item.innerHTML = '<div class="Chat_Label">' + index['From'][Adr2]['From'] + '</div>';
		}else{
			item.innerHTML = '<div class="Chat_Label">' + Adr2.slice(0,50) + '</div>';
		}
		var date_a;
		var date = new Date(parseFloat(index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2])*1000);
		if(Update_Time - index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2] < 86400){
			date_a = date.getHours() + ":" + date.getMinutes();
		}else{
			date_a = date.getDate() +  ' ' + getMonth_Brif(date.getMonth())
		}
		item.innerHTML += '<div class="Chat_Time">'+ date_a + '</div><div class="Chat_Text">'+ index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][0] +'</div>';
		if((len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) > 0){
			item.innerHTML +='<div class="Chat_Notion">' + (len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) + '</div>'
		}
		myNode.appendChild(item);
	}
}


async function GetMassagesOthors(Wal,Adr){
	dat = await getHTran(Wal,Adr);
	var data = [];
	for (let i of dat){
		lol = await PubToAdr(i[1]);
		kek = await PubToAdr(i[2]);
		if (!(data.includes(lol) || lol == Adr)){
			data.push(lol);
		}else if(!(data.includes(kek) || kek == Adr)){
			data.push(kek);
		}

	}
	return data;
}
async function Send(Wal,Adr1,Adr2,Sum,Msg,tor = true){
	if (tor){
		SendTranzh(await Tranzhs.Create(await PreSendTranzh([[await AdrToPub(Adr1),await  AdrToPub(Adr2), Wal, parseFloat(Sum), Chat_data[Chat_Wallet][Chat_Open_Adr]['PrivKey'], Msg]])));
	}else{
		for (let kke of user['Balance'][String(Wal)]){
			if (kke[0] == Adr1){
				Priv = encode(PrivCode(kke[1], conf['PrivKey']), 16);
				SendTranzh(await Tranzhs.Create(await PreSendTranzh([[await AdrToPub(Adr1),await  AdrToPub(Adr2), Wal, parseFloat(Sum), Priv, Msg]])));
			}
		}
	}
}



function ClearCanvas(){
	this.ctx.clearRect(0, 0, this.c.width, this.c.height);
	this.ctx.beginPath();
}
class Graf {
	constructor(Type , canvasName) {
		this.Type = Type;
		this.Wal1 = GWal1;
		this.Wal2 = GWal2;
		this.run = 1;
		this.posx = 0;
		this.mn = 0;
		this.posy = 0;
		this.canvasName = canvasName;
		this.Graf_k = 1000;
		this.Graf_tm = 10;
		var c = document.getElementById(canvasName);
		this.h = c.height;
		this.w = c.width;
		// this.ctx = this.c.getContext("2d");
		this.dat = [];


		if(Type != 1){
			document.getElementById('cursor').addEventListener("mousemove", function(e) {

				var c = document.getElementById(canvasName);
				var cRect = c.getBoundingClientRect();    // Gets CSS pos, && width/height
				var x = Math.round(e.clientX - cRect.left); // Subtract the 'left' of the canvas
				var y = Math.round(e.clientY - cRect.top);  // from the X/Y positions to make
				let i = 0;
				var c1 = document.getElementById('cursor');
				var ctx1 = c1.getContext("2d");


				let h = $("#"+canvasName).height()/$("#ScalarLine").height();
				let w = $("#"+canvasName).width()/$("#ScalarLine").width();
				ctx1.clearRect(0, 0, c1.width, c1.height);
				ctx1.beginPath();

				x = x / ($(".forGrafC").width()) * c1.width;
				y = y / ($(".forGrafC").height()) * c1.height;
				ctx1.strokeStyle='#9900ff';
				ctx1.fillStyle = "green";
				ctx1.lineWidth = 2;
				ctx1.textBaseline = "middle";
				ctx1.textAlign = "center";
				ctx1.font = 'bold ' + (c1.width*(1-w)*3/5)/4+ 'px sans-serif';
				ctx1.moveTo(x , 0);
				ctx1.lineTo(x , c1.height);
				// ctx1.moveTo(0 , y);
				// ctx1.lineTo(c1.width , y);
				x = x / w;
				y = y / h;
				var lol = function(number) {
  			  		var letter = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toString();
  				  	var le = letter.length;
  				  	if(6<le){le = 6;}
  				  // tm = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toFixed(0).toString().length;
  				  // if(tm>le){le = tm;}
  				  	letter = letter.substr(0, le);
  				  	ctx1.fillText(letter, c1.width*w + c1.width*(1-w)/2, h*number);
  					ctx1.moveTo(c1.width*w + c1.width*(1-w)/5, h*number);
  					ctx1.lineTo(0, h*number);
  					ctx1.moveTo(c1.width*w + c1.width*(1-w)*4/5, h*number);
  					ctx1.lineTo(c1.width, h*number);
  			  	};
			  	lol(y/h*h);
				ctx1.fillStyle='#9900ff';
				if(USEGRAF.Type == 2){
					var dat = USEGRAF.dat[0];
					var tm = USEGRAF.dat[1];
					let l = dat.length;
					while(i < l){

						if(dat[i][0] <= x && x <= dat[i][0] + tm){
							lol(dat[i][1]);
							lol(dat[i][2]);
							ctx1.stroke();
							break;
						}
						i++;
					}
				}else if(USEGRAF.Type == 0){
					var dat = USEGRAF.dat;
					let l = dat.length-1;
					while(i < l){
						if(dat[i][0] < x && x <= dat[i+1][0]){
							lol(dat[i][1]);
							ctx1.stroke();
							break;
						}
						i++;
					}
				}
			});
		}
	}
	async ShowGraf(){
		// console.log(this);
		while(true){
			this.graf_k = Graf_k;
			this.graf_tm = Graf_tm;
			this.Type = USEGRAF_Type;
			this.Wal1 = GWal1;
			this.Wal2 = GWal2;
			if(this.Type == 1 || this.Type == 0){
				// eel.GrafLineal(this)(Graf.DrawGrafLineal);
			}

			if(this.Type == 2){
				// eel.GrafCandle(this)(Graf.DrawGrafCandle);
			}
			ShowPrices(GetPricesF(GWal1, WalletsPrice));
			if(this.Type != 1){
				if(!USEGRAF.run){break;}
				for (let i=0;i<60;i++){
					if (this.Wal1 != GWal1 || this.Wal2 != GWal2){
						break;
					}
					await time_sleep(500);
					var h = $(".forGrafC").height();
					h=(h -30)/ h * 100;
					var w = $(".forGrafC").width();
					w=(w -80)/ w * 100;
					document.getElementById(this.canvasName).style.height = h + "%";
					document.getElementById(this.canvasName).style.width = w + "%";
				}
			}
		}
	}


	static DrawGrafLineal(dat){
		if(!USEGRAF.run){return;}
		USEGRAF = dat

		var c = document.getElementById(dat.canvasName);
		var ctx = c.getContext("2d");
		ctx.clearRect(0, 0, dat.w, dat.h);
		ctx.beginPath();
		ctx.lineWidth = 3;
		ctx.strokeStyle='#000';
		if(dat.dat.length >0 ){
			let i = 1;
			let l = dat.dat.length;
			ctx.moveTo(dat.dat[0][0], dat.dat[0][1]);
			while(i < l){
				ctx.lineTo(dat.dat[i][0], dat.dat[i][1]);
				i++;
			}
			ctx.stroke();

			if(dat.Type != 1){

				let h = $("#"+dat.canvasName).height()/$("#ScalarLine").height();
				let w = $("#"+dat.canvasName).width()/$("#ScalarLine").width();

				var c1 = document.getElementById("ScalarLine");
				var ctx1 = c1.getContext("2d");

				ctx1.clearRect(0, 0, c.width, c.height);
				ctx1.beginPath();
				ctx1.lineWidth = 3;
				ctx1.strokeStyle='#555';
				ctx1.textBaseline = "middle";
				ctx1.textAlign = "center";
				ctx1.fillStyle='#555';
			  ctx1.font = 'bold ' + (c1.width*(1-w)*3/5)/4+ 'px sans-serif';

			  var lol = function(number) {
			  	var letter = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toString();
				  var le = letter.length;
				  if(6<le){le = 6;}
				  // tm = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toFixed(0).toString().length;
				  // if(tm>le){le = tm;}
				  letter = letter.substr(0, le);
				  ctx1.fillText(letter, c1.width*w + c1.width*(1-w)/2, h*number);
					ctx1.moveTo(c1.width*w + c1.width*(1-w)/5, h*number);
					ctx1.lineTo(0, h*number);
					ctx1.moveTo(c1.width*w + c1.width*(1-w)*4/5, h*number);
					ctx1.lineTo(c1.width, h*number);
			  };
			  lol(c.height*0.2);
			  lol(c.height*0.4);
			  lol(c.height*0.6);
			  lol(c.height*0.8);

				ctx1.stroke()
				ctx1.beginPath();
				ctx1.strokeStyle = "#000";
				ctx1.fillStyle = "#000";
			  lol(dat.dat[l-1][1]);
			  	ctx1.stroke()
			}
		}
	}
	static DrawGrafCandle(data){

		if(!USEGRAF.run){return;}
		USEGRAF = data;
		var dat = data.dat[0];
		var tm = data.dat[1];
		let la = '';

		var c = document.getElementById(data.canvasName);
		var ctx = c.getContext("2d");
		ctx.clearRect(0, 0, data.w, data.h);
		ctx.beginPath();
		ctx.lineWidth = 3;

		if(dat.length >0 ){
			let i = 1;
			let l = dat.length;
			while(i < l){
				var mx = dat[i][1];
				if(mx < dat[i][2]){
					mx = dat[i][2];
				}
				var mn = dat[i][1];
				if(mn > dat[i][2]){
					mn = dat[i][2];
				}
				if(mx == dat[i][2]){
					ctx.fillStyle='#ff3333';
					la = '#ff3333';
					ctx.fillRect(dat[i][0]+tm/10, dat[i][1], tm-tm/5, mx - mn);

					ctx.strokeStyle='#ff3333';ctx.beginPath();
					ctx.moveTo(dat[i][0] + tm/2 , dat[i][3]);
					ctx.lineTo(dat[i][0] + tm/2 , mx);
					ctx.moveTo(dat[i][0] + tm/2 , dat[i][4]);
					ctx.lineTo(dat[i][0] + tm/2 , mn);
					ctx.stroke()
				}else{
					ctx.fillStyle='#33ff33';
					la = '#33ff33';
					ctx.fillRect(dat[i][0]+tm/10, dat[i][2], tm-tm/5, mx - mn);

					ctx.strokeStyle='#33ff33';ctx.beginPath();
					ctx.moveTo(dat[i][0] + tm/2 , dat[i][3]);
					ctx.lineTo(dat[i][0] + tm/2 , mx);
					ctx.moveTo(dat[i][0] + tm/2 , dat[i][4]);
					ctx.lineTo(dat[i][0] + tm/2 , mn);
					ctx.stroke()
				}
				i++;
			}
			ctx.stroke();
			// ctx.moveTo(c.width*0.2, 0)
			// ctx.lineTo(c.width*0.2, c.height)
			// ctx.moveTo(c.width*0.4, 0)
			// ctx.lineTo(c.width*0.4, c.height)
			// ctx.moveTo(c.width*0.6, 0)
			// ctx.lineTo(c.width*0.6, c.height)
			// ctx.moveTo(c.width*0.8, 0)
			// ctx.lineTo(c.width*0.8, c.height)
			let h = $("#"+data.canvasName).height()/$("#ScalarLine").height();
			let w = $("#"+data.canvasName).width()/$("#ScalarLine").width();

			var c1 = document.getElementById("ScalarLine");
			var ctx1 = c1.getContext("2d");

			ctx1.clearRect(0, 0, c.width, c.height);
			ctx1.beginPath();
			ctx1.lineWidth = 3;
			ctx1.strokeStyle='#555';
			ctx1.textBaseline = "middle";
			ctx1.textAlign = "center";
			ctx1.fillStyle='#555';
		  ctx1.font = 'bold ' + (c1.width*(1-w)*3/5)/4+ 'px sans-serif';

		  var lol = function(number) {
		  	var letter = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toString();
			  var le = letter.length;
			  if(6<le){le = 6;}
			  tm = ((c.height -number)/USEGRAF.posx + USEGRAF.mn).toFixed(0).toString().length;
			  if(tm>le){le = tm;}
			  letter = letter.substr(0, le);
			  ctx1.fillText(letter, c1.width*w + c1.width*(1-w)/2, h*number);
				ctx1.moveTo(c1.width*w + c1.width*(1-w)/5, h*number);
				ctx1.lineTo(0, h*number);
				ctx1.moveTo(c1.width*w + c1.width*(1-w)*4/5, h*number);
				ctx1.lineTo(c1.width, h*number);
		  };
		  lol(c.height*0.2);
		  lol(c.height*0.4);
		  lol(c.height*0.6);
		  lol(c.height*0.8);

			ctx1.stroke();
			ctx1.beginPath();
			ctx1.strokeStyle=la;
			ctx1.fillStyle="#000";
		  lol(dat[i-1][2]);
			ctx1.stroke();
		}
	}
	// calcArea();
}



async function Update_data_Chat(lastTime,now){
	for(var Wallet of Wallets_We_have){
		dat = await getHTran(Wallet,conf['login'],Update_lastTime,0);
		dat_to_priv = [];
		for(var msg of dat){
			if(msg[6] > now){
				continue;
			}
			var kek = Chat_data[Wallet];
			if(msg[1] in kek){
				kek = kek[msg[1]];
				dat_to_priv.push([msg[11],kek['PrivKey']])


			}else if(msg[2] in kek){
				kek = kek[msg[2]];

				dat_to_priv.push([msg[10],kek['PrivKey']])

			}
		}

		dat_to_priv = await PrivCode_list(dat_to_priv);

		for(var msg of dat){
			if(msg[6] > now){
				continue;
			}
			var kek = Chat_data[Wallet];
			if(msg[1] in kek){
				var index = kek['Order'].indexOf(msg[1]);
				if (index > -1) {
				  kek['Order'].splice(index, 2);
				}
				kek['Order'].unshift(msg[1]);

				kek = kek[msg[1]];
				if(!( msg[2] in kek['From'])){
					kek['From'][msg[2]]={'Last':0,'Msgs':[],'From':msg[8]};
				}
				index = kek['Order'].indexOf(msg[2]);
				if (index > -1) {
				  kek['Order'].splice(index, 1);
				}
				kek['Order'].unshift(msg[2]);
				var msg_text = await encode(dat_to_priv[msg[11]+ kek['PrivKey']], 256)
				kek['From'][msg[2]]['Msgs'].push([msg_text,msg[3],msg[6],false,msg[0]]);
				if(Wallet == Chat_Wallet && Chat_Open_Adr == msg[1] && Chat_Open_From == msg[2] && Page_Type == "Chat_2"){
					kek['From'][msg[2]]['Last'] ++;
					var item = document.createElement( 'div' );
					item.className  = 'Msg_Block';
					item.innerHTML = "<div class = 'Msg_Cont' id = 'out' ><div class = 'Msg_Text'>" + msg_text + "</div><div class = 'Msg_Sum'>" + msg[3] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + msg[6] + "</div></div>";
					document.getElementById("Chat_SKR").appendChild(item);
				}else{
					kek['Count']++;
					Chat_data[Wallet]['Count']++;
				}

			}else if(msg[2] in kek){
				var index = kek['Order'].indexOf(msg[2]);
				if (index > -1) {
				  kek['Order'].splice(index, 2);
				}
				kek['Order'].unshift(msg[2]);

				kek = kek[msg[2]];
				if(!( msg[1] in kek['From'])){
					kek['From'][msg[1]]={'Last':0,'Msgs':[],'From':msg[7]};
				}
				index = kek['Order'].indexOf(msg[1]);
				if (index > -1) {
				  kek['Order'].splice(index, 1);
				}
				kek['Order'].unshift(msg[1]);
				var msg_text = await encode(dat_to_priv[msg[10]+ kek['PrivKey']], 256)
				kek['From'][msg[1]]['Msgs'].push([msg_text,msg[3],msg[6],true,msg[0]]);

				if(Wallet == Chat_Wallet && Chat_Open_Adr == msg[2] && Chat_Open_From == msg[1] && Page_Type == "Chat_2"){
					kek['From'][msg[1]]['Last'] ++;
					var item = document.createElement( 'div' );
					item.innerHTML = "<div class = 'Msg_Cont' id = 'in' ><div class = 'Msg_Text'>" + msg_text + "</div><div class = 'Msg_Sum'>" + msg[3] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + msg[6] + "</div></div>";
					document.getElementById("Chat_SKR").appendChild(item);
				}else{
					kek['Count']++;
					Chat_data[Wallet]['Count']++;
				}
			}
		}
	}
	print(Chat_data)
	if(Page_Type == "Chat_1"){
		Chat_1()
	}else if(Page_Type == "Chat_0"){
		Chat_0()
	}else if(Page_Type == "Chat_0"){
		myNode = document.getElementById("nav_menu_l");
		myNode.innerHTML = '';
		index = Chat_data[Chat_Wallet][Chat_Open_Adr];
		for (let Adr2 of index['Order'].slice(0, 100)){
			myNode.appendChild(createLinear());
			var item = createItem();
			if(Adr2 == Chat_Open_From){
				item.className = "nav_element_Choosen";
			}
			item.onclick = async function (){
				Chat_Open_From = Adr2;
				Chat_2();
			};
			item.removeAttribute('align');
			if(len(index['From'][Adr2]['From']) > 0){
				item.innerHTML = '<div class="Chat_Label">' + index['From'][Adr2]['From'] + '</div>';
			}else{
				item.innerHTML = '<div class="Chat_Label">' + Adr2.slice(0,50) + '</div>';
			}
			var date_a;
			var date = new Date(parseFloat(index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2])*1000);
			if(Update_Time - index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][2] < 86400){
				date_a = date.getHours() + ":" + date.getMinutes();
			}else{
				date_a = date.getDate() +  ' ' + getMonth_Brif(date.getMonth())
			}
			item.innerHTML += '<div class="Chat_Time">'+ date_a + '</div><div class="Chat_Text">'+ index['From'][Adr2]['Msgs'][len(index['From'][Adr2]['Msgs'])-1][0] +'</div>';
			if((len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) > 0){
				item.innerHTML +='<div class="Chat_Notion">' + (len(index['From'][Adr2]['Msgs']) - index['From'][Adr2]['Last']) + '</div>'
			}
			myNode.appendChild(item);
		}
	}
}

async function Update_data(){
	while(Update_Active){
		Update_data_Chat(Update_lastTime,time_time());

		Update_lastTime = time_time();
		await time_sleep(Update_Time);
	}
}
