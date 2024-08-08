import moviepy.editor as mp
import whisper
import os

def extract_audio(video_file):
   
    video = mp.VideoFileClip(video_file)    
    audio_file = "extracted_audio.wav"
    video.audio.write_audiofile(audio_file, codec='pcm_s16le')    
    return audio_file

def generate_subtitles(audio_file):
    
    model = whisper.load_model("base")    
    result = model.transcribe(audio_file)    
    segments = result['segments']
    
    subtitles = ""
    for segment in segments:
        start = segment['start']
        end = segment['end']
        text = segment['text']
        
        subtitles += f"{format_timestamp(start)} --> {format_timestamp(end)}\n{text}\n\n"    
    return subtitles

def format_timestamp(seconds):
    
    hours = int(seconds // 3600)
    minutes = int((seconds % 3600) // 60)
    seconds = int(seconds % 60)
    milliseconds = int((seconds % 1) * 1000)
    
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

def save_subtitles(subtitles, output_file):
    with open(output_file, 'w') as file:
        file.write(subtitles)

def generate_subtitle_file(video_file, output_file):    
    audio_file = extract_audio(video_file)    
    subtitles = generate_subtitles(audio_file)   
    save_subtitles(subtitles, output_file)
    os.remove(audio_file)
    


# video_file = "./Video 4 - Krista Farmer Project Manager.mp4"
# output_file = "Video 4 - Krista Farmer Project Manager.srt"
# generate_subtitle_file(video_file, output_file)
