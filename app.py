from flask import Flask, render_template, jsonify, abort, request
from flask_cors import CORS
import json
from requests import get
from datetime import datetime, timezone

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
    return jsonify(data["sensores"])

#POST
@app.route(uriS + '/<int:id>/<float:value>', methods=['POST'])
def add_value(id, value):
    data = openFile()
    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data["sensores"] if sensor['id'] == id]
    #Para el valor de time dentro de un registro
    now = datetime.now(timezone.utc)

    if this_sensor:
        #Para el valor de day del sensor
        currentDate = datetime.date(now)
        this_date = [date for date in this_sensor[0]["inf"] if date["day"] == str(currentDate)]

        if this_date:
            this_date[0]["data"]["times"].append(str(now))
            this_date[0]["data"]["values"].append(value)

        else:
            this_sensor[0]["inf"].append(
                {
                    "day": str(currentDate),
                    "data": {
                        "times": [str(now)],
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
        if this_sensor[0]["inf"]:
            dict = {
                "id": this_sensor[0]["id"], 
                "name": this_sensor[0]["name"], 
                "min" : this_sensor[0]["min"],
                "max" : this_sensor[0]["max"],
                "value": this_sensor[0]["inf"][-1]["data"]["values"][-1], 
                "suffix": this_sensor[0]["suffix"], 
                "description": this_sensor[0]["description"]
            }
            return jsonify(dict)
        else:
            return "No Data"
    
    else:
        abort(404)

#Ultima fecha y tiempo
@app.route(uriS + '/last', methods=['GET'])
def utlima_fecha():
    data = openFile()
    #Buscar sensor en el json
    this_sensor = data["sensores"][0]

    if this_sensor:
        if this_sensor["inf"]:
            dict = {
                "date": this_sensor["inf"][-1]["day"], 
                "time": this_sensor["inf"][-1]["data"]["times"][-1]
            }
            return jsonify(dict)
        else:
            return "No Data"
    
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