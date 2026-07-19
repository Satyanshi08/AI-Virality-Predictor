from deepface import DeepFace
import cv2

def emotion_score(video_path):
    cap = cv2.VideoCapture(video_path)

    scores = []
    count = 0

    while count < 8:
        ret, frame = cap.read()
        if not ret:
            break

        try:
            result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)
            emotion = result[0]['dominant_emotion']

            if emotion == "happy":
                scores.append(100)
            elif emotion == "surprise":
                scores.append(80)
            elif emotion == "neutral":
                scores.append(50)
            else:
                scores.append(20)

        except:
            scores.append(0)

        count += 1

    cap.release()

    return sum(scores) / max(1, len(scores))