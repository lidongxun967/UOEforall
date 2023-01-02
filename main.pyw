import wmi,re,os
import json
import os
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

with open('run.json', 'r') as run:
    runz=json.loads(run.read())

with open('run.json', 'w+') as run:
    runz['PID']=os.getpid()
    js = json.dumps(runz, sort_keys=True, indent=4, separators=(',', ':'))
    run.write(js)

raw_wql ="SELECT * FROM __InstanceCreationEvent WITHIN 2 WHERE TargetInstance ISA \'Win32_USBHub\'"
c = wmi.WMI ()
watcher = c.watch_for(raw_wql=raw_wql)
while 1:
    usb = watcher ()
    with open('run.json', 'r') as run:
        runz=json.loads(run.read())

    with open('run.json', 'w+') as run:
        runz['PID']=os.getpid()
        js = json.dumps(runz, sort_keys=True, indent=4, separators=(',', ':'))
        run.write(js)
    q = wmicu(usb)
    try:
        os.system(f"start {runz[q['DeviceID']]}")
        print("qqm")
    except  :
        pass
    