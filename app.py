
from flask import Flask, request, jsonify, send_file
import yt_dlp
import os
import uuid

app = Flask(__name__)

@app.route("/")
def home():
    return "🎵 Highrise MP3 Server is running!"

@app.route("/song")
def get_song():
    query = request.args.get("q")
    if not query:
        return jsonify({"error": "No query provided"}), 400

    temp_dir = "/tmp"
    filename = f"{uuid.uuid4().hex}.mp3"
    filepath = os.path.join(temp_dir, filename)

    ydl_opts = {
        "format": "bestaudio/best",
        "noplaylist": True,
        "quiet": True,
        "outtmpl": filepath,
        "postprocessors": [{
            "key": "FFmpegExtractAudio",
            "preferredcodec": "mp3",
            "preferredquality": "192",
        }],
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        try:
            ydl.download([f"ytsearch1:{query}"])
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    return send_file(filepath, mimetype="audio/mpeg", as_attachment=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
