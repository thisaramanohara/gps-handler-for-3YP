from flask import Flask, request, jsonify
from flask_mqtt import Mqtt
import json

app = Flask(__name__)

app.config['MQTT_BROKER_URL'] = 'mqtt.eclipseprojects.io'
app.config['MQTT_BROKER_PORT'] = 1883
app.config['MQTT_KEEPALIVE'] = 5  # Set KeepAlive time in seconds

topic = '/3yp/flask/test'
landmines = []

mqtt_client = Mqtt(app)


@mqtt_client.on_connect()
def handle_connect(client, userdata, flags, rc):
   if rc == 0:
       print('Connected successfully')
       mqtt_client.subscribe(topic) # subscribe topic
   else:
       print('Bad connection. Code:', rc)


@mqtt_client.on_message()
def handle_mqtt_message(client, userdata, message):
   data = dict(
       topic=message.topic,
       payload=message.payload.decode()
    )
   data = json.loads(data['payload'])

   newLandmine = [data['lat'], data['lon']]
   landmines.append(newLandmine)
   print(landmines)

@app.route('/')
def sendLandmines():
    return "Welcome to GPS handler"

@app.route('/get-landmines', methods=['GET'])
def sendLandmines():
    return jsonify(landmines)

if __name__ == '__main__':
   app.run()
