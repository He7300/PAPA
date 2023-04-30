from flask import Flask, render_template, request, redirect, url_for, flash
from werkzeug.utils import secure_filename
import os
from PIL import Image
from pymongo import MongoClient

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg', 'gif'}

client = MongoClient('mongodb://localhost:27017/')
db = client['image-gallery']

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

@app.route('/')
def index():
    images = db.images.find()
    return render_template('index.html', images=images)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            image = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            db.images.insert_one({'filename': filename, 'width': image.width, 'height': image.height})
            flash('File uploaded successfully')
            return redirect(url_for('index'))
    return render_template('upload.html')

if __name__ == '__main__':
    app.run(debug=True)
