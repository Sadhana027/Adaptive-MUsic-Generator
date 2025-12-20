from flask import Flask, render_template, request, redirect, url_for, session, send_from_directory
import os
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Change this in production

# Paths
MUSIC_FOLDER = r"C:\Users\Keerthi Sowmya\OneDrive\Documents\MAGGIE\MINI PROJECT\music_dir"
USER_DB = 'users.json'

# Ensure user DB exists
if not os.path.exists(USER_DB):
    with open(USER_DB, 'w') as f:
        json.dump({}, f)

# Load users
with open(USER_DB, 'r') as f:
    users = json.load(f)

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if 'signup' in request.form:
            if username in users:
                return render_template('login.html', error="User already exists.")
            users[username] = generate_password_hash(password)
            with open(USER_DB, 'w') as f:
                json.dump(users, f)
            session['username'] = username
            return redirect(url_for('home'))

        elif 'login' in request.form:
            if username not in users or not check_password_hash(users[username], password):
                return render_template('login.html', error="Invalid username or password.")
            session['username'] = username
            return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/home')
def home():
    if 'username' not in session:
        return redirect(url_for('login'))
    songs = []
    for mood in os.listdir(MUSIC_FOLDER):
        folder_path = os.path.join(MUSIC_FOLDER, mood)
        if os.path.isdir(folder_path):
            for song in os.listdir(folder_path):
                if song.endswith(('.mp3', '.wav')):
                    songs.append({'name': song, 'path': f"{mood}/{song}"})
    return render_template('player.html', songs=songs, username=session['username'])

@app.route('/music/<path:filename>')
def serve_music(filename):
    return send_from_directory(MUSIC_FOLDER, filename)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
