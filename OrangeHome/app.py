import threading
from flask import Flask, redirect, render_template, request
from flask_sqlalchemy import SQLAlchemy 

import json
import requests

import logging

import sys

sys.path.append(r'../')
import config



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///../instance/site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.app_context().push()

db = SQLAlchemy(app)

# Disable console log
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

class Devices(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    room = db.Column(db.String(100), nullable=False)
    ip = db.Column(db.String(100), nullable=False)
    # addresses = db.Column(db.Text, nullable=False)
    status = db.Column(db.String, default='True')
    
    
class Commands(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    command = db.Column(db.Text, nullable=False)
    device_id = db.Column(db.Integer, db.ForeignKey('devices.id'))
    
    
class Room(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    
    
    
@app.route('/', methods=['GET', 'POST'])
def index():
    return  render_template('index.html')


@app.route('/devices/', methods=['GET', 'POST'])
def devices():
    devices = Devices.query.order_by(Devices.id).all()
    commands = Commands.query.order_by(Commands.id).all()
    return render_template('devices.html', devices=devices, commands=commands)


@app.route('/device_add/', methods=['GET', 'POST'])
def device_add():
    if request.method == 'POST':
        name = request.form['name']
        room = request.form['room']
        ip = request.form['ip']
        # data_list = request.form['addresses']
        
        # data_list = data_list.split(", ")
        # data_dict = {}
        # for item in data_list:
        #     key, value = item.split(": ")  
        #     data_dict[key] = value
            
        # data_json = json.dumps(data_dict)

        article = Devices(name=name, room=room, ip=ip) # type: ignore
        
        try:
            db.session.add(article)
            db.session.commit()
            return redirect('/devices')
        except:
            return "При добавление устройства произошла ошибка"
    else:
        return render_template('device_add.html')


@app.route('/device/<int:id>')
def device_detail(id):
    device = Devices.query.get(id)
    commands = Commands.query.filter_by(device_id=id).all()
    return render_template('device_detail.html', device=device, commands=commands)


@app.route('/device/<int:id>/edit', methods=['POST', 'GET'])
def device_edit(id):
    device = Devices.query.get(id)
    if request.method == 'POST':
        device.name = request.form['name']
        device.room = request.form['room']
        device.ip = request.form['ip']
        
        # data_list = request.form['addresses']
        
        # data_list = data_list.split(", ")
        # data_dict = {}
        # for item in data_list:
        #     key, value = item.split(": ")  
        #     data_dict[key] = value
            
        # data_json = json.dumps(data_dict)
        
        # device.addresses = data_json
        
        
        
        try:
            db.session.commit()
            return redirect(f'/device/{id}')
        except:
            return "При изменении устройства произошла ошибка"
    else:
        return render_template('device_edit.html', device=device)
    


@app.route('/device/<int:id>/command_add', methods=['POST', 'GET'])
def command_add(id):
    if request.method == 'POST':
        key = request.form['key']
        value = request.form['value']

        command = Commands(name=key, command=value, device_id=id)
        
        try:
            db.session.add(command)
            db.session.commit()
            return redirect(f'/device/{id}')
        except:
            return "При добавление команды произошла ошибка"
    else:
        return render_template('command_add.html')
    
    
@app.route('/device/<int:id>/<int:command_id>/command_edit', methods=['POST', 'GET'])
def command_edit(id, command_id):
    command = Commands.query.get(command_id)
    if request.method == 'POST':
        command.name = request.form['key']
        command.command = request.form['value']
        
        try:
            db.session.commit()
            return redirect(f'/device/{id}')
        except:
            return "При изменение команды произошла ошибка"
    else:
        return render_template('command_edit.html', command=command)
    

@app.route('/device/<int:id>/<int:command_id>/command_delete', methods=['POST', 'GET'])
def command_delete(id, command_id):
    command = Commands.query.get_or_404(command_id)

    try:
        db.session.delete(command)
        db.session.commit()    
        return redirect(f'/device/{id}')
    except:
        return "При удалении команды произошла ошибка"


@app.route('/device/<int:id>/delete')
def device_delete(id):
    device = Devices.query.get_or_404(id)

    try:
        db.session.delete(device)
        db.session.commit()    
        return redirect('/devices')
    except:
        return "При удалении устройства произошла ошибка"
    
        
@app.route('/device/<int:id>/use', methods=['GET', 'POST'])
def device_use(id):
    name = Devices.query.get(id).name
    commands = Commands.query.filter_by(device_id=id).all()
    if request.method == 'POST':
        for data in request.form:
            if '/' in data:
                data = data.split('----')
                command = data[0]
                device_id = data[1]
                ip = Devices.query.filter_by(id=device_id).first().ip
                requests.get(f'http://{ip}{command}')

        
        return render_template('use.html', commands=commands, name=name)
    else:
        return render_template('use.html', commands=commands, name=name)
    
    


        
@app.route('/settings', methods=['GET', 'POST'])
def settings_page():
    settings = {}
    for key, value in config.__dict__.items():
        if not key.startswith('__'):
            settings[key] = value
            
    if request.method == 'POST':
        key_new = request.form['key']
        value_new = request.form['value']
        
        print(key_new)
        print(value_new)
        
        config.__dict__[key_new] = value_new
    
    else:
        return render_template('settings.html', settings=settings)    
    

   
   
    
@app.before_request 
def handle_request():
    if request.path.startswith("/api"): 
        path = request.path 
        if path.startswith("/"):
            path = path[1:]
            
        parts = path.split("/")
        target_ip = parts[1]
        route = "/".join(parts[2:])
        
        device = Devices.query.filter_by(ip=target_ip).first()

        if not device:
            return "Device not found", 404
            
        if route not in device.addresses:
            return "Forbidden route", 403
            
        full_path = request.full_path
        
        if "?" in full_path:
            path, params = full_path.split("?")
    
            if "password" not in params:
                return "'Password' not found", 403
            else:
                pwd = request.args.get("password") 
                if pwd != "WC76s_fp":
                    return "Password not correct", 403
        else:
            return "'Password' not found", 403
    
        url = f"http://{device.ip}/{route}"
        requests.get(url)
        return 'Well'
    else:
        return



    
thread = threading.Thread(target=app.run, kwargs={
    "host": "0.0.0.0",
    "debug": False,
    "port": 5200
})
db.create_all() 
print('\n\n')
thread.start()  

# if __name__ == "__main__":
#     db.create_all()  
#     app.run(host='0.0.0.0', debug=True, port=5200) 