import os,json,bitcash,bit
from web3 import Web3, HTTPProvider
from web3.auto import w3
import hashlib
import conf
import pickle,Sakaar2
def sha256_16(x):

	return hashlib.sha256(str(x).encode()).hexdigest()


class ETH:
	web3 = None
	def Start():
		URL = 'https://mainnet.infura.io/v3/aee2a05c49874d37bbd54eccefa69adb'
		ETH.web3 = Web3(HTTPProvider(URL))
# ETH.Start()

class WalleT:
	def __init__ (self,symbol,KEY,AddressTo):
		self.symbol = symbol
		self.AddressTo = AddressTo
		if symbol in ['btcx']:
			k = bit.Key.from_hex(sha256_16(KEY))
			self.Priv = k.to_wif()
			self.Adr = k.address
		elif symbol in ['eth']:
			priv = sha256_16(KEY)
			self.Adr = Account.from_key(priv).address
			self.Priv = priv
		elif symbol in ['bch']:
			k = bitcash.Key.from_hex(sha256_16(KEY))
			self.Priv = k.to_wif()
			tor = 0
			res = ''
			adr = k.address
			for i in adr:
				if tor :
					res += i
				if i == ':':
					tor = 1
			self.Adr = res
		elif symbol in ['btc']:
			k = bitcash.Key.from_hex(sha256_16(KEY))
			self.Priv = Sakaar2.GetUnUsedAddress('SKR')
			self.Pub = Sakaar2.PrivToPub(self.Priv)
			self.Adr = Sakaar2.PubToAdr(self.Pub)
			print (self.Priv)
			print (self.Pub)
			print (self.Adr)



	def getBalance(Adr,symbol):
		kek = None
		if symbol in ['btcx']:
			kek = bit.network.satoshi_to_currency(bit.network.NetworkAPI.get_balance(Adr), 'btc')
		elif symbol in ['eth']:

			kek = ETH.web3.fromWei(ETH.web3.eth.getBalance(Adr),'ether')
		elif symbol in ['bch']:
			tor = 0
			res = ''
			tag = 'bitcoincash:'
			for i in Adr:
				if tor :
					res += i
				if i == ':':
					tor = 1
			if tor == 0 :
				Adr = tag+Adr
			else:
				Adr = tag+res
			kek = bitcash.network.satoshi_to_currency(bitcash.network.NetworkAPI.get_balance(Adr), 'bch')
		elif symbol in ['btc']:
			kek = Sakaar2.get_User(Adr,'SKR').Balance
		return kek

	def Send(self,AdrTo,Sum,gas = '50'):

		if self.symbol in ['btcx']:
			k = bitcash.Key(self.priv)
			outputs = [(AdrTo, Sum, 'btc')]
			k.send(outputs)
		elif self.symbol in ['eth']:
			nonce = ETH.web3.eth.getTransactionCount(self.Adr)
			tx = {
				'nonce':nonce,
				'to':AdrTo,
				'value': ETH.web3.toWei(Sum,'ether'),
				'gas':2000000,
				'gasPrice':ETH.web3.toWei(gas,'gwei'),
			}
			s_tx = ETH.web3.eth.account.signTransaction(tx,self.Priv)
			h_tx = ETH.web3.eth.sendRawTransaction(s_tx.rawTransaction)
		elif self.symbol in ['bch']:
			k = bitcash.Key(self.priv)
			tor = 0
			res = ''
			tag = 'bitcoincash:'
			for i in AdrTo:
				if tor :
					res += i
				if i == ':':
					tor = 1
			if tor == 0 :
				AdrTo = tag+AdrTo
			else:
				AdrTo = tag+res
			outputs = [(AdrTo, Sum, 'bch')]
			k.send(outputs)
		elif self.symbol in ['btc']:
			Sakaar2.SendTranzh(Sakaar2.Tranzhs(Sakaar2.PreSendTranzh([[self.Pub, Sakaar2.AdrToPub(AdrTo), 'SKR', Sum, self.Priv, 'LOL']])))
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
