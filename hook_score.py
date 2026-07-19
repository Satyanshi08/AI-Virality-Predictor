import cv2
import numpy as np


def hook_score(video_path):
    """
    Calculates Hook Score based on early video motion intensity.
    Focuses on first ~5 seconds of the video.
    Output: 0–100 score
    """

    cap = cv2.VideoCapture(video_path)

    # Get FPS (frames per second)
    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps == 0 or fps is None:
        fps = 30  # fallback value

    max_frames = int(fps * 5)  # analyze first 5 seconds

    prev_frame = None
    motion_sum = 0
    frame_count = 0

    while frame_count < max_frames:
        ret, frame = cap.read()
        if not ret:
            break

        # Convert to grayscale (simplifies comparison)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if prev_frame is not None:
            # Frame difference = motion estimate
            diff = cv2.absdiff(prev_frame, gray)
            motion_sum += np.mean(diff)

        prev_frame = gray
        frame_count += 1

    cap.release()

    # Avoid division errors
    if frame_count == 0:
        return 0

    # Normalize score
    raw_score = motion_sum / frame_count

    # Scale to 0–100 (tuned scaling factor)
    score = min(100, raw_score)

    return round(score, 2)