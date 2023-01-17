from model import VQAModel
from flask import Flask,request
from flask_cors import CORS
from transformers import AutoTokenizer, AutoFeatureExtractor, AutoModel
import io, base64
from PIL import Image
import torch


######## Config ############
label2idx = {'black': 6,
 'blue': 11,
 'brown': 10,
 'circle': 0,
 'gray': 3,
 'green': 1,
 'no': 12,
 'rectangle': 7,
 'red': 2,
 'teal': 5,
 'triangle': 9,
 'yellow': 8,
 'yes': 4}

idx2label = {v:k for k,v in label2idx.items()}

num_labels = 13

device = "cuda" if torch.cuda.is_available() else "cpu"

###############################

####### Model Details ######################################

## Language Model
tokenizer = AutoTokenizer.from_pretrained("bert-base-uncased")
language_model = AutoModel.from_pretrained("bert-base-uncased")

## Vision Model
feature_extractor = AutoFeatureExtractor.from_pretrained("google/vit-base-patch16-224-in21k")
vision_model = AutoModel.from_pretrained("google/vit-base-patch16-224-in21k")

print("Language and Vision Transformer Loaded")

language_model.to(device)
vision_model.to(device)


### VQA Model 
model = VQAModel(num_labels=num_labels)
model.load_state_dict(torch.load("./best.pt"))
model.to(device)
#############################################################

app = Flask(__name__)
CORS(app)

@app.route("/get_answer",methods = ['POST'])
def get_answer():
    
    image = request.json['image']
    question = request.json['question']
    
    image = Image.open(io.BytesIO(base64.decodebytes(bytes(image, "utf-8")))).convert("RGB")
    
    text_input = tokenizer(question,return_tensors="pt")
    image_input = feature_extractor(image,return_tensors = "pt")
        
    text_input ={k:v.to(device) for k,v in text_input.items()}
    image_input ={k:v.to(device) for k,v in image_input.items()}
    
    text_tensors = language_model(**text_input)
    image_tensors = vision_model(**image_input)
    
    text_tensors = text_tensors.pooler_output
    image_tensors = image_tensors.pooler_output
    
    model.eval()
    with torch.no_grad():
        output = model(image_tensors,text_tensors)
    
    value = output.argmax(-1).detach().cpu()[0].item()
    
    return {"answer":idx2label[value]}
    
    
    
if __name__ == "__main__":
    app.run(debug=True,port=5001)