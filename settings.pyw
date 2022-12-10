import easygui,sys
import wmi,re,os,time
import json



def wmicu(wmit):
    wmit=str(wmit)
    wmit=re.sub(";\n", ",\n",wmit)
    wmit=re.sub(' = ', """":""",wmit)
    wmit=re.sub('\t', """\t\"""",wmit)
    wmit=re.sub('\ninstance of Win32_USBHub\n', "",wmit)
    wmit=re.sub(',\n}', """\n}""",wmit)
    wmit=re.sub('FALSE', """"FALSE\"""",wmit)
    wmit=re.sub('TURE', """"TURE\"""",wmit)

    wmit=wmit[0:-2]
    return json.loads(wmit)

def rm():
    with open('run.json', 'r') as run:
        pidz=json.loads(run.read())['PID']
    os.system(f"taskkill /PID {pidz} /f")
    os.system("start python/pythonw.exe main.pyw")


with open('run.json', 'r') as run:
    runz=json.loads(run.read())
with open('run.json', 'w+') as run:
    runz['SPID']=os.getpid()
    js = json.dumps(runz, sort_keys=True, indent=4, separators=(',', ':'))
    run.write(js)




raw_wql ="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
c = wmi.WMI ()
watcher = c.watch_for(raw_wql=raw_wql)

while 1:
    a = easygui.buttonbox("选择功能", "UOE设置", ["添加设备", "删除设备"])
    if not a:
        sys.exit()
    
    if a=='添加设备':
        a=easygui.buttonbox("开始添加设备，请按下OK后插拔你的USB设备\n一部分设备不兼容此软件", "UOE设置-添加设备",['OK'])
        s=time.time()
        usb = watcher ()
        p = wmicu(usb)['DeviceID']
            
        if p:
            ret = easygui.fileopenbox("请选择插入此设备后要打开的文件（路径不能有空格）",'UOE','*',['*.*'],False)
            if ret:
                with open('run.json', 'r') as run:
                    runz=json.loads(run.read())
                with open('run.json', 'w+') as run:
                    runz[p]=ret
                    js = json.dumps(runz, sort_keys=True, indent=4, separators=(',', ':'))
                    run.write(js)
                rm()
    elif a=='删除设备':
        a=easygui.buttonbox("开始删除设备，请按下OK后插拔你的USB设备", "UOE设置-删除设备",['OK'])
        s=time.time()
        usb = watcher ()
        p = wmicu(usb)['DeviceID']
        if  easygui.ccbox('是否确认删除', 'UOE设置-确认删除',('是','否')):
            with open('run.json', 'r') as run:
                runz=json.loads(run.read())
            with open('run.json', 'w+') as run:
                runz[p]=None
                del runz[p]
                js = json.dumps(runz, sort_keys=True, indent=4, separators=(',', ':'))
                run.write(js)
            rm()