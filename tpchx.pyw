import pystray
import PIL.Image
import os
import json


image = PIL.Image.open("boxffffff.png")

def exit():
    with open('run.json', 'r') as run:
        pidz=json.loads(run.read())['PID']
    os.system(f"taskkill /PID {pidz} /f")
    os._exit(0)

def oj():
    os.system("start run.json")

def sz():
    with open('run.json', 'r') as run:
        pidz=json.loads(run.read())['SPID']
    os.system(f"taskkill /PID {pidz} /f")
    os.system("start python/pythonw.exe settings.pyw")

def click_menu():
    with open('run.json', 'r') as run:
        pidz=json.loads(run.read())['PID']
    os.system(f"taskkill /PID {pidz} /f")
    os.system("start python/pythonw.exe main.pyw")
    icon.notify("已刷新", "UOE")


icon = pystray.Icon("box",image,"UOE-单击刷新",pystray.Menu(
    pystray.MenuItem("打开配置文件",oj),
    pystray.MenuItem("设置",sz),
    pystray.MenuItem("退出",exit),
    pystray.MenuItem('',click_menu, default=True, visible=False)
))

click_menu()
icon.run()