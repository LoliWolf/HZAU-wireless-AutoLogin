import os
import time
import requests
import json
import win32api
import win32con
import psutil

urls = 'http://211.69.143.97/include/auth_action.php'
# 读用户数据
with open('config.json', encoding='utf-8') as config:
    jsonConfig = json.load(config)
    wlan = jsonConfig.get('wlan')
    username = jsonConfig.get('username')
    password = jsonConfig.get('password')
    rememberme = jsonConfig.get('remember-me')
    browser = jsonConfig.get('browser')

process = []
for proc in psutil.process_iter():
    if proc.name() == browser + '.exe':
        process.append(proc.pid)

# 连接到华农网络
command = 'netsh wlan connect name='+ wlan
os.popen(command)
flag = True
while flag:
    command = 'netsh interface show interface'
    info = os.popen(command).read()
    infolist = []
    string = ''
    for i in info:
        if i != '\n':
            string += i
        else:
            infolist.append(string)
            string = ''
    for i in infolist:
        if 'WLAN' in i:
            if '已连接' in i:
                flag = False
print('连网成功')
flag = True
while flag:
    time.sleep(0.5)
    for proc in psutil.process_iter():
        if proc.name() == browser + '.exe':
            if proc.pid not in process:
                flag = False
                break

payload = {'action': 'login', 'username': str(username), 'password': '{noop}' + str(password), 'ac_id': 5,
           'save_me': rememberme, 'ajax': 1}
resp = requests.request(method='POST', url=urls, data=payload)

# 模拟键盘操作关闭登录界面
win32api.keybd_event(17, 0, 0, 0)  # Ctrl
win32api.keybd_event(87, 0, 0, 0)  # W
win32api.keybd_event(87, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放指令
win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)
time.sleep(0.5)
win32api.keybd_event(18, 0, 0, 0)  # Alt
win32api.keybd_event(27, 0, 0, 0)  # Esc
win32api.keybd_event(27, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放指令
win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)

resp.encoding = 'utf-8'
response = resp.text
print(response)

if '欠' in response:
    command = 'netsh wlan disconnect'
    os.popen(command)
    os.system('pause')

exit(0)
