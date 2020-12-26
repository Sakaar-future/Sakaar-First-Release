import subprocess
import pip,shelve
conf = None
def install(package):
    if hasattr(pip, 'main'):
        pip.main(['install', package])
    else:
        pip._internal.main(['install', package])
code = 81 # restart
def get_conf():
    # pass
    global conf
    conf = getattr(conf,'_conf',None)
    if conf is None:
        conf = shelve.open('conf')
    return conf

while code == 82 or code == 81:
    if code == 82:
        get_conf()
        if 'Version' not in conf:
            pass
        else:
            install("Sakaar=="+conf['Version'])
        conf['ExitCode'] = 1
        conf.close()
    try:
        process = subprocess.Popen(['python',"Controler.py"])
        process.wait()
    except Exception as e:
        pass
    try:
        process = subprocess.Popen(['python3',"Controler.py"])
        process.wait()
    except Exception as e:
        pass

    get_conf()
    try:
        code = conf['ExitCode']
    except:
        pass
    conf.close()
