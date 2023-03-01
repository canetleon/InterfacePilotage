import serial,time
def init_stm32():
   print("Init stm32")
   arduino = serial.Serial("/dev/ttyACM0", 9600, timeout=1)
   time.sleep(0.1) #wait for serial to open
   if arduino.isOpen():
      print("{} connected!".format(arduino.port))
   return arduino
def msg_to_stm32(arduino, msg):
   print("Sending " + msg + " to stm32")
   try:
      arduino.write(msg.encode())
      while arduino.inWaiting()==0:
         pass
      if arduino.inWaiting()>0:
         answer=arduino.readline()
         arduino.flushInput()
         return "ok", answer
   except Exception as e:
      arduino.flushInput()
      return "error", str(e)
