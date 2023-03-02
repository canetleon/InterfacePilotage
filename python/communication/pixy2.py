import os
from flask import Flask, render_template
from PIL import Image, ImageDraw as D
import time

full_filename = '/home/canetleon/Documents/pixy2/build/get_raw_frame/out.ppm'
cmd_frame = 'cd /home/canetleon/Documents/pixy2/build/get_raw_frame && sudo ./get_raw_frame'
cmd_blocks = 'cd /home/canetleon/Documents/pixy2/build/get_blocks_cpp_demo && sudo ./get_blocks_cpp_demo'

app = Flask(__name__)
FOLDER = os.path.join('static', 'pixyStream')
app.config['FOLDER'] = FOLDER

@app.route('/')
@app.route('/pixy')
def show_index():
    starttime = time.time()
    try:
       os.system(cmd_frame)
       #os.system
       print(time.time() - starttime)
       im = Image.open(full_filename)
       draw=D.Draw(im)
       draw.rectangle([(10,10),(100,100)],outline="white")
       im.save('static/pixyStream/frame.jpg')
    except Exception as e:
       print('error',str(e))
    print(time.time() - starttime)
    return render_template("index.html", user_image = os.path.join(app.config['FOLDER'],'frame.jpg'))

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8101)
