import subprocess
import sys

# ฟังก์ชันช่วยรันคำสั่ง shell
def run(cmd):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=True)
    return result


try:
    run(f"{sys.executable} -m pip install --upgrade pip")
    run(f"{sys.executable} -m pip install -r requirements.txt")
except subprocess.CalledProcessError:
    print("requirements.txt failed")






