import os
import numpy
import yt_dlp
from spleeter.separator import Separator
import logging

logging.getLogger('spleeter').setLevel(logging.ERROR)
def check_folders_and_models():
    if not os.path.exists('raw_videos'):
        os.makedirs('raw_videos')
    if not os.path.exists('splitted_audios'):
        os.makedirs('splitted_audios')
    
def download_youtube_video():
    yt_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'raw_videos/%(title)s.%(ext)s',
        'noplaylist': True,
        'quiet':True,
        'no_warnings':True,
        'noprogress':True,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }
    
    ydl = yt_dlp.YoutubeDL(yt_opts)
    
    youtube_video_url = input("Enter YouTube video URL: ")
    
    try:
        print("Downloading video")
        ydl.download(youtube_video_url)
        print("Video ready at: raw_videos")
    except Exception as e:
        print(f"Video download failed! ❌ Error: {e}")
        
def split_music(stems:int=2):
    all_files = [os.path.join('raw_videos', f) for f in os.listdir('raw_videos')]
    most_recent_file = max(all_files, key=os.path.getmtime)
    separator = Separator(f'spleeter:{stems}stems')

    # # Separate the audio file and save the output
    output_folder = "splitted_audios"
    separator.separate_to_file(most_recent_file, output_folder)

if __name__ == '__main__':
    check_folders_and_models()
    download_youtube_video()
    stems = input('Stems: 2, 4 or 5: ')
    if stems in ['2','4','5']:
        stems = int(stems)
        split_music(stems = stems)
    else:
        print('Stems will be 2, for separating voice and Music')
        split_music(stems = 2)








        