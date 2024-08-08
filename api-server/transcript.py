import moviepy.editor as mp
import whisper
import os

def extract_audio(video_file):
    video = mp.VideoFileClip(video_file)
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file, codec='pcm_s16le')
    return audio_file

def generate_transcript(audio_file):
    model = whisper.load_model("base")
    result = model.transcribe(audio_file)
    transcript = result['text']
    return transcript

def save_transcript(transcript, output_file):
    with open(output_file, 'w') as file:
        file.write(transcript)

def generate_transcript_file(video_file, output_file):
    audio_file = extract_audio(video_file)
    transcript = generate_transcript(audio_file)
    save_transcript(transcript, output_file)
    os.remove(audio_file)

# Example usage:
# video_file = "./Video 4 - Krista Farmer Project Manager.mp4"
# output_file = "Video 4 - Krista Farmer Project Manager.txt"
# generate_transcript_file(video_file, output_file)
