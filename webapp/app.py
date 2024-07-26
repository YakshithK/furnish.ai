from flask import Flask, flash, request, redirect, url_for, render_template
import os
from werkzeug.utils import secure_filename
import roboflow
import cv2
from matplotlib import pyplot as plt
import random
import sqlite3

def fetch_recommendations(detected_items, name):
    conn = sqlite3.connect('database/furniture.db')
    c = conn.cursor()
    recommendations = []
    
    for item in detected_items:
        c.execute('SELECT * FROM furniture WHERE style=? AND name=?', (item, name))
        recommendations.extend(c.fetchall())  # Using extend to handle multiple recommendations
    
    conn.close()
    return recommendations

style = []

database = {'Modern' :['Bed', 'Lamp', 'Nightstand', 'Dresser', 'Desk', 'Mirror', 'Rug', 'Chairs'],
            'Cozy' :['Bed', 'Lamp', 'Nightstand', 'Dresser', 'Desk', 'Mirror', 'Rug'],
            'Basic' :['Bed', 'Lamp', 'Nightstand', 'Dresser', 'Desk', 'Mirror', 'Rug'],
            'Antique' :['Bed', 'Lamp', 'Nightstand', 'Dresser', 'Desk', 'Mirror', 'Rug']}

rf = roboflow.Roboflow(api_key='fXKYJZEGo61jhtWmaGPu')
project = rf.workspace().project("furniture-detection-t6j8e")
model = project.version("3").model

model.confidence = 50
model.overlap = 25

app = Flask(__name__)

UPLOAD_FOLDER = r'C:\Users\prabh\Desktop\furnish.ai\webapp\static\uploads'
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
        selected_style = request.form.get('selected_style')
        style.append(selected_style)
        flash('Image successfully uploaded and displayed below')
        return redirect(url_for('display_image', filename=filename))
    else:
        flash('Allowed image types are - png, jpg, jpeg, gif')
        return redirect(request.url)

@app.route('/display/<filename>')
def display_image(filename):
    im_path = "C:\\Users\\prabh\\Desktop\\furnish.ai\\webapp\\static\\uploads\\"
    master_path = os.path.join(im_path, filename)

    image = cv2.imread(master_path)
    image = cv2.resize(image, (0, 0), fx=0.5, fy=0.5)

    selected_style = style[0]
    print(selected_style)

    master_items = database[selected_style]

    prediction = model.predict(master_path)
    dict_pred = prediction.__dict__
    pred_items = []
    dict_pred = dict_pred['predictions']
    pred = dict_pred[0]
    pred_items.append(pred['class'])
    pred1 = dict_pred[1]
    pred_items.append(pred1['class'])
    pred2 = dict_pred[2]
    pred_items.append(pred2['class'])

    new_items = [item for item in master_items if item not in pred_items]

    recommendations = []
    for item in new_items:
        recommendations.extend(fetch_recommendations([selected_style], item))

    # Select a few random recommendations
    random_recommendations = random.sample(recommendations, min(len(recommendations), 5))
    

    #cv2.imwrite(master_path, image)
    return render_template('index.html', filename=filename, pred_items=pred_items, recommendations=random_recommendations)

if __name__ == "__main__":
    app.run()
