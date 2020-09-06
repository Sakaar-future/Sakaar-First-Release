import subprocess
code = 82

while code == 82:
    process = subprocess.Popen(['python',"Sakaar"])
    process.wait()
    code = process.returncode
