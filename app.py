from flask import Flask, Response, stream_with_context, render_template_string, request, send_file
import requests
from werkzeug.datastructures import Headers
from werkzeug.wsgi import FileWrapper

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<title>Video Streaming Example</title>
<link rel="stylesheet" href="/static/style.css">
</head>
<body>

<div class="title">SPY-CLI-X</div>

<video controls width="640" autoplay>
    <source src="/stream?id={{ video_path }}" type="video/mp4">
    Your browser does not support the video tag.
</video>

</body>
</html>
"""

@app.route('/spyclix/stream/')
def index():
    video_path = request.args.get('id')
    print(video_path)
    if video_path:
        # Render the template with the video path
        return render_template_string(HTML_TEMPLATE, video_path=video_path)
    else:
        # Return a default page or error if the video path is not provided
        return "Video ID not provided", 400

@app.route('/stream')
def video_stream():
    video_path = request.args.get('id')
    if not video_path:
        return "Video path not provided", 400
    
    video_url = f"https://www.eporner.com/{video_path}"
    print(video_url)
    
    range_header = request.headers.get('Range')
    headers = {}
    if range_header:
        headers['Range'] = range_header
    
    req = requests.get(video_url, headers=headers, stream=True)
    return Response(stream_with_context(req.iter_content(chunk_size=1024)),
                    content_type=req.headers['Content-Type'],
                    status=req.status_code,
                    headers=dict(req.headers))

if __name__ == '__main__':
    app.run(debug=True, port=5000)
