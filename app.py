from flask import Flask, render_template, jsonify, abort, request
import json
from requests import get

app = Flask(__name__)

uriS = '/api/sensores'
uriU = '/api/usuarios'

with open('data.json', 'r') as file:
    data = json.load(file)

with open('users.json', 'r') as file:
    users = json.load(file)

#HOME----------------------------------------------------------------
#GET
@app.route(uriS, methods=['GET'])
def home():
    device_eui = '2CF7F1C04350014D'
    user = 'NAM2OM6AZSLWE733'
    password = '29F2DB070C804D8BA5D2DB268452BE24517C9789F458452CA199022C3C94EA1A'
    response = get(f'https://sensecap.seeed.cc/openapi/view_latest_telemetry_data?device_eui={device_eui}', auth = (user, password)).json()
    print(response)
    return jsonify(data)

#POST
@app.route(uriS + '/<int:id>/<float:value>', methods=['GET'])
def show_values(id, value):
    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data if sensor['id'] == id]
    if this_sensor:
        this_sensor[0]["values"].append(value)
    else:
        abort(404)
    
    return jsonify(this_sensor[0])

#USUARIOS-----------------------------------------------------------
#GET
@app.route(uriU, methods=['GET', 'POST'])
def usuarios():
    if request.method == 'POST':
        if request.json:
            if ((request.json["username"] != '' and not(request.json["username"].isspace())) and (request.json["password"] != '' and not(request.json["password"].isspace()))):
                user = {
                    "username": request.json["username"],
                    "password": request.json["password"]
                }
                users.append(user)
                return jsonify(users)
            else:
                return abort(404)
    elif request.method == 'GET':
        return jsonify(users) 



if __name__ == '__main__':
    app.run(debug = True)
