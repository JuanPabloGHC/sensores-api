from flask import Flask, render_template, jsonify, abort, request
import json

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