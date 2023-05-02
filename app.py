from flask import Flask, render_template, jsonify, abort, request
from flask_cors import CORS
import json
from requests import get

app = Flask(__name__)

#enable CORS
CORS(app)

uriS = '/api/sensores'
uriU = '/api/usuarios'

def openFile():
    with open('data.json', 'r') as file:
        data = json.load(file)
    return data

def save(data):
    with open('data.json', 'w') as file:
        json.dump(data, file)

def saveUsers(data):
    with open('users.json', 'w') as file:
        json.dump(data, file)

#HOME----------------------------------------------------------------
#GET ALL
@app.route(uriS, methods=['GET'])
def home():
    data = openFile()

    device_eui = '2CF7F1C04350014D'
    user = 'NAM2OM6AZSLWE733'
    password = '29F2DB070C804D8BA5D2DB268452BE24517C9789F458452CA199022C3C94EA1A'
    response = get(f'https://sensecap.seeed.cc/openapi/view_latest_telemetry_data?device_eui={device_eui}', auth = (user, password)).json()
    print(response)
    
    return jsonify(data)

#POST
@app.route(uriS + '/<int:id>/<float:value>', methods=['POST'])
def add_value(id, value):
    data = openFile()

    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data if sensor['id'] == id]
    if this_sensor:
        this_sensor[0]["values"].append(value)
        
        save(data)
    else:
        abort(404)
    
    return "ok"

#USUARIOS-----------------------------------------------------------
#GET
@app.route(uriU, methods=['GET', 'POST'])
def usuarios():
    with open('users.json', 'r') as file:
        users = json.load(file)

    if request.method == 'POST':
        if request.json:
            if ((request.json["username"] != '' and not(request.json["username"].isspace())) and (request.json["password"] != '' and not(request.json["password"].isspace()))):
                user = {
                    "username": request.json["username"],
                    "password": request.json["password"]
                }
                users.append(user)
                saveUsers(users)
                
                return jsonify(users)
            else:
                return abort(404)
    elif request.method == 'GET':
        return jsonify(users) 



if __name__ == '__main__':
    app.run(debug = True)
