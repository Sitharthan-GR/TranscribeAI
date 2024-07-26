import yt_dlp
import ffmpeg
import whisper
import os
import time


def get_audio_stream_url(youtube_url):
    ydl_opts = {
        'format': 'bestaudio',
        'noplaylist': True,
        'quiet': True,
        'no_warnings': True,
        'extract_flat': 'in_playlist'
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(youtube_url, download=False)
        audio_stream_url = info['url']
        return audio_stream_url

def extract_audio(stream_url, duration=10):
    ffmpeg.input(stream_url).output('audio.wav', format='wav', acodec='pcm_s16le', ac=1, ar='44100', t=duration).run()


def transcribe_audio():
    model = whisper.load_model("base")  
    result = model.transcribe("audio.wav")
    return result["text"]


def transcribe_youtube_live(youtube_url, duration=10):
    stream_url = get_audio_stream_url(youtube_url)
    
    while True:
        extract_audio(stream_url, duration)
        transcription = transcribe_audio()
        print("Transcription: " + transcription)
        
        
        os.remove('audio.wav')
        
        
        time.sleep(duration)


youtube_url = 'https://www.youtube.com/watch?v=Qeg-4kS9Hbo'


transcribe_youtube_live(youtube_url)
