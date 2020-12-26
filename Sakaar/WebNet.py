from threading import Thread
import os,json,socket
from time import time as time_time, sleep as time_sleep
from random import randint
from sqlite3 import connect as sql3connect
from shelve import open as shelve_open
from requests import post as requests_post
from base64 import b64decode, b64encode
Path = os.path.dirname(__file__)

conn = sql3connect(Path + '/Out_Data_Base.db')
c = conn.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS API_Wallet(
	Symbol			Text	NOT NULL,
	Registr			Text	NOT NULL,
	Registr_1		Text	NOT NULL,
	Registr_R		Text	NOT NULL,
	Registr_R_1		Text	NOT NULL,
	Registr_R_2		Text	NOT NULL,
	GetBalance		Text	NOT NULL,
	GetBalance_1	Text	NOT NULL,
	GetBalance_R	Text	NOT NULL,
	GetBalance_R_1	Text	NOT NULL,
	Send        	Text	NOT NULL,
	Send_1	        Text	NOT NULL,
	Send_2	        Text	NOT NULL,
	Send_3	        Text	NOT NULL,
	Send_4	        Text	NOT NULL,
	Send_R	        BOOL	NOT NULL,
	TCP_HTTP		Text	NOT NULL,
	HTTP_Registr	Text	NOT NULL,
	HTTP_Balance	Text	NOT NULL,
	HTTP_Send		Text	NOT NULL,
	TCP_Address		Text	NOT NULL,
	TCP_PORT		Text	NOT NULL
	) ''')
conn.commit()
conn.close()


def sha256_16(x):

	return hashlib.sha256(str(x).encode()).hexdigest()


class Wallet_Out:
	def __init__ (self):
		Symbol = input("Введите символ(SKR) : ")

		Registr_API = input("Введите API для Регистраций в виде одной строки \n : ")
		Registr_API_1 = input("Под каким Ключем вставлять Ключевое слово или Пароль : ")
		Registr_API_R = input("Введите API получаемый после Регистраций в виде одной строки \n : ")
		Registr_API_R_1 = input("Под каким Ключем информация о Адресе кошелька \n : ")
		Registr_API_R_2 = input("Под каким Ключем информация о Публичном ключе \n : ")

		GetBalance_API = input("Введите API для Получения Баланса в виде одной строки \n : ")
		GetBalance_API_1 = input("Под каким Ключем вставлять Адресс Кошелька : ")
		GetBalance_API_R = input("Введите API получаемый после Получения Баланса в виде одной строки \n : ")
		GetBalance_API_R_1 = input("Под каким Ключем информация о Балансе \n : ")

		Send_API = input("Введите API для Отправки в виде одной строки \n : ")
		Send_API_1 = input("Под каким Ключем вставлять Адресс Кошелька Отправителя : ")
		Send_API_2 = input("Под каким Ключем вставлять Адресс Кошелька Получателя : ")
		Send_API_3 = input("Под каким Ключем вставлять Сумму Для Отправки : ")
		Send_API_4 = input("Под каким Ключем вставлять Приватный Ключ или Пароль Для Отправки : ")
		Send_API_R = (input("Есть ли обратное сообшение после отправки (Y/n): ").upper()[0] == 'Y')

		while(True):
			tcp_http = input("Каким образи идет обмен сообшениями TCP или HTTP (Введите вид отправки) \n : ")
			if tcp_http == "TCP":
				tcp_address = input("TCP Адресс отправки (0.tcp.ngrok.io) : ")
				tcp_port = input("TCP порт отправки (10101) : ")
				break
			elif tcp_http == "HTTP":
				http_reg = input("HTTP Адресс отправки для Регистраций (https://www.youtube.com/Registr) : ")
				http_bal = input("HTTP Адресс отправки для Получения Баланса (https://www.youtube.com/getBalance) : ")
				http_sen = input("HTTP Адресс отправки для Отправки (https://www.youtube.com/Send) : ")
				break

		conn = sql3connect(Path + '/Out_Data_Base.db')
        c = conn.cursor()
        c.execute('''CREATE TABLE IF NOT EXISTS API_Wallet(
			Symbol			Text	NOT NULL,
		    Registr			Text	NOT NULL,
		    Registr_1		Text	NOT NULL,
			Registr_R		Text	NOT NULL,
			Registr_R_1		Text	NOT NULL,
			Registr_R_2		Text	NOT NULL,
		    GetBalance		Text	NOT NULL,
		    GetBalance_1	Text	NOT NULL,
		    GetBalance_R	Text	NOT NULL,
		    GetBalance_R_1	Text	NOT NULL,
		    Send        	Text	NOT NULL,
		    Send_1	        Text	NOT NULL,
		    Send_2	        Text	NOT NULL,
		    Send_3	        Text	NOT NULL,
		    Send_4	        Text	NOT NULL,
		    Send_R	        BOOL	NOT NULL,
			TCP_HTTP		Text	NOT NULL,
			HTTP_Registr	Text	NOT NULL,
			HTTP_Balance	Text	NOT NULL,
			HTTP_Send		Text	NOT NULL,
			TCP_Address		Text	NOT NULL,
			TCP_PORT		Text	NOT NULL
			) ''')
        conn.commit()
        c.execute(f'''SELECT Address FROM API_Wallet WHERE Symbol = '{Symbol}' ''')
        if c.fetchone() is None:
            c.execute(f'''INSERT OR IGNORE INTO API_Wallet VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', (
				Symbol,
				Registr_API,
				Registr_API_1,
				Registr_API_R,
				Registr_API_R_1,
				Registr_API_R_2,
				GetBalance_API,
				GetBalance_API_1,
				GetBalance_API_R,
				GetBalance_API_R_1,
				Send_API,
				Send_API_1,
				Send_API_2,
				Send_API_3,
				Send_API_4,
				Send_API_R,
				tcp_http,
				http_reg,
				http_bal,
				http_sen,
				tcp_address,
				tcp_port
			))
        conn.commit()
        conn.close()
    def FromSQL(Symbol):
		conn = sql3connect(Path + '/Out_Data_Base.db')
		c = conn.cursor()
        x = c.execute(f'''SELECT * From Orders WHERE Symbol = '{Symbol}' ''').fetchall()[0]
        return {
		'Symbol' : x[0],

		'Registr':json.loads(x[1]),
		'Registr_1':x[2],
		'Registr_R':x[3],
		'Registr_R_1':x[4],
		'Registr_R_2':x[5],

		'GetBalance':json.loads(x[6]),
		'GetBalance_1':x[7],
		'GetBalance_R':x[8],
		'GetBalance_R_1':x[9],

		'Send':json.loads(x[10]),
		'Send_1':x[11],
		'Send_2':x[12],
		'Send_3':x[13],
		'Send_4':x[14],
		'Send_R':x[15],

		'TCP_HTTP':x[16]
		'HTTP_Registr':x[17],
		'HTTP_GetBalance':x[18],
		'HTTP_Send':x[19],
		'TCP_Address':x[20],
		'TCP_PORT':x[21]
		}

