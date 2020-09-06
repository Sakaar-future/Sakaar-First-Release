import io

from base64 import b64encode
import eel
from Sakaar import *

class conf:

	conf = None

	def get_conf():
		# pass
		conf.conf = getattr(conf.conf,'_conf',None)
		if conf.conf is None:
			conf.conf = shelve_open('conf')
		return conf

conf.get_conf()

eel.init('web')
user = get_UserOF(conf.conf['login'])

# @eel.expose
# def dummy(dummy_param):
# 	print("I got a parameter: ", dummy_param)
# 	return "string_value", 1, 1.2, True, [1, 2, 3, 4], {"name": "eel"}
#
#@eel.expose
# def generate_qr(data):
# 	img = pyqrcode.create(data)
# 	buffers = io.BytesIO()
# 	img.png(buffers, scale=8)
# 	encoded = b64encode(buffers.getvalue()).Decode("ascii")
# 	print("QR code generation successful.")
# 	eel.start('main.html', size=(1000, 600))
# 	return "data:image/png;base64, " + encoded

class  Chat:
	Massages = []
	Adr1 = ''
	Adr2 = ''
	Wal = ''
	priv = ''

@eel.expose
def GetMassagesOthors(Wal,Adr):
	dat = getHTran(Wal,Adr)
	data = []
	for i in dat:
		if not PubToAdr(i[1]) in data:
			data.append(PubToAdr(i[1]))
	return data
@eel.expose
def GetMassages(Wal,Adr1,Adr2,tor = True):
	if Chat.Wal != Wal or Chat.Adr1 != Adr1 or Chat.Adr2 != Adr2 or tor:
		Chat.Wal = Wal
		Chat.Adr1 = Adr1
		Chat.Adr2 = Adr2
		Chat.Massages = []
		for kke in user['Balance'][str(Wal)]:
			if kke[0] == Adr1:
				Chat.priv = encode(PrivCode(kke[1], conf.conf['PrivKey']), 16)
				break
		dat = getHTran(Wal,Adr1,Adr2)
		data = []
		for i in dat:
			if (i[1] == AdrToPub(Adr1)):
				data.append([encode(PrivCode(i[10], Chat.priv), 256),i[3],i[6],False])
			else:
				data.append([encode(PrivCode(i[9], Chat.priv), 256),i[3],i[6],True])
		Chat.Massages = Chat.Massages + list(reversed(data))
	else:
		print('kek')
		dat = getHTran(Wal,Adr1,Adr2,Chat.Massages[0][1])
		data = []
		for i in dat:
			if (i[1] == AdrToPub(Adr1)):
				data.append([encode(PrivCode(i[10], Chat.priv), 256),i[3],i[6],False])
			else:
				data.append([encode(PrivCode(i[9], Chat.priv), 256),i[3],i[6],True])
		Chat.Massages = Chat.Massages + list(reversed(data))
	return Chat.Massages


@eel.expose
def Send(Wal,Adr1,Adr2,Sum,Msg,tor = True):
	if tor:
		SendTranzh(Tranzhs.Create(PreSendTranzh([[AdrToPub(Adr1), AdrToPub(Adr2), Wal, float(Sum), Chat.priv, Msg]])))
	else:
		for kke in user['Balance'][str(Wal)]:
			if kke[0] == Adr1:
				Priv = encode(PrivCode(kke[1], conf.conf['PrivKey']), 16)
				SendTranzh(Tranzhs.Create(PreSendTranzh([[AdrToPub(Adr1), AdrToPub(Adr2), Wal, float(Sum), Priv, Msg]])))






@eel.expose
def Start():
	eel.setLogin(conf.conf['login'])
	for i in user['Balance'].keys():
		eel.setWallet(i)

