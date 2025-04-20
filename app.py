import os
import re
import base64
import yt_dlp
from flask import Flask, request, send_file, jsonify, render_template

app = Flask(__name__)

# Decode the cookies from environment variable ONCE during app start
cookies_base64 = os.getenv('YT_COOKIES_BASE64')
if cookies_base64:
    cookies = base64.b64decode(cookies_base64).decode('utf-8')
    with open('cookies.txt', 'w', encoding='utf-8') as f:
        f.write(cookies)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download_video():
    video_url = request.args.get('url')
    if not video_url:
        return jsonify({'error': 'No URL provided'}), 400

    download_dir = os.path.join(os.getcwd(), 'downloads')
    os.makedirs(download_dir, exist_ok=True)

    # Set download options
    ydl_opts = {
        'outtmpl': os.path.join(download_dir, '%(title)s.%(ext)s'),
        'format': 'bestvideo+bestaudio/best',
        'merge_output_format': 'mp4',
        'cookies': 'cookies.txt'  # Tell yt-dlp to use the decoded cookies
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(video_url, download=True)
            title = info_dict.get('title', 'video')
            clean_title = re.sub(r'[\\/*?:"<>|]', "", title)
            video_file = os.path.join(download_dir, f"{clean_title}.mp4")

        if os.path.exists(video_file):
            return send_file(video_file, as_attachment=True)
        else:
            return jsonify({'error': 'Downloaded file not found'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
