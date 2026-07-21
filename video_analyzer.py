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
        frame = cv2.resize(frame, (640, 360))


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
            minSize=(60,60)
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


    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)


    ret, prev_frame = cap.read()

    motion_values = []


    if ret:

        prev_frame = cv2.resize(
            prev_frame,
            (640,360)
        )

        prev_gray = cv2.cvtColor(
            prev_frame,
            cv2.COLOR_BGR2GRAY
        )


        frame_number = 0

        SAMPLE_RATE = 15


        while True:

            ret, curr_frame = cap.read()

            if not ret:
                break


            frame_number += 1


            # Skip frames
            if frame_number % SAMPLE_RATE != 0:
                continue


            curr_frame = cv2.resize(
                curr_frame,
                (640,360)
            )


            curr_gray = cv2.cvtColor(
                curr_frame,
                cv2.COLOR_BGR2GRAY
            )


            diff = cv2.absdiff(
                prev_gray,
                curr_gray
            )


            score = diff.mean()


            motion_values.append(score)


            # Scene change
            if score > 40:
                scene_changes += 1


            prev_gray = curr_gray



    if motion_values:

        motion_score = sum(motion_values) / len(motion_values)



    cap.release()



    # ---------------- AI Features ----------------

    from hook_score import hook_score
    from emotion_score import emotion_score
    from audio_score import audio_energy_score


    hook = hook_score(video_path)

    emotion = emotion_score(video_path)

    audio = audio_energy_score(video_path)



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