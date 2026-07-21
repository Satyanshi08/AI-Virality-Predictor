import cv2
import os

face_cascade = cv2.CascadeClassifier(
    cv2.data.haarcascades +
    "haarcascade_frontalface_default.xml"
)


def analyze_video(video_path):

    cap = cv2.VideoCapture(video_path)

    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    duration = frame_count / fps if fps > 0 else 0

    brightness = None
    contrast = None
    motion_score = 0
    scene_changes = 0
    face_count = 0
    thumbnail_path = None

    # ---------------- First Frame Analysis ----------------

    success, frame = cap.read()

    if success:

        frame = cv2.resize(frame, (256, 144))

        brightness = float(frame.mean())

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        contrast = float(gray.std())

        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(40, 40)
        )

        face_count = len(faces)

        os.makedirs("static", exist_ok=True)

        thumbnail_path = "static/thumbnail.jpg"

        cv2.imwrite(
            thumbnail_path,
            frame
        )

    # ---------------- Motion + Scene Analysis ----------------

    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

    SAMPLE_COUNT = 20
    step = max(1, frame_count // SAMPLE_COUNT)

    motion_values = []
    prev_gray = None
    frame_index = 0

    while True:

        ret, curr_frame = cap.read()

        if not ret:
            break

        if frame_index % step != 0:
            frame_index += 1
            continue

        curr_frame = cv2.resize(curr_frame, (256, 144))

        curr_gray = cv2.cvtColor(
            curr_frame,
            cv2.COLOR_BGR2GRAY
        )

        if prev_gray is not None:

            diff = cv2.absdiff(
                prev_gray,
                curr_gray
            )

            score = float(diff.mean())

            motion_values.append(score)

            if score > 40:
                scene_changes += 1

        prev_gray = curr_gray

        frame_index += 1

        if len(motion_values) >= SAMPLE_COUNT:
            break

    if motion_values:
        motion_score = sum(motion_values) / len(motion_values)

    cap.release()

    # ---------------- AI Features ----------------
    # Enable these later after OpenCV pipeline is stable

    hook = 50
    emotion = 50
    audio = 50

    return {

        "duration": round(duration, 2),

        "fps": round(fps, 2),

        "width": width,

        "height": height,

        "thumbnail": thumbnail_path,

        "brightness":
            round(brightness, 2)
            if brightness is not None else None,

        "contrast":
            round(contrast, 2)
            if contrast is not None else None,

        "motion_score":
            round(motion_score, 2),

        "scene_changes":
            scene_changes,

        "face_count":
            face_count,

        "hook_score":
            round(float(hook), 2),

        "emotion_score":
            round(float(emotion), 2),

        "audio_energy_score":
            round(float(audio), 2)
    }