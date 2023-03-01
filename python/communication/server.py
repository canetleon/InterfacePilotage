from flask import Flask, request, jsonify
from flask_cors import CORS
from com_stm32v2 import setupSerial, recvLikeArduino, sendToArduino

#init stm_32
stm = False
mode = "joystick"
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
   global mode
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
         print("mode : ", value['mode'])
         mode = value['mode']
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
   global mode
   if request.method == 'POST':
      try:
         value = request.get_json()
         print(value)
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
      print(mode)
      return mode
@app.route('/com',methods = ['POST', 'GET'])
def com():
   if request.method == 'POST':
      print("ok")
   else:
       return jsonify({"method":"GET"})


if __name__ == '__main__':
   app.run(host='0.0.0.0', port='8000')
