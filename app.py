from flask import Flask, render_template_string, request
import yt_dlp
import os

app = Flask(__name__)

# Ensure that the 'downloads' folder exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Function to download the video or audio
def download_media(url, quality, media_type):
    if media_type == 'audio':
        ydl_opts = {
            'format': 'bestaudio/best',  # Best audio quality
            'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output path and filename
            'postprocessors': [{
                'key': 'FFmpegAudio',
                'preferredcodec': 'mp3',  # Convert audio to MP3
                'preferredquality': '192',  # MP3 quality
            }],
        }
    else:
        if quality == 'best':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',  # Best video and audio quality
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output path and filename
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height={quality}]+bestaudio/best',  # Specific resolution
                'outtmpl': 'downloads/%(title)s.%(ext)s',  # Output path and filename
            }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])  # Starts the download
        return f"Download complete! {media_type.capitalize()} quality: {quality if media_type == 'video' else ''}"
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main route for the app
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']  # Video URL from the form
        quality = request.form['quality']  # Video quality from the dropdown
        media_type = request.form['media_type']  # Video or audio type from the form
        message = download_media(url, quality, media_type)  # Call the download function with quality and media type
        return render_template_string(HTML_FORM, message=message)
    
    return render_template_string(HTML_FORM, message=None)

# HTML Form Template
HTML_FORM = '''
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>YouTube Downloader</title>
</head>
<body>
    <h1>YouTube Video/Audio Downloader</h1>
    {% if message %}
        <p><strong>{{ message }}</strong></p>
    {% endif %}

    <form method="post">
        <label for="url">Video URL:</label>
        <input type="text" name="url" id="url" placeholder="Enter the video URL" required><br><br>

        <label for="media_type">Select Media Type:</label>
        <select name="media_type" id="media_type">
            <option value="video">Video</option>
            <option value="audio">Audio (MP3)</option>
        </select><br><br>

        <label for="quality">Select Video Quality (Only for Video Downloads):</label>
        <select name="quality" id="quality">
            <option value="best">Best Quality (Video + Audio)</option>
            <option value="1080p">1080p</option>
            <option value="720p">720p</option>
            <option value="480p">480p</option>
            <option value="360p">360p</option>
        </select><br><br>

        <input type="submit" value="Download">
    </form>
</body>
</html>
'''

if __name__ == '__main__':
    app.run(debug=True)
