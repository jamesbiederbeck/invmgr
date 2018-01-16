import os
from sys import platform
import receivinghelper
from flask import Flask, request, redirect, url_for
from werkzeug.utils import secure_filename
try:
    assert platform != "win32"# Implement new upload paths, and flask usage for windows
except:
    print("Run this on wsl")
ALLOWED_EXTENSIONS = ["TSV","TXT","CSV"]

app = Flask(__name__)
print(app)
@app.route("/")
def whatever():
    return "Hello World!"
@app.route("/test")
def alsowhatever():
    return "goodbye World!"
@app.route("/receive",methods=['POST'])
def getuserscan(data):
    with open("received-scan.txt") as f:
        f.write(data.rstrip)
    
def file_allowed(filename):
    """take a string, and valide the filename
    """
    return "." in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/', methods=['GET', 'POST'])
def uploadfile():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        if file.filename == "":
            flash("No file was selected")
        if file and file_allowed(file.filename):
            filename = secure_filename(file.filename)#look out for code injects
            file.save(os.path.join(app.config['UPLOAD FOLDER'],filename))
            return redirect(url_for('uploaded_file',file=filename))
