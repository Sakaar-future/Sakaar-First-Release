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
	'PortBitX : SKR':'SKR',
	'SKR':'SKR'
};
var WalletsPrice ={};
var data =[[]];
let GWal1 = '';
let GWal2 = '';
var run =1;
var t;
var USEGRAF_Type = 2;
var Graf_k = 1000;
var Graf_tm = 10;
var USEGRAF;

function sleep(ms) {
 return new Promise(resolve => setTimeout(resolve, ms));
}

function bignav(){
	document.getElementById("nav_wal").style.width = "200px";
	document.getElementById("main_1").style.left = "200px";
}

function normalnav(){
	document.getElementById("nav_wal").style.width = "65px";
	document.getElementById("main_1").style.left = "65px";
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
					eel.CreateWallet(Wallet[arc]);
					document.getElementById('nav_wal_l').innerHTML = '<hr align="center" width="75%" size="3" color="purple"><div class="nav_element" onclick="World()">Search</div><hr align="center" width="75%" size="3" color="purple"><div class="nav_element" onclick="AddWallet()">AddWallet</div>';
					eel.Start()();
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
			eel.CreateWallet(Wallet[arc]);
			document.getElementById('nav_wal_l').innerHTML = '<hr align="center" width="75%" size="3" color="purple"><div class="nav_element" onclick="World()">Search</div><hr align="center" width="75%" size="3" color="purple"><div class="nav_element" onclick="AddWallet()">AddWallet</div>';
			eel.Start()();
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
	for (var arc in dat){
		document.getElementById(arc+'nav_menu_l').innerHTML = (arc + ' ' + dat[arc]);
	}
	// document.getElementById(Name).innerHTML = document.getElementById(Name).innerHTML + price;
}

function HideWindow(){
	document.getElementById('filter').style.display='none';
	document.getElementById('window').innerHTML = '';
	document.getElementById('window').style.display='none';
}

function createItem(){
	var item = document.createElement( 'div' );
	item.className = "nav_element";
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

function generateQRCode() {
	var data = document.getElementById("data").value;
	eel.generate_qr(data)(setImage);
}

function setImage(base64) {

	document.getElementById("qr").src = base64;
}

function Heel(){

	document.getElementById("main").innerHTML = "Heelo JavaScript!";
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
		await sleep(500);
	}catch(e){
	}
	GWal1 = '';
	document.getElementById("main").innerHTML = 'SKR';
	const myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	//1
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = function(){SKR()};
	item.id = 'SKR';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//2
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = MyWallets;
	item.id = 'MyWallets';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//3
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Voiting;
	item.id = 'Voiting';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//4
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Order_A;
	item.id = 'Order';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//5
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Order_H;
	item.id = 'Order_H';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//6
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = CreateNODA;
	item.id = 'CreateNODA';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//7
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Setings;
	item.id = 'Setings';
	item.innerHTML = item.id;
	myNode.appendChild(item);
}

function SKR(){

	SDisplay();
}
//done
function MyWallets(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	eel.getMyWallets()(setMenu);
}