@eel.expose
def GetVoitingSataus():
	tr = ''
	tor = (conf.conf['login'] in conf.conf['Voited'])
	for i in conf.conf['Voiting'].keys():
		if tor:
			tr += '<div>'
			tr+='<div class="el_table">'+str(conf.conf['Voiting'][i][1])+'</div>'
			tr += '<div class="progress"><div class="progress-bar" role="progressbar" aria-valuenow="' + str(100 *conf.conf['Voiting'][i][0]/conf.conf['FullFreez'])+ '" aria-valuemin="0" aria-valuemax="100" style="width:' + str(100 *conf.conf['Voiting'][i][0]/conf.conf['FullFreez'])+ '%"></div></div>'
		else:
			tr += '<div onclick="Voit(\''+ str(i)+'\')">'
			tr+='<div class="el_table">'+str(conf.conf['Voiting'][i][1])+'</div>'

		tr += '</div>'
		tr += '<hr align="center" size="3" width="75%" color="purple">'
	return tr

@eel.expose
def Voit(key):

	VoteFor(key)

def CreateBlock_Wallet(Wallet,Address):
	tr = '<div>'
	tr += '<div class="el_table" onclick = "onWallet(\'' + str(Wallet) +'\')" id ="' + str(Wallet)+ '">' + str(Wallet) + '</div>'
	tr += '<div class="el_table" onclick = "showWallet(\''+str(Wallet)+'\', \'' + str(Address[0]) +'\')">' + str(getBalance(Wallet,Address[0])) + '</div>'
	tr += '<div class="el_table" onclick = "showWallet(\''+str(Wallet)+'\', \'' + str(Address[0]) +'\')">' + str(Address[0]) + '</div>'
	tr += '<div class="el_table" onclick = "showWallet(\''+str(Wallet)+'\', \'' + str(Address[0]) +'\')">Submit</div>'
	tr += '<div class="el_table" onclick = "Wallet_D(\''+str(Wallet)+'\', \'' + str(Address[0]) +'\')">Delete</div>'
	tr += '</div>'
	tr += '<hr align="center" size="3" width="75%" color="purple">'
	return tr
@eel.expose
def getMyWallets():
	tr = ''
	user = get_UserOF(conf.conf['login'])
	for i in user['Balance'].keys():
		for j in user['Balance'][i]:
			tr += CreateBlock_Wallet(i,j)
	return tr

@eel.expose
def CreateWallet(Wallet):

	RegistrNewWallet(Wallet)

@eel.expose
def Wallet_D(Wallet,Address):

	ANConACC(conf.conf['login'], Wallet, Address)

	user = get_UserOF(conf.conf['login'])

@eel.expose
def Tranzh_P(Wallet):
	dat = getATran(Wallet,conf.conf['login'])
	tr = ''
	for arc in dat:
		tr += '<div>'
		tr += '<div class="el_table">' +str(arc[0]) + '</div>'
		tr += '<div class="el_table">' +str(arc[1]) + '</div>'
		tr += '<div class="el_table">' +str(arc[2]) + '</div>'
		tr += '<div class="el_table">' +str(arc[3]) + '</div>'
		tr += '</div>'
		tr += '<hr align="center" size="3" width="75%" color="purple">'

	return tr

@eel.expose
def Tranzh_H(Wallet):
	dat = getHTran(Wallet,conf.conf['login'])
	tr = ''
	for arc in dat:
		tr += '<div>'
		tr += '<div class="el_table">' +str(arc[0]) + '</div>'
		tr += '<div class="el_table">' +str(arc[1]) + '</div>'
		tr += '<div class="el_table">' +str(arc[2]) + '</div>'
		tr += '<div class="el_table">' +str(arc[3]) + '</div>'
		tr += '<div class="el_table">' +str(arc[4]) + '</div>'
		tr += '</div>'
		tr += '<hr align="center" size="3" width="75%" color="purple">'

	return tr

dat_ActiveOrders = None
@eel.expose
def Order_A(Wallet):
	dat = getAOrder(Wallet,conf.conf['login'])
	global dat_ActiveOrders
	dat_ActiveOrders = dat
	tr = ''
	i = 0
	for arc in dat:
		tr += '<div>'
		tr += '<div class="el_table">' +str(arc[3]) + '</div>'
		tr += '<div class="el_table">' +str(arc[4]) + '</div>'
		tr += '<div class="el_table">' +str(arc[0]) + '</div>'
		tr += '<div class="el_table">' +str(arc[1]) + '</div>'
		tr += '<div class="el_table">' +str(arc[5]) + '</div>'
		tr += '<div class="el_table">' +str(arc[5]/arc[6]) + '</div>'
		tr += '<div class="el_table">' +str(arc[7]) + '</div>'
		tr += '<div class="el_table">' +str(arc[8]) + '</div>'
		tr += '<div class="el_table" onclick="eel.Order_D(' + str(i) + ')">remove</div>'
		tr += '</div>'
		tr += '<hr align="center" size="3" width="75%" color="purple">'
		i += 1

	return tr

