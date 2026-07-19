from video_analyzer import analyze_video

# Replace this with the actual filename inside uploads/
video_path = "uploads/test.mp4"

result = analyze_video(video_path)

print("Video Analysis Results:")
print("-----------------------")
print(f"Duration: {result['duration']} seconds")
print(f"FPS: {result['fps']}")
print(f"Width: {result['width']}")
print(f"Height: {result['height']}")