import librosa
import numpy as np

def audio_energy_score(video_path):
    """
    Extract audio energy from video
    Output: 0–100 score
    """

    try:
        y, sr = librosa.load(video_path, sr=None)

        rms = librosa.feature.rms(y=y)[0]
        energy = np.mean(rms)

        # scale to 0–100
        score = min(100, energy * 200)

        return round(score, 2)

    except Exception:
        return 0