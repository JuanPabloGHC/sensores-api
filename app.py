from flask import Flask, render_template, jsonify, abort, request
from flask_cors import CORS
import json
from requests import get
from datetime import datetime, date, timezone

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

#HOME----------------------------------------------------------------
@app.route('/')
def home():
    return render_template('index.html')

#SENSORES------------------------------------------------------------
#GET ALL
@app.route(uriS, methods=['GET'])
def homeS():
    data = openFile()

    # device_eui = '2CF7F1C04350014D'
    # user = 'NAM2OM6AZSLWE733'
    # password = '29F2DB070C804D8BA5D2DB268452BE24517C9789F458452CA199022C3C94EA1A'
    # response = get(f'https://sensecap.seeed.cc/openapi/view_latest_telemetry_data?device_eui={device_eui}', auth = (user, password)).json()
    # data_dict = {'temperatura': response['data'][0]['points'][0]['measurement_value'], 'humedad': response['data'][0]['points'][1]['measurement_value']}
    # print(data_dict)
    #add_valueS(1, float(response['data'][0]['points'][0]['measurement_value']))

    return jsonify(data["sensores"])

#POST
@app.route(uriS + '/<int:id>/<float:value>', methods=['POST'])
def add_value(id, value):
    data = openFile()
    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data["sensores"] if sensor['id'] == id]
    #Para el valor de time dentro de un registro
    now = datetime.now(timezone.utc)
    currentTime = datetime.time(now)
    if this_sensor:
        #Para el valor de day del sensor
        currentDate = datetime.date(now)
        this_date = [date for date in this_sensor[0]["inf"] if date["day"] == str(currentDate)]

        if this_date:
            this_date[0]["data"]["times"].append(str(currentTime))
            this_date[0]["data"]["values"].append(value)

        else:
            this_sensor[0]["inf"].append(
                {
                    "day": str(currentDate),
                    "data": {
                        "times": [str(currentTime)],
                        "values": [value]
                    } 
                }
            )
        save(data)
    else:
        abort(404)
    
    # return jsonify(data["sensores"])
    return "ok"

#Ultimo valor del sensor
@app.route(uriS + '/<int:id>', methods=['GET'])
def ultimo_registro(id):
    data = openFile()

    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data["sensores"] if sensor['id'] == id]

    if this_sensor:
        dict = {
            "name": this_sensor[0]["name"], 
            "value": this_sensor[0]["inf"][-1]["data"][-1]["values"][-1], 
            "suffix": this_sensor[0]["suffix"], 
            "description": this_sensor[0]["description"]
        }
        return jsonify(dict)
    
    else:
        abort(404)

#Ultima fecha y tiempo
@app.route(uriS + '/last', methods=['GET'])
def utlima_fecha():
    data = openFile()
    #Buscar sensor en el json
    this_sensor = data["sensores"][0]

    if this_sensor:
        dict = {
            "date": this_sensor["inf"][-1]["day"], 
            "time": this_sensor["inf"][-1]["data"][-1]["times"][-1]
        }
        return jsonify(dict)
    
    else:
        abort(404)

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
                save(data)

                return jsonify(data["users"])
            else:
                return abort(404)
    elif request.method == 'GET':
        return jsonify(data["users"]) 



if __name__ == '__main__':
    app.run(debug = True)
