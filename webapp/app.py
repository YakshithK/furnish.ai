from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
import roboflow
import cv2

rf = roboflow.Roboflow(api_key='fXKYJZEGo61jhtWmaGPu')
project = rf.workspace().project("furniture-detection-t6j8e")
model = project.version("3").model

model.confidence = 50
model.overlap = 25

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\prabh\Desktop\Courses\Python\Flask\image handling\static\uploads'
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == '':
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('display_image', filename=filename))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')

@app.route('/display/<filename>')
def display_image(filename):
    im_path = "C:\\Users\\prabh\\Desktop\\Courses\\Python\\Flask\\image handling\\static\\uploads\\"
    path = os.path.join(im_path, filename)
    
    image = cv2.imread(path, cv2.IMREAD_COLOR)
    image = cv2.resize(image, (224, 224))
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image = image / 255.0
    
    prediction = model.predict(path)
    dict_pred = prediction.__dict__
    pred_class = []
    dict_pred = dict_pred['predictions']
    pred = dict_pred[0]
    pred_class.append(pred['class'])
    pred1 = dict_pred[1]
    pred_class.append(pred1['class'])
    pred2 = dict_pred[2]
    pred_class.append(pred2['class'])

    return render_template('index.html', filename=filename, pred_class=pred_class)

if __name__ == "__main__":
    app.run()
