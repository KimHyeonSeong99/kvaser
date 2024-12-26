from flask import Flask, request, redirect
from flask import render_template, url_for, flash
from publisher_file import send_file_to_broker
import os

broker_ip = '192.168.65.1'
app = Flask(__name__)
app.secret_key= 'secret_key'

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), ' upload')
os.makedirs(UPLOAD_FOLDER, exist_ok= True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def upload_form():
    return render_template('upload.html')
@app.route('/upload', methods = ['POST'])
def upload_file():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(url_for('upload_form'))
    
    file = request.files['file']
    username = request.form['username']
    password = request.form['password']

    print(f"File:{file.filename}\nUsername:{username}\nPassword:{password}")

    if file.filename == '':
        flash('No file namee')
        return redirect(url_for('upload_form'))
    if file:
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(file_path)
        send_file_to_broker(file_path, broker_ip, username, password)
        flash(f"File '{file.filename}' uploaded successfully!")
        return redirect(url_for('upload_form'))
    
if __name__ == "__main__":
    app.run(host='0.0.0.0', port = 5000, debug = True)