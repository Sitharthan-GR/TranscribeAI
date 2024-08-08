from flask import Flask, request, jsonify,send_file
import whisper
from moviepy.editor import VideoFileClip
from transformers import pipeline
from summary import summarize_text,extract_audio,transcribe_audio_with_whisper
from flask_cors import CORS,cross_origin
from subtitle import generate_subtitle_file
from transcript import generate_transcript_file

app = Flask(__name__)
CORS(app)
# app.config['CORS_HEADERS'] = 'Content-Type'
# CORS(app, resources={r"/check": {"origins": "http://localhost:5173"}})


@app.route("/members")
# @cross_origin(origins=['http://localhost:3000'])
def members():
    # response = jsonify(message="Simple server is running")
    # response.headers.add("Access-Control-Allow-Origin", "*")
    return {"members":["Members1","Members2","Members3"]}

@app.route('/summarize_video', methods=['POST'])
# @cross_origin()
# @cross_origin(origins='http://localhost:5173')
def summarize_video():
    video_file = request.files['video']
    video_path = "./video.mp4"
    audio_path = "extracted_audio.wav"

    video_file.save(video_path)

    extract_audio(video_path, audio_path)
    transcription = transcribe_audio_with_whisper(audio_path)
    summary = summarize_text(transcription)

    return jsonify({"summary": summary})



@app.route('/generate_subtitle', methods=['POST'])
# @cross_origin()
# @cross_origin(origins='http://localhost:5173')
def generate_subtitle():
    # print("request: "+str(request))
    video_file = request.files['video']
    # video_title = request.files['title']
    srtFile = "./temp.srt"
    video_path = "./video.mp4"
    # audio_path = "extracted_audio.wav"

    video_file.save(video_path)

    
    
    subtitle = generate_subtitle_file(video_path,srtFile)
    try:
        return send_file(srtFile,as_attachment=True)    
    except FileNotFoundError:
        return "File not found", 404

@app.route('/generate_transcript', methods=['POST'])
# @cross_origin()
# @cross_origin(origins='http://localhost:5173')
def generate_transctipt():
    # print("request: "+str(request))
    video_file = request.files['video']
    # video_title = request.files['title']
    srtFile = "./temp.txt"
    video_path = "./video.mp4"
    # audio_path = "extracted_audio.wav"

    video_file.save(video_path)

    
    
    subtitle = generate_transcript_file(video_path,srtFile)
    try:
        return send_file(srtFile,as_attachment=True)    
    except FileNotFoundError:
        return "File not found", 404


@app.route('/check', methods=['POST'])
# @cross_origin(origins='http://localhost:5173')
def checkping():
    
    return jsonify({"result": "hello success"})


if __name__ == '__main__':
    app.run(debug=True)
