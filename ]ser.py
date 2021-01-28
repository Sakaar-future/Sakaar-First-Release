from Sakaar import *
import pickle

print('Start')

# Link = 'DB';
conf.conf['isServer'] = True
conf.conf['isRunning'] = True
conf.conf['isSUPER'] = True
# variable = Thread(target = Server_Ent, args = ())
# variable.start()
CreateAccount('StiveMan1', '0')
Login('StiveMan1', '0')
AddWallet('SKR')
# time_sleep(2000)
RegistrNewWallet('SKR')
conn = sql3connect(Path + '/exmp1.db')
c = conn.cursor()
kke1 = get_UserOF(conf.conf['login'])
c.execute(f'''UPDATE SKR SET Balance= 20000000 WHERE Address = '{kke1['Balance']['SKR'][0][0]}' ''')
conn.commit()
conn.close()
SendTONODA('StiveMan1', 5000)
Activate('StiveMan1')
LogOut()
CreateAccount('GrandBull', '2271105')
Login('GrandBull', '2271105')
AddWallet('SKR')
RegistrNewWallet('SKR')
conn = sql3connect(Path + '/exmp1.db')
c = conn.cursor()
kke1 = get_UserOF(conf.conf['login'])
c.execute(f'''UPDATE SKR SET Balance= 20000000 WHERE Address = '{kke1['Balance']['SKR'][0][0]}' ''')
conn.commit()
conn.close()
SendTONODA('GrandBull', 5000)
print(conf.conf['FullFreez'])
Activate('GrandBull')

# login = "GrandBull"
# password = "2271105"
# ngrok_ip = "4a9fb18ec3bf.ngrok.io"

# login =     input('Login : ')
# password =     input('Password : ')
ngrok_ip = '127.0.0.1:10101'
conf.conf['MyIP'] = [ngrok_ip, 'GrandBull']
conf.conf['isRunning'] = True
conf.conf['Connected'] = [[ngrok_ip, 'GrandBull']]
# conf.conf['MyIP'] = ngrok_ip;
# AddWallet('SKR')
# Login(login,password)
# Activate(login)
# GrandBull
# 2271105
