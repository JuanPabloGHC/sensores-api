from flask import Flask, render_template, jsonify, abort, request
import json

app = Flask(__name__)

uri = '/api/sensores'

with open('data.json', 'r') as file:
    data = json.load(file)

#GET----------------------------------------------------------------
#HOME
@app.route(uri, methods=['GET'])
def home():
    return jsonify(data)

#POST--------------------------------------------------------------
@app.route(uri + '/<int:id>/<float:value>', methods=['GET'])
def show_values(id, value):
    #Buscar sensor en el json
    this_sensor = [sensor for sensor in data if sensor['id'] == id]
    if this_sensor:
        this_sensor[0]["values"].append(value)
    else:
        abort(404)
    
    return jsonify(this_sensor[0])



if __name__ == '__main__':
    app.run(debug = True)