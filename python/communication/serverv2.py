from flask import Flask, request, jsonify
from flask_cors import CORS
from com_stm32v2 import setupSerial, recvLikeArduino, sendToArduino
from joystick_control import pilotage
import time
import RPi.GPIO as GPIO

#init GPIO
GPIO.setmode(GPIO.BOARD)
GPIO.setup(32, GPIO.OUT)
pwm = GPIO.PWM(32, 1)


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

## Routes

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
         try:
            if value['commande_numerique']['eclairage']:
               pwm.start(100)
            if not value['commande_numerique']['eclairage']:
               pwm.stop()
         except Exception as e:
            pass
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
   else:
       return "GET"

@app.route('/com/brasmaitre',methods = ['POST', 'GET'])
def brasmaitre():
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
         print("mode : ", value['mode'])
         print("bars maitre : ",value['valeur'])
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
            return jsonify({'status': "ok","statusSTM":stmok,'stm_value':str(arduinoReply),'confirmed_value':pilot})
         return jsonify({'status': "ok","statusSTM":stmok,'confirmed_value':value})
      except Exception as e:
         return jsonify({"status": "error","confirmed_value":str(e)})



@app.route('/com/joystick',methods = ['POST', 'GET'])
def joystick():
   debut = time.time()
   global articulation_old
   global mode_pince
   vmax = .1
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
         try:
            articulation_old, mode_pince, pilot = pilotage(articulation_old, mode_pince, value, vmax)
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


## Test Routes

@app.route('/test/stockage',methods = ['POST', 'GET'])
def stockagetest():
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


@app.route('/test/commande',methods = ['POST', 'GET'])
def commandetest():
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

@app.route('/test/connexion',methods = ['POST', 'GET'])
def connexiontest():
   if request.method == 'POST':
      try:
         value = request.get_json()
         print("mode : ", value['mode'])
         print("information : ",value['information'])
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
   else:
       return "GET"

@app.route('/test/joystick',methods = ['POST', 'GET'])
def joysticktest():
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

if __name__ == '__main__':
   app.run(host='0.0.0.0', port='8000')
