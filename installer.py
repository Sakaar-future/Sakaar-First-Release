import pip

# packages = ['flask','pyngrok','requests']
# def install(package):
#	 if hasattr(pip, 'main'):
#		 pip.main(['install', package])
#	 else:
#		 pip._internal.main(['install', package])
# for arc in packages:
# 	install(arc)

import shelve,requests,os,base64
conf = None
def get_conf():
	# pass
	global conf
	conf = getattr(conf,'_conf',None)
	if conf is None:
		conf = shelve.open('conf')
	return conf
get_conf()
conf['Connected'] = ['96273a93bad1.ngrok.io']
conf['Version'] = '1.000'
conf['OurWallets'] = ['BTC','SKR']
systems = {
	2: '01',
	10: '0123456789',
	16: '0123456789abcdef',
	32: 'abcdefghijklmnopqrstuvwxyz234567',
	33: 'abcdefghijklmnopqrstuvwxyz2345670',
	64: '-0123456789QWERTYUIOPASDFGHJKLZXCVBNMqwertyuiopasdfghjklzxcvbnm_',
	256: ''.join([chr(x) for x in range(256)])
}
def get_code_string(base):
	if base in systems:
		return systems[base]
	else:
		raise ValueError("Invalid base!")
def encode(val, base, minlen=0):
	val = int(val)
	base, minlen = int(base), int(minlen)
	code_string = get_code_string(base)
	result = ''
	while val > 0:
		result = code_string[val % base] + result
		val //= base
	return code_string[0] * max(minlen - len(result), 0) + result

def Send_T1(dat,OUT = False): # Send to all
	if OUT == False:
		for ip in conf['Connected']:
			try:
				res = requests.post(f'http://{str(ip)}/', json = dat)
				if not res.json() is None:
					return res.json()
			except Exception as e:
				pass
	else:
		for ip in conf['SUPERIP']:
			try:
				res = requests.post(f'http://{str(ip)}/', json = dat)

				if not res.json() is None:
					return res.json()
			except Exception as e:
				pass

def GetUpDate():
	#Here if you use it your programm is like new virsion
	dat = Send_T1(GetUpDate_S())
	for x in dat['dirs']:
		if not os.path.exists(x):
			os.mkdir(x)
	for x in dat['files']:
		print (x)
		with open(x, 'wb') as f:
			f.write(base64.b64decode(bytes(dat['files'][x],'utf-8')))
def GetUpDate_S():

	return {'Protocol':'GetUpDate'}
def GetAllData():
	dat = Send_T1(GetAllData_S())
	for x in dat:
		print (x)
		with open(x, 'wb') as f:
			f.write(base64.b64decode(bytes(dat[x],'utf-8')))
def GetAllData_S():

	return {'Protocol':'GetAllData'}
def GetConf():
    dat = Send_T1(GetConf_S())
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
def GetConf_S():

    return {'Protocol':'GetConf'}

# GetAllData()
GetUpDate()
GetConf()
