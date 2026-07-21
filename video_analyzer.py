import cv2
import os

print("CV2 module:", cv2)
print("CV2 file:", getattr(cv2, "__file__", "No file"))
print("CV2 version:", getattr(cv2, "__version__", "Unknown"))
print("Has CascadeClassifier:", hasattr(cv2, "CascadeClassifier"))


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


    brightness = None
    contrast = None
    motion_score = 0
    scene_changes = 0
    face_count = 0
    thumbnail_path = None


    # ---------------- First Frame Analysis ----------------

    success, frame = cap.read()

    if success:

        # Resize for faster processing
        frame = cv2.resize(frame, (320,180))


        brightness = frame.mean()

        gray = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2GRAY
        )

        contrast = gray.std()


        # Face detection
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=8,
            minSize=(40,40)
        )

        face_count = len(faces)


        # Thumbnail
        os.makedirs("static", exist_ok=True)

        thumbnail_path = "static/thumbnail.jpg"

        cv2.imwrite(
            thumbnail_path,
            frame
        )


    # ---------------- Motion + Scene Analysis ----------------

    total_frames = int(frame_count)
    motion_values = []

    if total_frames > 1:

      SAMPLE_COUNT = 40  # Analyze at most 40 frames

      step = max(1, total_frames // SAMPLE_COUNT)

      prev_gray = None
      motion_values = []

      for i in range(0, total_frames, step):

        cap.set(cv2.CAP_PROP_POS_FRAMES, i)

        ret, curr_frame = cap.read()

        if not ret:
            continue

        curr_frame = cv2.resize(curr_frame, (320, 180))

        curr_gray = cv2.cvtColor(curr_frame, cv2.COLOR_BGR2GRAY)

        if prev_gray is not None:

            diff = cv2.absdiff(prev_gray, curr_gray)

            score = float(diff.mean())

            motion_values.append(score)

            if score > 40:
                scene_changes += 1

        prev_gray = curr_gray

    if motion_values:
        motion_score = sum(motion_values) / len(motion_values)



    cap.release()



    # ---------------- AI Features ----------------

    #from hook_score import hook_score
    #from emotion_score import emotion_score
    #from audio_score import audio_energy_score


    #hook = hook_score(video_path)

    #emotion = 50

    #audio = audio_energy_score(video_path)
    print("STARTING HOOK")
    from hook_score import hook_score
    hook = hook_score(video_path)
    print("HOOK DONE")


    print("SKIPPING EMOTION FOR TEST")
    emotion = 50


    print("STARTING AUDIO")
    from audio_score import audio_energy_score
    audio = audio_energy_score(video_path)
    print("AUDIO DONE")


    return {

        "duration": round(duration,2),

        "fps": round(fps,2),

        "width": width,

        "height": height,

        "thumbnail": thumbnail_path,


        "brightness":
            round(float(brightness),2)
            if brightness is not None else None,


        "contrast":
            round(float(contrast),2)
            if contrast is not None else None,


        "motion_score":
            round(float(motion_score),2),


        "scene_changes":
            scene_changes,


        "face_count":
            face_count,


        "hook_score":
            round(float(hook),2),


        "emotion_score":
            round(float(emotion),2),


        "audio_energy_score":
            round(float(audio),2)

    }