from flask import Flask, request, jsonify
from flask_cors import CORS
from com_stm32v2 import setupSerial, recvLikeArduino, sendToArduino
from joystick_control import pilotage
import time

#init stm_32
stm = False
mode = "articulation"
articulation_old = 1
mode_pince = 1
articulation_select = {'0':7,'1':'mode_pince','4':2,'5':3,'6':4,'7':5,'8':6}
try:
   setupSerial(115200, "/dev/ttyACM0")
   stm = True
except Exception as e:
   stm = False
   print("running wo stm")
app = Flask(__name__)
CORS(app)

@app.route('/com/stockage',methods = ['POST', 'GET'])
def stockage():
   if request.method == 'POST':
      try:
         value = request.get_json()
         print("nouveau stockage : ", value['nouveau_stockage'])
         print("emplacements : ", value['emplacement'])
         stmok= False
         if stm:
            try:
               sendToArduino("this is a test")
               arduinoReply = recvLikeArduino()
               while (arduinoReply == 'XXX'):
                  arduinoReply = recvLikeArduino()
               print ("Reply %s" %(arduinoReply))
               stmok = True
            except Exception as e:
               stmok = False
            return jsonify({'status': "ok","statusSTM":stmok,'stm_value':str(arduinoReply),'confirmed_value':value})
         return jsonify({'status': "ok","statusSTM":stmok,'confirmed_value':value})
      except Exception as e:
         return jsonify({"status": "error","confirmed_value":str(e)})
   else:
       return "GET"


@app.route('/com/commande',methods = ['POST', 'GET'])
def commande():
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
         print("mode : ", value['mode'])
         print("commande numérique : ",value['commande_numerique'])
         stmok = False
         if stm:
            try:
               sendToArduino("this is a test")
               arduinoReply = recvLikeArduino()
               while (arduinoReply == 'XXX'):
                  arduinoReply = recvLikeArduino()
               print ("Reply %s" %(arduinoReply))
               stmok = True
            except Exception as e:
               stmok = False
            return jsonify({'status': "ok","statusSTM":stmok,'stm_value':str(arduinoReply),'confirmed_value':value})
         return jsonify({'status': "ok","statusSTM":stmok,'confirmed_value':value})
      except Exception as e:
         return jsonify({"status": "error","confirmed_value":str(e)})

@app.route('/com/connexion',methods = ['POST', 'GET'])
def connexion():
   if request.method == 'POST':
      try:
         value = request.get_json()
         print("mode : ", value['mode'])
         print("information : ",value['information'])
         stm = False
         if stm:
            try:
               sendToArduino("this is a test")
               arduinoReply = recvLikeArduino()
               while (arduinoReply == 'XXX'):
                  arduinoReply = recvLikeArduino()
               print ("Reply %s" %(arduinoReply))
               stmok = True
            except Exception as e:
               stmok = False
            return jsonify({'status': "ok","statusSTM":stmok,'stm_value':str(arduinoReply),'confirmed_value':value})
         return jsonify({'status': "ok","statusSTM":stmok,'confirmed_value':value})

      except Exception as e:
         return jsonify({"status": "error","confirmed_value":str(e)})
   else:
       return "GET"

@app.route('/com/joystick',methods = ['POST', 'GET'])
def joystick():
   debut = time.time()
   global mode
   global articulation_old
   global mode_pince
   vmax = 20
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
         try:
            articulation_old, mode_pince, pilot = pilotage(articulation_old, mode_pince, mode, value, vmax)
            print(articulation_old)
            print(pilot)
         except:
            pilot = {'mode':'stop','vitesses':[0,0,0,0,0,0,0]}

         stmok = False
         if stm:
            try:
               sendToArduino(pilot)
               arduinoReply = recvLikeArduino()
               while (arduinoReply == 'XXX'):
                  arduinoReply = recvLikeArduino()
               print ("Reply %s" %(arduinoReply))
               stmok = True
            except Exception as e:
               stmok = False
            print(time.time() - debut)
            return jsonify({'status': "ok","statusSTM":stmok,'stm_value':str(arduinoReply),'confirmed_value':pilot})
         print(time.time() - debut)
         return jsonify({'status': "ok","statusSTM":stmok,'confirmed_value':pilot})
      except Exception as e:
         return jsonify({"status": "error","confirmed_value":str(e)})
@app.route('/com',methods = ['POST', 'GET'])
def com():
   if request.method == 'POST':
      print("ok")
   else:
       return jsonify({"method":"GET"})


if __name__ == '__main__':
   app.run(host='0.0.0.0', port='8000')
