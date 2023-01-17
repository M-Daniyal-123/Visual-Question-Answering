from flask import Flask,jsonify
from PIL import Image
import os,io,sys
import base64
import random
from flask_cors import CORS

image_folder  = "./images/"
all_images = os.listdir(image_folder)

app = Flask(__name__)
CORS(app)

###################
@app.route("/fetch_image",methods =['GET'])
def fetch_image():
    
    image = random.choice(all_images)
    img = Image.open(image_folder+image).convert("RGB")
    
    
    rawBytes = io.BytesIO()
    img.save(rawBytes, "JPEG")
    rawBytes.seek(0)
    img_base64 = base64.b64encode(rawBytes.read()).decode("utf8")
	
    # sample = str(img_base64).split('\'')
    # print(sample)
    # print(img_base64)
    return jsonify({'image':img_base64})
    
if __name__ == '__main__':
	app.run(debug = True)
        