class WalleT:
	def Send(dat,wall_data,type):
		if wall_data['TCP_HTTP'] == "TCP":
			sock = socket.socket()
			sock.connect((wall_data['TCP_Address'],int(wall_data['TCP_PORT'])))
			sock.send(json.dumps(dat).decode())
			res = b''
			while(True):
				data = conn.recv(BUFFER_SIZE)
				if not data: break
				res += data
			sock.close()
			return res.encode()
		elif wall_data['TCP_HTTP'] == "HTTP":
			res = requests_post(wall_data['HTTP_' + type], json = dat)
			res = res.json()
			return res

	def __init__ (self,symbol,KEY,AddressTo):
		self.symbol = symbol.upper()
		self.AddressTo = AddressTo
		Password = sha256_16(KEY)
		wall_data = Wallet_Out.FromSQL(symbol.upper())
		Registr_API = wall_data['Registr']
		Registr_API[wall_data['Registr_1']] = Password
		res_data = WalleT.Send(Registr_API,wall_data,"Registr")
		self.Priv = Password
		self.Pub = res_data[wall_data['Registr_R_1']]
		self.Adr = res_data[wall_data['Registr_R_2']]

	def getBalance(Adr,symbol):
		wall_data = Wallet_Out.FromSQL(symbol.upper())
		GetBalance_API = wall_data['GetBalance']
		GetBalance_API[wall_data['GetBalance_1']] = Adr
		res_data = WalleT.Send(GetBalance_API,wall_data,"GetBalance")
		return res_data[wall_data['GetBalance_R_1']]

	def Send(self,AdrTo,Sum,gas = '50'):
		wall_data = Wallet_Out.FromSQL(self.symbol)
		Send_API = wall_data['Send']
		Send_API[wall_data['Send_1']] = self.Adr
		Send_API[wall_data['Send_2']] = AdrTo
		Send_API[wall_data['Send_3']] = Sum
		Send_API[wall_data['Send_4']] = self.Priv
		WalleT.Send(Send_API,wall_data,"Send")

	def save(self):
		if not os.path.exists(conf.conf['Link']+'//Out'):
			os.mkdir(conf.conf['Link']+'//Out')
		if not os.path.exists(conf.conf['Link']+'//Out//'+self.symbol):
			os.mkdir(conf.conf['Link']+'//Out//'+self.symbol)
		# if os.path.exists(conf.conf['Link']+'//'+str(self.Wallet)+'//'+str(self.Address)+'.usr'):
		# 	os.remove(conf.conf['Link']+'//'+str(self.Wallet)+'//'+str(self.Address)+'.usr')
		with open(conf.conf['Link']+'//Out//'+self.symbol+'//'+str(self.Adr)+'.usr', 'wb') as f:
			pickle.dump(self, f)

def get_account(Address,symbol):
	kke = None
	Address = str(Address)
	symbol = str(symbol)
	if os.path.exists(conf.conf['Link'] + '//Out//'+symbol+'//'+Address+ '.usr'):
		with open(conf.conf['Link'] + '//Out//'+symbol+'//'+Address+ '.usr', 'rb') as input:
			kke = pickle.load(input)
	return kke
