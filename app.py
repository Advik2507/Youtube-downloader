import os
import yt_dlp
from flask import Flask, request, send_file

app = Flask(__name__)

# Set up the route for downloading videos
@app.route('/download', methods=['GET'])
def download_video():
    # Get the YouTube video URL from the query string
    video_url = request.args.get('url')
    if not video_url:
        return "Error: No URL provided", 400

    # Set up options for yt-dlp (customize the output format if needed)
    ydl_opts = {
        'outtmpl': 'downloads/%(title)s.%(ext)s',  # Downloads to 'downloads' folder with the video title
        'format': 'bestvideo+bestaudio/best',  # Highest quality video and audio
    }

    # Download the video using yt-dlp
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            video_title = info_dict.get('title', 'video')
            video_file = f"downloads/{video_title}.mp4"
    except Exception as e:
        return f"Error downloading video: {str(e)}", 500

    # Return the downloaded video file
    if os.path.exists(video_file):
        return send_file(video_file, as_attachment=True)
    else:
        return "Error: Video not found", 404

if __name__ == '__main__':
    if not os.path.exists('downloads'):
        os.makedirs('downloads')  # Create 'downloads' folder if it doesn't exist
    app.run(debug=True)