@eel.expose
def Order_H(Wallet):
	dat = getHOrder(Wallet,conf.conf['login'])
	global dat_ActiveOrders
	dat_ActiveOrders = dat
	tr = ''
	i = 0
	for arc in dat:
		tr += '<div>'
		tr += '<div class="el_table">' +str(arc[4]) + '</div>'
		tr += '<div class="el_table">' +str(arc[2]) + '</div>'
		tr += '<div class="el_table">' +str(arc[3]) + '</div>'
		tr += '<div class="el_table">' +str(arc[5]) + '</div>'
		tr += '<div class="el_table">' +str(arc[0]) + '</div>'
		tr += '<div class="el_table">' +str(arc[1]) + '</div>'
		tr += '<div class="el_table" onclick="eel.Order_D(' + str(i) + ')">remove</div>'
		tr += '</div>'
		tr += '<hr align="center" size="3" width="75%" color="purple">'
		i += 1

	return tr

@eel.expose
def GetAddrisesOfWallet(Wal,tor = 0):
	dat = []
	if tor == 0:
		for i in user['Balance'][str(Wal)]:
			dat.append(i[0])
	else:
		for i in user['Balance'][str(Wal)]:
			dat.append([i[0],getBalance(Wal,i[0])])
	return dat

@eel.expose
def Order_D(stk):
	print (stk,type(stk))
	CancelOrder(Order.FromSQL(dat_ActiveOrders[stk]))

@eel.expose
def SendOrder_1(AdrFrom,AdrTo,sum,price,Wal1,Wal2):
	MakeOrder(AdrFrom,Wal1,sum,AdrTo,Wal2,price)

class Graf:
	mn = 0
	mx = 0
	k = 10
	tm = 1000
	t = 0.0
	data = []
	Wal1 = ''
	Wal2 = ''
	Wal2 = ''
	lastTime = ''
k = 1000
tm = 10

def getGrafData(Wal1, Wal2):
	try:
		if Graf.Wal1 != Wal1 or  Graf.Wal2 != Wal2:
			print('ERROR')
			Graf.Wal1 = Wal1
			Graf.Wal2 = Wal2
			Graf.data = []
			Graf.k = k
			Graf.tm = tm
			Graf.lastTime = k + tm
			Graf.mn = 0
			Graf.mx = 0
			Graf.t = time_time();
		else:
			Time = time_time()
			if (Graf.k != k or  Graf.tm != tm):
				Graf.k = k
				Graf.tm = tm
				lol_pop = Graf.data[len(Graf.data) - 1][1]
				Graf.data = Graf.data + list(getDataForGraf(Wal1, Wal2,lol_pop ,k + tm + lol_pop - Time))
			Time = time_time()
			Graf.lastTime = Time - Graf.t
			Graf.t = Time
		Graf.data = list(getDataForGraf(Wal1, Wal2,Graf.t,Graf.lastTime)) + Graf.data
		if len(Graf.data):
			Graf.mx = Graf.mn = float(Graf.data[0][0])
			for line in Graf.data:
				line = list(line)
				if float(Graf.t) - float(line[1]) >=0 and float(Graf.t) - float(line[1]) <= k + tm:
					line[0] = float(line[0])
					line[1] = float(line[1])
					Graf.mx = max(Graf.mx , float(line[0]))
					Graf.mn = min(Graf.mn , float(line[0]))
			Graf.mn = max(Graf.mn , 0)
			Graf.mx -= Graf.mn
			Graf.mx = max(1,Graf.mx)
			return 1
		return 0
	except Exception as e:
		print(e)
		return 0

@eel.expose
def GrafLineal(graf):
	global k,tm
	k = int(graf['graf_k'])
	tm = int(graf['graf_tm'])
	graf['dat'] = GrafLinealS(graf['h'], graf['w'], graf['Type'], graf['Wal1'], graf['Wal2'])
	graf['mn'] = Graf.mn;
	if Graf.mx:
		graf['posx'] = graf['h']/Graf.mx;
		graf['posy'] = graf['w']/k
	return graf