function Voiting(){
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	eel.GetVoitingSataus()(setMenu);
}
//done
function Voit(key){
	HDisplay();
	eel.Voit(key)();
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



eel.Start()(onAccount);
//done
eel.expose(setLogin);
function setLogin(name){
	short_username
	if (name.length > 10){
		name = name.substring(0, 10);
		name += '...';
	}
	document.getElementById("user_name").innerHTML = name;
	name = name.toUpperCase();
	document.getElementById("short_username").innerHTML = name[0] + name[1];
}

eel.expose(setWallet);
function setWallet(name){
	document.getElementById("nav_wal_l").appendChild(createLinear());
	var item = createItem();
	item.onclick = function() {onWallet(name)};
	item.id = name;
	item.innerHTML = item.id;
	document.getElementById("nav_wal_l").appendChild(item);
}

var Chat_Open_From = '';
var Chat_Open_Adr = '';
var Chat_Wallet = '';

async function onWallet(name){
	try{
		USEGRAF.run =0;
		await sleep(500);
	}catch(e){
		console.log(e);
	}
	GWal1 = name;
	Chat_Wallet = name;
	// Chat();
	document.getElementById("main").innerHTML = '';
	const myNode = document.getElementById("nav_menu_l");
	myNode.innerHTML = '';
	//1
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Chat;
	item.id = 'Chat';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//2
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Graph;
	item.id = 'Graph';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//3
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Tranzh_P;
	item.id = 'Tranzh_P';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//4
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Order_A;
	item.id = 'Order';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//5
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Order_H;
	item.id = 'Order_H';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	//6
	myNode.appendChild(createLinear());
	var item = createItem();
	item.onclick = Tranzh_H;
	item.id = 'Tranzh_H';
	item.innerHTML = item.id;
	myNode.appendChild(item);
	Chat();
}

function Chat(){1
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div></div>';
	SDisplay();
	eel.GetAddrisesOfWallet(Chat_Wallet,1)(Chat_0);
}
function Chat_0(dat) {
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div></div>';
	const myNode = document.getElementById("Chat_SKR");
	myNode.innerHTML = '';
	for (let Adr of dat){
		myNode.appendChild(createLinear());
		var item = createItem();
		item.className = "nav_element_chat";
		item.onclick = function (){
			Chat_Open_Adr = Adr[0];
			eel.GetMassagesOthors(Chat_Wallet,Chat_Open_Adr)(Chat_1);
		};
		item.innerHTML = "<div>" + Adr[0] + "</div><div>" + Adr[1]+"</div>";
		myNode.appendChild(item);
	}
}
function Chat_1(dat) {
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"><div id="Chat_Back">Back</div></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div></div>';
	const myNode = document.getElementById("Chat_SKR");
	document.getElementById('Chat_Back').onclick = function(){
		eel.GetAddrisesOfWallet(Chat_Wallet,1)(Chat_0);
	};
	myNode.innerHTML = '';
	for (let Adr2 of dat){
		myNode.appendChild(createLinear());
		var item = createItem();
		item.className = "nav_element_chat";
		item.onclick = function (){
			Chat_Open_From = Adr2;
			eel.GetMassages(Chat_Wallet,Chat_Open_Adr,Chat_Open_From)(Chat_2);
		};
		item.innerHTML = Adr2;
		myNode.appendChild(item);
	}

}
function Chat_2(dat) {
	document.getElementById("main").innerHTML = '<div id="Chat_Window"><div id="Chat_Up_Bar"><div id="Chat_Back">Back</div></div><div id="Chat_SKR_l"><div id="Chat_SKR"></div></div><div class = "Send"><div class = "Send_Msg"><input class ="Send" id="Send_Msg" placeholder="Text" type ="text"></div><div class = "Send_Sum"><input id="Send_Sum" class ="Send" placeholder="Sum" type ="text"></div><input class ="Send_Btn" id="Send_Btn" value="Send" type ="button"></div></div>';
	document.getElementById("Chat_SKR_l").style.overflow = 'scroll';
	document.getElementById("Chat_SKR_l").style.bottom = '40px';
	document.getElementById("Chat_Window").style.overflow = 'hidden';
	document.getElementById('Send_Btn').onclick = function(){
		var Msg = document.getElementById("Send_Msg").value;
		var Sum = document.getElementById("Send_Sum").value;
		eel.Send(Chat_Wallet,Chat_Open_Adr,Chat_Open_From,Sum,Msg)();
	};
	document.getElementById('Chat_Back').onclick = function(){
		eel.GetMassagesOthors(Chat_Wallet,Chat_Open_Adr)(Chat_1);
	};

	const myNode = document.getElementById("Chat_SKR");
	myNode.innerHTML = '';
	for (let Msg of dat){
		var item = document.createElement( 'div' );
		myNode.appendChild(createLinear());
		if(Msg[3]){
			item.innerHTML = "<div class = 'Msg_Cont' id = 'in' ><div class = 'Msg_Text'>" + Msg[0] + "</div><div class = 'Msg_Sum'>" + Msg[1] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + Msg[2] + "</div></div>";
		}else{
			item.innerHTML = "<div class = 'Msg_Cont' id = 'out' ><div class = 'Msg_Text'>" + Msg[0] + "</div><div class = 'Msg_Sum'>" + Msg[1] + ' ' + Chat_Wallet + "</div><div class = 'Msg_Time'>" + Msg[2] + "</div></div>";
		}
		myNode.appendChild(item);
	}

}

async function Graph(){
	HDisplay();
	SearchWallets(list = 'nav_menu_l',type = 0,func = async function(GWal1,GWal2) {
		console.log(GWal1);
		document.getElementById("TypeOfOperstion").innerHTML = '<option value="1">Buy ' + GWal1 + '</option><option value="2">Buy ' + GWal2 + '</option>';

		document.getElementById("div_AdrFrom").innerHTML = GWal1 + ' Address : <select id="AdrFrom"></select>';
		let x = await eel.GetAddrisesOfWallet(GWal1)();
		for (let arc of x){
			let le = arc.length;
			if(20<le){le = 20}
			document.getElementById("AdrFrom").innerHTML += '<option value="'+ arc +'">' + arc.substr(0, le) + '</option>';
		}

		// document.getElementById("TypeOfOperstion").innerHTML
		document.getElementById("div_AdrTo").innerHTML = GWal2 + ' Address : <select id="AdrTo" value="Receiving Address"></select>';
		x = await eel.GetAddrisesOfWallet(GWal2)();
		for (let arc of x){
			let le = arc.length;
			if(20<le){le = 20}
			document.getElementById("AdrTo").innerHTML += '<option value="'+ arc +'">' + arc.substr(0, le) + '</option>';
		}
		// <option value="1">test1</option>
		// let a = eel.GetAddrisesOfWallet(GWal1)(setMenu);
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
		eel.SendOrder_1(adrfrom,adrto,sum,price,GWal1,GWal2)();
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
function CreateORDER_L(){
}
//done
function Wallet_D(Wallet,Address){

	eel.Wallet_D(Wallet,Address)
}
//done
function Tranzh_P(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	eel.Tranzh_P(GWal1)(setMenu)
}
//done
function Order_A(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	if (GWal1 == ''){
		SearchWallets(list = 'window',type = 1,func = function(GWal1,GWal2) {eel.Order_A(GWal2)(setMenu)});
	}else{
		eel.Order_A(GWal1)(setMenu);
	}
}
//done
function Order_H(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	if (GWal1 == ''){
		SearchWallets(list = 'window',type = 1,func = function(GWal1,GWal2) {eel.Order_H(GWal2)(setMenu)});
	}else{
		eel.Order_H(GWal1)(setMenu);
	}
}
//done
function Tranzh_H(){
	SDisplay();
	document.getElementById("main").innerHTML = '<div id="main_t_l"><div id="main_t"></div></div>';
	eel.Tranzh_H(GWal1)(setMenu)
}



function SDisplay(){
	if(Display == 0){
		Display = 1;
		var link = document.getElementById('display');
		// link.style.display = 'none'; //or
		link.style.opacity = 1.0;
	}
}

function HDisplay(){
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
	eel.Send(Wal,Adr1,Adr2,Sum,Msg,0)();
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
				var cRect = c.getBoundingClientRect();    // Gets CSS pos, and width/height
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
				eel.GrafLineal(this)(Graf.DrawGrafLineal);
			}

			if(this.Type == 2){
				eel.GrafCandle(this)(Graf.DrawGrafCandle);
			}
			eel.GetPrices(GWal1, WalletsPrice)(ShowPrices);
			if(this.Type != 1){
				if(!USEGRAF.run){break;}
				for (let i=0;i<60;i++){
					if (this.Wal1 != GWal1 || this.Wal2 != GWal2){
						break;
					}
					await sleep(500);
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
		// console.log(dat);
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
