
# -------- User Model ---import os
import time
import os
import pygame
import threading
import cv2
from deepface import DeepFace
from flask import Flask, render_template_string, render_template, jsonify, request, redirect, url_for, flash
import webbrowser
import requests
import shutil
import uuid

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user, UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

# -------- Constants & Config --------
MUSIC_FOLDER = r"C:\Users\Keerthi Sowmya\OneDrive\Documents\MAGGIE\MINI PROJECT\music_dir"
pygame.mixer.init()

app = Flask(__name__)
app.secret_key = 'your_secret_key_here_change_this'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'  # SQLite DB file
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.login_view = 'login'
login_manager.init_app(app)
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(150))
    email = db.Column(db.String(150), unique=True)
    password = db.Column(db.String(150))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# -------- Weather, Mood & Music Functions (unchanged) --------
current_song_name = ""
current_duration = 0
weather_data = {}
user_mood = ""
user_city = "Unknown"
songs = []
song_index = 0

def get_weather_and_air_quality():
    global user_city
    api_key = "4106c2238201b371f6b9501fdfe73099"
    city = "Hyderabad"
    weather_url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    try:
        weather_resp = requests.get(weather_url)
        weather_json = weather_resp.json()

        condition = weather_json['weather'][0]['main']
        temperature = weather_json['main']['temp']
        humidity = weather_json['main']['humidity']
        user_city = weather_json['name']

        lat = weather_json['coord']['lat']
        lon = weather_json['coord']['lon']

        air_quality_url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        air_quality_resp = requests.get(air_quality_url)
        air_quality_json = air_quality_resp.json()
        aqi = air_quality_json['list'][0]['main']['aqi']

        aqi_dict = {1: "Good", 2: "Fair", 3: "Moderate", 4: "Poor", 5: "Very Poor"}
        air_quality = aqi_dict.get(aqi, "Unknown")

        return {
            "condition": condition,
            "temperature": temperature,
            "humidity": humidity,
            "air_quality": air_quality
        }
    except Exception as e:
        print("Error fetching weather or air quality:", e)
        return {
            "condition": "Clear",
            "temperature": 25,
            "humidity": 50,
            "air_quality": "Good"
        }

