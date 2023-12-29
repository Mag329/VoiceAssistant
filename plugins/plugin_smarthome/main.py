import sys
sys.path.append(r'../')
from plugins.plugin_smarthome.smarthome import *
from additions import *

import pymorphy3


morph = pymorphy3.MorphAnalyzer(lang='ru')

def main(cmd, text):
    appliance = recognize_appliance(text)
    if appliance['type'] == 'device':
        appliance = appliance['device']
        
        # ip = Devices.query.filter_by(name=appliance).first().ip
        
        devices_db = Devices.query.filter().all()
        for device_db in devices_db:
            if device_db.name.lower() == appliance:
                ip = device_db.ip
                print_text(appliance, cmd, ip)
                work_with_device(appliance, cmd, ip)
            else:
                continue
            
        
    elif appliance['type'] == 'command':
        host = appliance['host']
        host = morph.parse(host)[0]
        host = host.normal_form
        device = appliance['device']
        
        devices_db = Devices.query.filter().all()
        for device_db in devices_db:
            if device_db.name.lower() == host:
                ip = device_db.ip
                print_text(host, device, ip)
                work_with_device(host, device, ip)
            else:
                continue
    else:
        return