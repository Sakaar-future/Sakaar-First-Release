import subprocess
import pip
conf = None
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
code = 82 # restart
def get_conf():
    # pass
    global conf
    conf = getattr(conf,'_conf',None)
    if conf is None:
        conf = shelve.open('conf')
    return conf
get_conf()
while code == 82:
    if conf['Version'] is None:
        pass
    else:
        install("Sakaar=="+conf['Version'])
    try:
        process = subprocess.Popen(['python',"Controler.py"])
        process.wait()
        code = process.returncode
    except Exception as e:
        pass
    try:
        process = subprocess.Popen(['python3',"Controler.py"])
        process.wait()
        code = process.returncode
    except Exception as e:
        pass
