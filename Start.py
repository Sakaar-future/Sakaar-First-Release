import subprocess
code = 82

while code == 82:
    process = subprocess.Popen(['python',"Controler.py"])
    process.wait()
    code = process.returncode
