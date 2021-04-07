import pipeline
from flask import Flask,flash, render_template, url_for, request,redirect
import os 
import zipfile
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Uploads'
ALLOWED_EXTENSIONS = {'mp4'}
TABLEAU_URL = 'https://public.tableau.com/profile/anubhav.pandey7854#!/vizhome/FirstEmotionTrack/EmotionTrackPg1'
app = Flask(__name__)
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/",methods=['POST','GET'])
def index():
    if request.method == "POST":
        return 'Successfully pushed to server'
    else:
        return render_template("index.html")

@app.route('/uploader', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        # check if the post request has the file part
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            filepath=os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            print("File uploaded to path->{}".format(filepath))
            pipeline.model_script(filepath)
            return redirect(TABLEAU_URL)
        return render_template('index.html')                       

if __name__ == "__main__":
    app.run(host="0.0.0.0")

