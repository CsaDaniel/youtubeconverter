from flask import Flask, request, send_file, render_template
from pytube import YouTube
from moviepy.editor import *
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    # Get the YouTube video URL from the user input
    url = request.form.get('url')

    # Create a YouTube object with the video URL
    video = YouTube(url)

    # Get the highest resolution video stream
    stream = video.streams.get_highest_resolution()

    # Download the video stream to a local file
    video_path = f"{video.title}.mp4"
    stream.download(output_path=".", filename=video_path)

    # Check if the user wants to download an MP4 file
    format = request.form.get('format')
    if format == 'mp4':
        # Send the MP4 file as a response to the user's browser
        return send_file(video_path, as_attachment=True)

    # Convert the video to MP3 format
    audio_path = f"{video.title}.mp3"
    clip = AudioFileClip(video_path)
    clip.write_audiofile(audio_path)

    # Delete the original video file
    os.remove(video_path)

    # Send the MP3 file as a response to the user's browser
    return send_file(audio_path, as_attachment=True)




if __name__ == '__main__':
    app.run(debug=True)