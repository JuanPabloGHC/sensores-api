from flask import Flask, render_template, jsonify, abort, request
from flask_cors import CORS
import json
from requests import get
from datetime import datetime

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
        json.dump(data, file["sensores"])

def saveUsers(data):
    with open('data.json', 'w') as file:
        json.dump(data, file["users"])

#HOME----------------------------------------------------------------
#GET ALL
@app.route(uriS, methods=['GET'])
def home():
    data = openFile()

    device_eui = '2CF7F1C04350014D'
    user = 'NAM2OM6AZSLWE733'
    password = '29F2DB070C804D8BA5D2DB268452BE24517C9789F458452CA199022C3C94EA1A'
    response = get(f'https://sensecap.seeed.cc/openapi/view_latest_telemetry_data?device_eui={device_eui}', auth = (user, password)).json()
    data_dict = {'temperatura': response['data'][0]['points'][0]['measurement_value'], 'humedad': response['data'][0]['points'][1]['measurement_value']}
    print(data_dict)
    return jsonify(data[0]["sensores"])

#POST
@app.route(uriS + '/<int:id>/<float:value>', methods=['GET'])
def add_value(id, value):
    data = openFile()
    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data[0]["sensores"] if sensor['id'] == id]
    now = datetime.now()
    if this_sensor:
        currentDate = str(now.day) + "-" + str(now.month)
        this_date = [date for date in this_sensor[0]["inf"] if date["day"] == currentDate]
        if this_date:
            this_date[0]["data"].append(
                {
                    "time": now.minute, 
                    "value": value
                }
            )
        else:
            this_sensor[0]["inf"].append(
                {
                    "day": currentDate,
                    "data": [
                        {
                            "time": now.minute,
                            "value": value
                        }
                    ]
                }
            )
    else:
        abort(404)
    
    return jsonify(data[0]["sensores"])

#POST
# @app.route(uriS + '/<int:id>/<float:value>', methods=['POST'])
# def add_value(id, value):
#     data = openFile()

#     #Buscar sensor en el json
#     this_sensor = [sensor for sensor in data if sensor['id'] == id]
#     if this_sensor:
#         this_sensor[0]["values"].append(value)
        
#         save(data)
#     else:
#         abort(404)
    
#     return "ok"

#USUARIOS-----------------------------------------------------------
#GET
@app.route(uriU, methods=['GET', 'POST'])
def usuarios():
    data = openFile()

    if request.method == 'POST':
        if request.json:
            if ((request.json["username"] != '' and not(request.json["username"].isspace())) and (request.json["password"] != '' and not(request.json["password"].isspace()))):
                user = {
                    "username": request.json["username"],
                    "password": request.json["password"]
                }
                data[0]["users"].append(user)
                return jsonify(data[0]["users"])
                # users.append(user)
                # saveUsers(users)
                
                # return jsonify(users)
            else:
                return abort(404)
    elif request.method == 'GET':
        return jsonify(data[0]["users"]) 



if __name__ == '__main__':
    app.run(debug = True)
