import whisper
from moviepy.editor import VideoFileClip
from transformers import pipeline

def extract_audio(video_path, audio_path):
    video = VideoFileClip(video_path)
    video.audio.write_audiofile(audio_path)

def transcribe_audio_with_whisper(audio_path):
    model = whisper.load_model("base")
    result = model.transcribe(audio_path)
    return result["text"]

def summarize_text(text):
    summarizer = pipeline("summarization")
    summary = summarizer(text, max_length=130, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def summarize_video(video_path):
    audio_path = "extracted_audio.wav"
    extract_audio(video_path, audio_path)
    transcription = transcribe_audio_with_whisper(audio_path)
    summary = summarize_text(transcription)
    return summary

# video_summary = summarize_video("/Users/sidhu/Documents/PartTime-job/ALT MEDIA/Fall2024/Video 3 - Jonathan Greyson, Intel.mov")
# print(video_summary)
