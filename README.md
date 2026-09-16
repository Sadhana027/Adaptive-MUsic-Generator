# 🎵 Adaptive Music Generator

An AI-powered web application that detects the user's facial emotion through a webcam and dynamically recommends music based on the detected mood. The application also integrates weather information to provide a more personalized music experience.

## ✨ Features

* 🔐 **User Registration & Login**

  * User account creation and authentication.
  * Passwords are securely hashed before storage.
  * Session management using Flask-Login.

* 😊 **Facial Emotion Detection**

  * Captures the user's facial expressions using a webcam.
  * Uses OpenCV and DeepFace for emotion recognition.
  * Detects moods such as:

    * Happy
    * Sad
    * Angry
    * Neutral

* 🎶 **Adaptive Music Recommendation**

  * Automatically selects songs according to the detected mood.
  * Songs are organized into mood-based folders.
  * Users can play the recommended songs through the web application.

* 🌦️ **Weather Integration**

  * Retrieves weather information through a weather API.
  * Weather details are displayed along with the detected mood.

* 🎧 **Web-Based Music Player**

  * Provides an interface for playing mood-based songs.
  * Dynamically loads songs from the project's music directory.

## 🛠️ Technologies Used

| Technology       | Purpose                     |
| ---------------- | --------------------------- |
| Python           | Backend programming         |
| Flask            | Web application framework   |
| OpenCV           | Webcam and image processing |
| DeepFace         | Facial emotion recognition  |
| TensorFlow       | Deep learning backend       |
| Flask-SQLAlchemy | Database integration        |
| SQLite           | User data storage           |
| Flask-Login      | User authentication         |
| Pygame           | Audio functionality         |
| HTML & CSS       | Frontend                    |
| JavaScript       | Client-side functionality   |
| OpenWeather API  | Weather information         |

## 📂 Project Structure

```text
Adaptive-Music-Generator/
│
├── main.py
├── users.db
├── requirements.txt
├── README.md
│
├── templates/
│   ├── login.html
│   └── ...
│
├── static/
│   ├── ...
│   └── music_temp/
│
├── music_dir/
│   ├── Happy/
│   ├── Sad/
│   ├── Neutral/
│   └── Angry/
│
└── .venv/
```

## ⚙️ Installation & Setup

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd Adaptive-Music-Generator
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

### 3. Activate the virtual environment

**Windows PowerShell:**

```powershell
.venv\Scripts\Activate.ps1
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

If `requirements.txt` is not available:

```bash
pip install flask flask-sqlalchemy flask-login werkzeug pygame opencv-python deepface tensorflow tf-keras requests
```

### 5. Configure API keys

The application uses environment variables for sensitive configuration such as API keys and Flask secret keys.

Example:

```text
OPENWEATHER_API_KEY=your_api_key
FLASK_SECRET_KEY=your_secret_key
```

Do not upload actual API keys or secret keys to a public repository.

### 6. Run the application

```bash
python main.py
```

The application will be available at:

```text
http://127.0.0.1:5000
```

## 🎯 How It Works

```text
             User
               │
               ▼
        Login / Register
               │
               ▼
            Webcam
               │
               ▼
       Facial Detection
               │
               ▼
          DeepFace
               │
               ▼
       Emotion Detection
               │
       ┌───────┼────────┐
       ▼       ▼        ▼
     Happy    Sad     Angry
               │
             Neutral
               │
               ▼
       Mood-Based Songs
               │
               ▼
        Music Player
               │
               ▼
       Weather Information
```

## 🎵 Music Organization

Songs should be placed inside their corresponding mood folders:

```text
music_dir/
│
├── Happy/
│   ├── song1.mp3
│   └── song2.mp3
│
├── Sad/
│   ├── song1.mp3
│   └── song2.mp3
│
├── Angry/
│   ├── song1.mp3
│   └── song2.mp3
│
└── Neutral/
    ├── song1.mp3
    └── song2.mp3
```

The application searches these folders and recommends songs according to the detected emotion.

## 🔐 Security

* User passwords are stored using password hashing.
* API keys should be stored using environment variables.
* Secret keys should not be exposed in public repositories.
* Database files containing user information should not be committed to GitHub.

Recommended `.gitignore` entries:

```text
.venv/
__pycache__/
*.pyc
.env
users.db
```

## 🚀 Future Enhancements

* Personalized music recommendations based on listening history
* Favorite and playlist functionality
* Improved emotion-recognition accuracy
* Mood history and analytics
* Integration with online music platforms
* Improved music-player controls
* Responsive mobile interface
* More emotion categories
* Personalized recommendations using machine-learning techniques

## 👩‍💻 Project Information

**Project Title:** Adaptive Music Generator

**Project Type:** B.Tech Mini Project

**Domain:** Artificial Intelligence & Machine Learning / Web Development

**Primary Technologies:** Python, Flask, OpenCV, DeepFace, TensorFlow, SQLite

**Key Concepts:** Facial Emotion Recognition, Mood-Based Recommendation, Web Development, Database Management, API Integration

## 📌 Note

This project was developed for educational purposes to demonstrate the integration of **Python web development, computer vision, facial emotion recognition, database management, and API integration** to create an adaptive music recommendation system.
