import os
import pygame
import requests
from deepface import DeepFace
import cv2
import sys
import time

# Fix encoding issues in Windows terminal
sys.stdout.reconfigure(encoding='utf-8')

# Initialize pygame mixer
pygame.mixer.init()

# Path to your music directory
music_data_dir = r"C:\Users\Keerthi Sowmya\OneDrive\Documents\MAGGIE\MINI PROJECT"  # Correct this path if needed

# Ensure music directory exists
if not os.path.exists(music_data_dir):
    print(f"⚠ Music directory {music_data_dir} does not exist!")
    exit()

# Replace with your OpenWeatherMap API key
OPENWEATHERMAP_API_KEY = "dec3012f11bd8625be68c2718d99848e"
DEFAULT_CITY = "Hyderabad"

# Function to get current weather condition
def get_weather_condition(city=DEFAULT_CITY):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={OPENWEATHERMAP_API_KEY}&units=metric"
    try:
        response = requests.get(url)
        data = response.json()

        if data.get("weather"):
            condition = data["weather"][0]["main"].lower()
            temperature = data["main"]["temp"]
            print(f"🌦 Current Weather: {condition.capitalize()}, {temperature}°C")
            return condition
        else:
            print("⚠ Could not get weather info. Defaulting to 'clear'.")
            return "clear"
    except Exception as e:
        print(f"Error fetching weather: {e}")
        return "clear"

# Function to list songs from a specific mood/weather folder
def list_mood_songs(mood):
    mood_dir = os.path.join(music_data_dir, mood)
    if os.path.exists(mood_dir):
        songs = [os.path.join(mood_dir, f) for f in os.listdir(mood_dir) if f.endswith((".mp3", ".wav"))]
        if songs:
            print(f"\n🎵 Songs available for {mood}:")
            for index, song in enumerate(songs):
                print(f"{index + 1}. {os.path.basename(song)}")
            return songs
        else:
            print(f"⚠ No songs found for {mood}.")
    else:
        print(f"⚠ No music folder found for {mood}.")
    return []

# Function to list all songs in the entire music folder
def list_all_songs():
    all_songs = []
    for root, _, files in os.walk(music_data_dir):
        for file in files:
            if file.endswith((".mp3", ".wav")):
                all_songs.append(os.path.join(root, file))
    return all_songs

# Function to play a song
def play_song(song_path):
    try:
        pygame.mixer.music.load(song_path)
        pygame.mixer.music.play()
        print(f"\n🎵 Now playing: {os.path.basename(song_path)}")
    except Exception as e:
        print(f"⚠ Error playing song: {e}")

# Function to detect mood from webcam (quick snapshot)
def get_mood_from_webcam():
    cap = cv2.VideoCapture(0)
    detected_mood = "neutral"
    
    start_time = time.time()
    detected_once = False

    while time.time() - start_time < 5:  # Capture for 5 seconds max
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            detected_mood = result[0]['dominant_emotion']
            detected_once = True
        except Exception as e:
            detected_mood = "neutral"

        cv2.putText(frame, f"Emotion: {detected_mood}", (30, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.imshow('Detecting Mood...', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        

    cap.release()
    cv2.destroyAllWindows()
    cv2.waitKey(1)  # Critical to fully close OpenCV windows
    return detected_mood

# Main function
def main():
    while True:
        detected_mood = get_mood_from_webcam()
        print(f"\n🧠 Detected Mood: {detected_mood}")

        weather_condition = get_weather_condition()
        print(f"🎯 Using Mood + Weather: {detected_mood} + {weather_condition}")

        # Try mood+weather folder, then mood, then weather
        combined_folder = f"{detected_mood}_{weather_condition}"
        mood_songs = list_mood_songs(combined_folder)

        if not mood_songs:
            mood_songs = list_mood_songs(detected_mood)

        if not mood_songs:
            mood_songs = list_mood_songs(weather_condition)

        all_songs = list_all_songs()

        if not mood_songs:
            print("\n⚠ No songs found for mood/weather. Showing full library.")
            mood_songs = all_songs
        if mood_songs:
            print("\n🎵 Available Songs:")
            for idx, song in enumerate(mood_songs):
                print(f"{idx + 1}. {os.path.basename(song)}")

        if not all_songs:
            print("❌ No songs available in the library. Exiting...")
            break

        current_index = 0

        while True:
            user_input = input("\n▶ Enter song index, song name, 'n' for next song, or 'q' to quit: ").strip().lower()

            if user_input == 'q':
                print("👋 Exiting program...")
                pygame.mixer.music.stop()
                return

            elif user_input == 'n':
                current_index = (current_index + 1) % len(mood_songs)
                play_song(mood_songs[current_index])

            elif user_input.isdigit() and 1 <= int(user_input) <= len(mood_songs):
                current_index = int(user_input) - 1
                play_song(mood_songs[current_index])

            else:
                matching_songs = [s for s in all_songs if os.path.basename(s).lower() == user_input]
                if matching_songs:
                    play_song(matching_songs[0])
                else:
                    print("⚠ Invalid input. Try again.")

if __name__ == "__main__":
    main()
