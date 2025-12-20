import cv2
from deepface import DeepFace

def detect_mood(timeout=10, confidence_threshold=70):
    # Load Haar Cascade for face detection
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise Exception("Could not open webcam")

    detected_mood = None
    start_time = cv2.getTickCount()  # Start timer
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Resize frame for better performance
        frame = cv2.resize(frame, (640, 480))

        # Convert frame to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

        # Analyze emotion every 5 frames
        if frame_count % 5 == 0:
            if cv2.getTickCount() - start_time > timeout * cv2.getTickFrequency():
                print("Timeout reached. Exiting mood detection.")
                break

            try:
                # Analyze emotion using DeepFace
                result = DeepFace.analyze(frame, actions=['emotion'], detector_backend='mtcnn', enforce_detection=False)
                if result and result[0]['emotion']:
                    detected_mood = result[0]['dominant_emotion']
                    confidence = result[0]['emotion'][detected_mood]
                    print(f"Detected Emotion: {detected_mood} (Confidence: {confidence:.2f})")

                    # Only accept the mood if confidence is above the threshold
                    if confidence > confidence_threshold:
                        break
            except Exception as e:
                print(f"Error detecting emotion: {e}")

        frame_count += 1

        # Display frame with detected faces
        for (x, y, w, h) in faces:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # Display mood and confidence on the frame
        cv2.putText(frame, f"Mood: {detected_mood}", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

        cv2.imshow('Mood Detection', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    print(f"Detected Mood: {detected_mood}")
    return detected_mood or "neutral"  # Return detected mood or default to "neutral"
