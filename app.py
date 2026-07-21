from flask import Flask, render_template, request
import os
import re
from googleapiclient.discovery import build


app = Flask(__name__)


UPLOAD_FOLDER = "uploads"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs("static", exist_ok=True)



# -----------------------------------
# YouTube API Configuration
# -----------------------------------

YOUTUBE_API_KEY = os.environ.get("AIzaSyB_P1_VjIVAc_-_nPvlKmnDkufJRGt8spE")
#YOUTUBE_API_KEY = "AIzaSyB_P1_VjIVAc_-_nPvlKmnDkufJRGt8spE"



# -----------------------------------
# Extract YouTube Information
# -----------------------------------

def extract_platform_data(url):

    match = re.search(
        r"(?:v=|\/)([0-9A-Za-z_-]{11})",
        url
    )

    if not match:
        raise Exception("Invalid YouTube URL")


    video_id = match.group(1)


    youtube = build(
        "youtube",
        "v3",
        developerKey=YOUTUBE_API_KEY
    )


    response = youtube.videos().list(
        part="snippet,statistics",
        id=video_id
    ).execute()


    if not response.get("items"):
        raise Exception("Video not found")


    item = response["items"][0]


    snippet = item["snippet"]
    stats = item["statistics"]


    return {

        "title": snippet.get(
            "title",
            ""
        ),

        "channel": snippet.get(
            "channelTitle",
            ""
        ),

        "views": int(
            stats.get(
                "viewCount",
                0
            )
        ),

        "likes": int(
            stats.get(
                "likeCount",
                0
            )
        ),

        "comments": int(
            stats.get(
                "commentCount",
                0
            )
        ),

        "platform": "YouTube",

        "thumbnail":
            snippet["thumbnails"]["high"]["url"]

    }



# -----------------------------------
# Home
# -----------------------------------

@app.route("/", methods=["GET", "POST"])
def home():

    result = None


    if request.method == "POST":


        url = request.form.get("url")

        video = request.files.get("video")



        # ==================================================
        # OPTION 1 : YOUTUBE URL
        # ==================================================

        if url:


            try:

                data = extract_platform_data(url)


            except Exception as e:

                print(e)

                return render_template(
                    "index.html",
                    result=None,
                    error=f"❌ {e}"
                )



            likes = data["likes"]

            comments = data["comments"]

            views = data["views"]



            like_rate = (
                (likes / views) * 100
                if views else 0
            )


            comment_rate = (
                (comments / views) * 100
                if views else 0
            )



            view_score = min(
                40,
                views / 2500
            )


            like_score = min(
                35,
                like_rate * 7
            )


            comment_score = min(
                25,
                comment_rate * 250
            )



            performance_score = round(

                view_score
                +
                like_score
                +
                comment_score

            )



            if performance_score >= 75:

                label = "🔥 High Performing Video"


            elif performance_score >= 50:

                label = "⚡ Moderately Performing"


            else:

                label = "❌ Low Performing"




            result = {


                "mode": "url",

                "platform": data["platform"],

                "title": data["title"],

                "channel": data["channel"],

                "thumbnail": data["thumbnail"],

                "views": views,

                "likes": likes,

                "comments": comments,

                "like_rate": round(
                    like_rate,
                    2
                ),

                "comment_rate": round(
                    comment_rate,
                    2
                ),

                "performance_score":
                    performance_score,

                "label":
                    label

            }



        # ==================================================
        # OPTION 2 : VIDEO UPLOAD
        # ==================================================


        elif video and video.filename:


            from video_analyzer import analyze_video



            save_path = os.path.join(
                UPLOAD_FOLDER,
                video.filename
            )



            video.save(save_path)



            analysis = analyze_video(
                save_path
            )



            virality_score = (

                (analysis["motion_score"] or 0)
                * 0.15

                +

                analysis["scene_changes"]
                * 0.10

                +

                analysis["hook_score"]
                * 0.25

                +

                analysis["emotion_score"]
                * 0.20

                +

                analysis["audio_energy_score"]
                * 0.20

                +

                analysis["face_count"]
                * 2

            )



            virality_score = min(
                100,
                round(
                    virality_score,
                    2
                )
            )



            if virality_score >= 75:

                label = "🔥 High Viral Potential"


            elif virality_score >= 50:

                label = "⚡ Medium Viral Potential"


            else:

                label = "❌ Low Viral Potential"




            suggestions = []



            if analysis["face_count"] == 0:

                suggestions.append(
                    "Add a human face in the opening seconds"
                )


            if analysis["motion_score"] < 20:

                suggestions.append(
                    "Increase movement and pacing"
                )


            if analysis["scene_changes"] < 10:

                suggestions.append(
                    "Use more scene transitions"
                )


            if analysis["brightness"] < 90:

                suggestions.append(
                    "Improve lighting"
                )


            if analysis["contrast"] < 30:

                suggestions.append(
                    "Increase visual contrast"
                )


            if not suggestions:

                suggestions.append(
                    "Video already has strong viral indicators"
                )



            result = {

                **analysis,

                "mode":
                    "upload",

                "virality_score":
                    virality_score,

                "label":
                    label,

                "suggestions":
                    suggestions

            }



    return render_template(
        "index.html",
        result=result,
        error=None
    )



if __name__ == "__main__":

    app.run(
        host="0.0.0.0",
        port=5000
    )