def detect_mood_from_webcam(timeout=10):
    cap = cv2.VideoCapture(0)
    mood = "neutral"
    start_time = time.time()

    while time.time() - start_time < timeout:
        ret, frame = cap.read()
        if not ret:
            continue

        frame = cv2.flip(frame, 1)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        try:
            analysis = DeepFace.analyze(rgb_frame, actions=['emotion'], enforce_detection=False)
            if isinstance(analysis, list):
                emotion = analysis[0]['dominant_emotion']
            else:
                emotion = analysis['dominant_emotion']

            if emotion in ["happy", "sad", "neutral", "angry"]:
                mood = emotion
            else:
                mood = "neutral"
        except Exception as e:
            print(f"Error during mood detection: {e}")

        cv2.putText(frame, f"Mood: {mood}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)
        cv2.imshow("Mood Detection (Press q to quit)", frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    return mood

MOOD_GIFS = {
    "happy": "https://em-content.zobj.net/source/microsoft-teams/337/grinning-face_1f600.png",
    "sad": "https://em-content.zobj.net/source/microsoft-teams/337/crying-face_1f622.png",
    "neutral": "https://em-content.zobj.net/source/microsoft-teams/337/neutral-face_1f610.png",
    "angry": "https://em-content.zobj.net/source/microsoft-teams/337/angry-face_1f620.png"
}

WEATHER_GIFS = {
    "Rain": "https://em-content.zobj.net/source/microsoft-teams/337/cloud-with-rain_1f327-fe0f.png",
    "Clear": "https://em-content.zobj.net/source/microsoft-teams/337/sun_2600-fe0f.png",
    "Clouds": "https://em-content.zobj.net/source/microsoft-teams/337/cloud_2601-fe0f.png",
    "Wind": "https://em-content.zobj.net/source/microsoft-teams/337/wind-face-emoji_1f32c.png",
    "Snow": "https://em-content.zobj.net/source/microsoft-teams/337/snowflake_2744-fe0f.png",
}

def load_songs_for_mood(mood):
    folder_map = {
        "happy": "Happy",
        "sad": "Sad",
        "neutral": "Neutral",
        "angry": "Angry"
    }
    folder_name = folder_map.get(mood, "Neutral")
    mood_folder = os.path.join(MUSIC_FOLDER, folder_name)
    if not os.path.exists(mood_folder):
        print(f"Mood folder not found: {mood_folder}")
        return []
    song_list = [os.path.join(mood_folder, f) for f in os.listdir(mood_folder) if f.lower().endswith('.mp3')]
    return song_list

def background_detection():
    global user_mood, weather_data
    print("Fetching weather and air quality...")
    weather_data = get_weather_and_air_quality()
    print(f"Weather data: {weather_data}")

    print("Detecting mood from webcam...")
    user_mood = detect_mood_from_webcam(timeout=10)
    print(f"Detected mood: {user_mood}")

# -------- Flask Routes --------
TEMP_MUSIC_DIR = os.path.join(os.getcwd(), "static", "music_temp")
os.makedirs(TEMP_MUSIC_DIR, exist_ok=True)

PLAYER_TEMPLATE = """ 
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8" />
    <title>Mood Based Music Player - {{ mood.title() }}</title>
    <style>
        /* Your CSS styling from before */
        body {
            font-family: Arial, sans-serif;
            background-image: url("https://tse1.mm.bing.net/th/id/OIP.o2fcnb508lXf0OO-afgT0QHaEK?r=0&rs=1&pid=ImgDetMain");
            background-size: cover;
            background-position: center;
            background-repeat: no-repeat;
            color: white;
            text-align: center;
            padding: 30px;
        }
        h1 {
            margin-bottom: 20px;
        }
        
        .songs {
            display: flex;
            flex-wrap: wrap;
            justify-content: center;
            gap: 20px;
        }
        .song-card {
            background: #1e1e1e;
            padding: 15px;
            border-radius: 10px;
            width: 200px;
            box-shadow: 0 0 10px #00ff99;
            cursor: pointer;
            transition: transform 0.2s ease;
        }
        .song-card:hover {
            transform: scale(1.05);
            background: #00ff99;
            color: black;
        }
        .song-title {
            margin: 10px 0;
            font-weight: bold;
            font-size: 1.1em;
        }
        .info-box {
            margin-top: 30px;
            font-size: 1em;
        }
        .gif-container {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-top: 30px;
            padding: 0 10%; /* Adds space from edges */
        }
        .gif-box {
            margin-top: 10px;
        }
        .logout-btn {
            margin-top: 20px;
            padding: 8px 15px;
            background: #ff4444;
            color: white;
            border: none;
            border-radius: 6px;
            cursor: pointer;
            font-size: 1em;
        }
        .logout-btn:hover {
            background: #cc0000;
        }
    </style>
</head>
<body>
    <h1>Mood Detected: {{ mood.title() }}</h1>

    <button class="logout-btn" onclick="window.location.href='{{ url_for('logout') }}'">Logout</button>

    <div class="songs">
        {% for idx, song in enumerate(songs) %}
        <div class="song-card" onclick="playSong({{ idx }})">
            <div class="song-title">{{ idx + 1 }}. {{ song }}</div>
        </div>
        {% endfor %}
    </div>

    <div class="info-box">
        <p><strong>City:</strong> {{ city }}</p>
        <p><strong>Condition:</strong> {{ condition }}</p>
        <p><strong>Temperature:</strong> {{ temperature }} °C</p>
        <p><strong>Humidity:</strong> {{ humidity }}%</p>
        <p><strong>Air Quality:</strong> {{ air_quality }}</p>
    </div>

    <div class="gif-container">
        <div class="gif-box">
            <h3>🧠 Mood</h3>
            <img src="{{ mood_gif }}" alt="Mood" width="100" />
        </div>

        <div class="gif-box">
            <h3>🌤 Weather</h3>
            <img src="{{ weather_gif }}" alt="Weather" width="100" />
        </div>
    </div>

    <audio id="audioPlayer" controls style="margin-top: 30px; width: 80%;"></audio>

    <script>
        const songs = {{ songs_json | safe }};
        const audioPlayer = document.getElementById('audioPlayer');

        function playSong(index) {
            const songPath = "/play_song_path?path=" + encodeURIComponent(songs[index]);
            fetch(songPath)
                .then(response => response.json())
                .then(data => {
                    audioPlayer.src = "/static/music_temp/" + data.filename;
                    audioPlayer.play();
                });
        }
    </script>
</body>
</html>
"""

@app.route('/')
@login_required
def home():
    background_detection()
    global songs
    songs = load_songs_for_mood(user_mood)
    song_names = [os.path.basename(s) for s in songs]
    mood_gif = MOOD_GIFS.get(user_mood, MOOD_GIFS["neutral"])
    weather_gif = WEATHER_GIFS.get(weather_data.get("condition", "Clear"), WEATHER_GIFS["Clear"])
    return render_template_string(PLAYER_TEMPLATE,
                                  mood=user_mood,
                                  songs=song_names,
                                  songs_json=songs,
                                  city=user_city,
                                  condition=weather_data.get("condition", "Clear"),
                                  temperature=weather_data.get("temperature", 25),
                                  humidity=weather_data.get("humidity", 50),
                                  air_quality=weather_data.get("air_quality", "Good"),
                                  mood_gif=mood_gif,
                                  weather_gif=weather_gif,
                                  enumerate=enumerate)

@app.route('/play_song_path')
@login_required
def play_song_path():
    song_path = request.args.get('path')
    if not song_path or not os.path.exists(song_path):
        return jsonify({"error": "Invalid song path"}), 400

    filename = str(uuid.uuid4()) + ".mp3"
    dest_path = os.path.join(TEMP_MUSIC_DIR, filename)
    shutil.copy2(song_path, dest_path)

    return jsonify({"filename": filename})

# -------- Login & Register --------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        full_name = request.form.get('full_name')
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email address already exists')
            return redirect(url_for('register'))

        new_user = User(full_name=full_name, email=email, password=generate_password_hash(password))
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for('home'))

    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash('Invalid login credentials')
            return redirect(url_for('login'))

        login_user(user)
        return redirect(url_for('home'))

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == "__main__":
    # Create DB tables if not exist
    with app.app_context():
        db.create_all()

    webbrowser.open("http://127.0.0.1:5000/login")
    app.run(debug=True, port=5000)
