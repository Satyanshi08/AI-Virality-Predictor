import cv2
import os
from hook_score import hook_score
from emotion_score import emotion_score
from audio_score import audio_energy_score

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    success, frame = cap.read()

    brightness = None
    contrast = None
    motion_score = None
    scene_changes = 0
    face_count = 0
    thumbnail_path = None

    if success:

        brightness = frame.mean()

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        contrast = gray.std()

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=8,
            minSize=(60, 60)
        )

        face_count = len(faces)

        os.makedirs("static", exist_ok=True)
        thumbnail_path = "static/thumbnail.jpg"
        cv2.imwrite(thumbnail_path, frame)

        # ---------------- Motion ----------------
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, prev_frame = cap.read()

        if ret:
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)
            motion_values = []

            while True:
                ret, curr_frame = cap.read()
                if not ret:
                    break

                curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(prev_gray, curr_gray)
                motion_values.append(diff.mean())
                prev_gray = curr_gray

            if motion_values:
                motion_score = sum(motion_values) / len(motion_values)

        # ---------------- Scene Changes ----------------
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, prev_frame = cap.read()

        if ret:
            prev_gray = cv2.cvtColor(prev_frame, cv2.COLOR_BGR2GRAY)

            while True:
                ret, curr_frame = cap.read()
                if not ret:
                    break

                curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)
                diff = cv2.absdiff(prev_gray, curr_gray)

                if diff.mean() > 40:
                    scene_changes += 1

                prev_gray = curr_gray

    cap.release()

    # 🔥 AI FEATURES
    hook = hook_score(video_path)
    emotion = emotion_score(video_path)
    audio = audio_energy_score(video_path)

    return {
        "duration": round(duration, 2),
        "fps": round(fps, 2),
        "width": width,
        "height": height,
        "thumbnail": thumbnail_path,
        "brightness": round(brightness, 2) if brightness else None,
        "contrast": round(float(contrast), 2) if contrast else None,
        "motion_score": round(float(motion_score), 2) if motion_score else None,
        "scene_changes": scene_changes,
        "face_count": face_count,

        # 🔥 NEW FEATURES
        "hook_score": round(float(hook), 2),
        "emotion_score": round(float(emotion), 2),
        "audio_energy_score": round(float(audio), 2)
    }