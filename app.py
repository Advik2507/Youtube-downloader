from flask import Flask, render_template_string, request
import yt_dlp
import os

app = Flask(__name__)

# Ensure that the 'downloads' folder exists
if not os.path.exists('downloads'):
    os.makedirs('downloads')

# Function to download the video or audio
def download_media(url, quality, media_type, audio_quality):
    if media_type == 'audio':
        if audio_quality == '320k':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '320',
                }],
            }
        elif audio_quality == '256k':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '256',
                }],
            }
        elif audio_quality == '192k':
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
                'postprocessors': [{
                    'key': 'FFmpegAudio',
                    'preferredcodec': 'mp3',
                    'preferredquality': '192',
                }],
            }

    else:  # Video download
        if quality == 'best':
            ydl_opts = {
                'format': 'bestvideo+bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }
        else:
            ydl_opts = {
                'format': f'bestvideo[height={quality}]+bestaudio/best',
                'outtmpl': 'downloads/%(title)s.%(ext)s',
            }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        return f"Download complete! {media_type.capitalize()} quality: {quality if media_type == 'video' else audio_quality}."
    except Exception as e:
        return f"An error occurred: {str(e)}"

# Main route
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        url = request.form['url']
        quality = request.form['quality']
        media_type = request.form['media_type']
        audio_quality = request.form.get('audio_quality', '192k')
        message = download_media(url, quality, media_type, audio_quality)
        return render_template_string(HTML_FORM, message=message)
    return render_template_string(HTML_FORM, message=None)

# HTML form
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

        <label for="audio_quality">Select Audio Quality (Only for Audio Downloads):</label>
        <select name="audio_quality" id="audio_quality">
            <option value="192k">192 kbps</option>
            <option value="256k">256 kbps</option>
            <option value="320k">320 kbps</option>
        </select><br><br>

        <input type="submit" value="Download">
    </form>
</body>
</html>
'''

# Run with environment PORT (for Render)
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
