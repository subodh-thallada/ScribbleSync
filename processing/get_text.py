from flask import Flask, request, render_template
import os

# from get_theme import theme_prompts

import subprocess
import random
import numpy as np


app = Flask(__name__)

uploads_dir = os.path.join(app.instance_path, 'uploads')
static_dir = os.path.join(app.root_path, 'static')
os.makedirs(uploads_dir, exist_ok=True)


@app.route('/upload')
def index():
    return render_template('upload.html')


@app.route('/')
def page():
    return render_template('page.html')


def convert_video_format(input_path, output_path):
    """Convert video to a compatible format using FFmpeg."""
    try:
        command = ['ffmpeg', '-i', input_path, '-c:v', 'libx264', '-strict', '-2', output_path]
        subprocess.run(command, check=True)
        return output_path
    except subprocess.CalledProcessError as e:
        raise ValueError(f"Error converting video format: {e}")



@app.route('/upload', methods=['POST'])
def upload_video():
    if 'video' not in request.files:
        return 'No video file part', 400

    video = request.files['video']
    theme = request.form['theme']
    theme_prompt = "Ensure a professional tone, with appropriate marketing music"

    if video.filename == '':
        return 'No selected file', 400

    video_path = os.path.join(uploads_dir, video.filename)
    video.save(video_path)

    try:
        audio_path = extract_audio(video_path)
        transcript = transcribe_audio(audio_path)
    except ValueError as e:
        return str(e), 500

    if theme in theme_prompts:
        theme_prompt = theme_prompts[theme]

    video_clip = VideoFileClip(video_path)

    # mix the soundtrack with the original audio
    video_clip = mix_soundtrack(video_clip, theme)

    # apply filters based on theme
    video_clip = apply_filters(video_clip, theme)

    # Generate Custom BGM
    # caption = get_caption(video_clip.get_frame(5))
    # generate_music(transcript, caption)

    # Upscale the resolution of the video
    # upscale_video(video_clip)

    # save the edited video
    edited_video_filename = 'edited_' + os.path.splitext(video.filename)[0] + '.mp4'
    edited_video_path = os.path.join(static_dir, edited_video_filename)
    video_clip.write_videofile(edited_video_path, codec='libx264')

    return render_template('result.html', transcript=transcript, video_filename=edited_video_filename, theme_prompt=theme_prompt)


if __name__ == '__main__':
    app.run(debug=False)