from flask import Flask, render_template, request
from flask_socketio import SocketIO, emit
# import subprocess
import io
from io import StringIO

import cv2
import numpy as np
import base64
from PIL import Image
# from from_root import from_root
from PIL import UnidentifiedImageError

app = Flask(__name__)
socketio = SocketIO(app, debug=True, cors_allowed_origins='*', async_mode='eventlet')


@app.route('/')
def hello_world():
    index_file = 'index.html'
    return render_template(index_file)

# @app.route('/home')
# def main():
#     template = 'base.html'
#     return render_template(template)


# @socketio.on("my_event")
# def check_ping():
#     for x in range(5):
#         cmd = 'ping -c 1 8.8.8.8|head -2|tail -1'
#         listing1 = subprocess.run(cmd, stdout=subprocess.PIPE, text=True, shell=True)
#         sid = request.sid
#         emit('server', {"data1": x, "data": listing1.stdout}, room=sid)
#         socketio.sleep(1)

@socketio.on('image')
def image(data_image):
    sbuf = StringIO()
    sbuf.write(data_image)

    # decode and convert into image
    b = io.BytesIO(base64.b64decode(data_image))
    try:
        pimg = Image.open(b)

        # converting RGB to BGR, as opencv standards
        frame = cv2.cvtColor(np.array(pimg), cv2.COLOR_RGB2BGR)

        # Process the image frame
        # processed = process_frame(frame)

        # Encode to jpg
        img_encode = cv2.imencode('.jpg', frame)[1]

        # base64 encode
        string_data = base64.b64encode(img_encode).decode('utf-8')
        b64_src = 'data:image/jpg;base64,'
        string_data = b64_src + string_data

        # emit the frame back
        emit('response_back', string_data)
    except UnidentifiedImageError:
        print("No Data received")