def GrafLinealS(height, width, tor, Wal1, Wal2):
	dat = []
	posy = 0
	if(getGrafData(Wal1, Wal2)):
		posx = height/Graf.mx;
		posy = width/k
		la = 0
		for line in reversed(Graf.data):
			if float(Graf.t) - float(line[1]) >=0 and float(Graf.t) - float(line[1]) <= k + tm:
				y = (Graf.t - float(line[1]))*posy
				x = height - (float(line[0])-Graf.mn)*posx
				y = width - float(y)
				# if(y >= 0 and y<=width) and (x >=0 and x <= height):
				le = len(dat)
				if(le > 0 and tor != 1):
					dat.append([y, dat[le-1][1]])
				dat.append([y, x])

		le = len(dat)
		if(le > 0 and tor != 1):
			dat.append([width, dat[le-1][1]])
		Pscale3 = Graf.mn + height*0.2/posx
		Pscale2 = Graf.mn + height*0.50/posx
		Pscale1 = Graf.mn + height*0.25/posx
		Tscale1 = Graf.t + width*0.2/posy
		Tscale2 = Graf.t + width*0.4/posy
		Tscale3 = Graf.t + width*0.6/posy
		Tscale4 = Graf.t + width*0.8/posy

		#Graf.mx - Now Wallet
		# print(dat)

	return dat

@eel.expose
def GrafCandle(graf):
	global k,tm
	k = int(graf['graf_k'])
	tm = int(graf['graf_tm'])
	graf['dat'] = GrafCandleS(graf['h'], graf['w'], graf['Wal1'], graf['Wal2'])
	graf['mn'] = Graf.mn;
	if Graf.mx:
		graf['posx'] = graf['h']/Graf.mx;
		graf['posy'] = graf['w']/k
		# print(Graf.data)
	return graf

def GrafCandleS(height, width, Wal1, Wal2):
	dat = []
	posy = 0
	if(getGrafData(Wal1, Wal2)):
		posx = height/Graf.mx;
		posy = width/k
		y = (Graf.t - float(Graf.data[0][1]))*posy
		x = height - (float(Graf.data[0][0])-Graf.mn)*posx
		y = width - float(y)
		dat = [[y-tm*posy, x, x, x, x, Graf.data[0][1]]]
		# tin in out mx mn
		i = 0
		for line in reversed(Graf.data):
			if float(Graf.t) - float(line[1]) >=0 and float(Graf.t) - float(line[1]) <= k + tm:
				y = (Graf.t - float(line[1]))*posy
				x = height - (float(line[0])-Graf.mn)*posx
				y = width - float(y)
				if(int(line[1]/tm) == int(dat[i][5]/tm)):
					dat[i][2] = x
					dat[i][4] = min(x, dat[i][4])
					dat[i][3] = max(x, dat[i][3])
				else:
					i+=1
					dat.append([y-tm*posy, x, x, x, x, line[1]])
		i = 0
		r = len(dat)
		while i+1<r:
			dat[i][2] = dat[i+1][1]
			dat[i][4] = min(dat[i+1][1], dat[i][4])
			dat[i][3] = max(dat[i+1][1], dat[i][3])
			i+=1

		Pscale3 = Graf.mn + height*0.2/posx
		Pscale2 = Graf.mn + height*0.4/posx
		Pscale1 = Graf.mn + height*0.6/posx
		Tscale1 = Graf.t + width*0.2/posy
		Tscale2 = Graf.t + width*0.4/posy
		Tscale3 = Graf.t + width*0.6/posy
		Tscale4 = Graf.t + width*0.8/posy

	#Graf.mx - Now Wallet
	# print(dat)
	return dat, tm*posy

@eel.expose
def GetPrices(Wal1, data):
	return GetPricesF(Wal1,data)
mods = ['custom','chrome', 'electron', 'edge']
for arc in mods:
	try:
		eel.start('index.html',mode = arc,size=(1000, 600))
		break
	except Exception as e:
		print(e)
# eel.start('reg.html', size=(350, 400))
