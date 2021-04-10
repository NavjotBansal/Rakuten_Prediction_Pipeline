import pipeline
from flask import Flask,flash, render_template, url_for, request,redirect,send_file
import os 
import zipfile
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = 'Uploads'
ALLOWED_EXTENSIONS = {'mp4'}
TABLEAU_URL = 'https://public.tableau.com/profile/anubhav.pandey7854#!/vizhome/TestEmotionTrack/EmotionTrackPg1'
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
            # return redirect(TABLEAU_URL)
            send_file('output.mp4', attachment_filename='output.mp4', as_attachment=True)
            return render_template('downloads.html')
        return render_template('index.html')  
        
@app.route("/processing",methods=['POST','GET'])
def processing():
    if request.method == "POST":
        return 'Successfully pushed to server'
    else:
        return render_template('processing.html') 

@app.route('/file-downloads/')
def file_downloads():
	try:
		return render_template('downloads.html')
	except Exception as e:
		return str(e)

@app.route('/return-video/')
def return_video():
	try:
		return send_file('output.mp4', attachment_filename='output.mp4', as_attachment=True)
	except Exception as e:
		return str(e)       

@app.route('/return-csv/')
def return_csv():
	try:
		return send_file('Emotion_Data.csv', attachment_filename='Emotion_Data.csv', as_attachment=True)
	except Exception as e:
		return str(e)  

@app.route('/tableau/')
def tableau_redirect():
	try:
		return redirect(TABLEAU_URL)
	except Exception as e:
		return str(e)               

if __name__ == "__main__":
    app.run(host="0.0.0.0")

