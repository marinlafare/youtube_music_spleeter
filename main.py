import os
import re
import logging
import os
from pathlib import Path
import yt_dlp
from spleeter.separator import Separator

logging.getLogger('spleeter').setLevel(logging.ERROR)

def sanitize_filename(filename):
    """
    Sanitizes a string to be a valid filename.
    Removes invalid characters and replaces spaces with underscores.
    """
    # Remove characters that are not alphanumeric, spaces, or hyphens
    s = re.sub(r'[^\w\s-]', '', filename)
    # Replace one or more spaces with a single underscore
    s = re.sub(r'\s+', '_', s)
    return s.strip()

def download_and_split(youtube_url, stems: int):
    """
    Downloads a YouTube video as an MP3 and splits it into the specified number of stems.
    """
    try:
        # Step 1: Download the video as an MP3 audio file
        print(f"Downloading audio from {youtube_url}...")
        
        # Get video title from yt-dlp without downloading
        yt_opts_title = {
            'noplaylist': True,
            'quiet': True,
            'skip_download': True,
        }
        with yt_dlp.YoutubeDL(yt_opts_title) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
            video_title = info.get('title', 'video')

        sanitized_title = sanitize_filename(video_title)
        output_path_template = os.path.join('raw_videos', f'{sanitized_title}.%(ext)s')

        yt_opts = {
            'format': 'bestaudio/best',
            'outtmpl': output_path_template,
            'noplaylist': True,
            'quiet': True,
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            }],
        }
        
        with yt_dlp.YoutubeDL(yt_opts) as ydl:
            ydl.download([youtube_url])
        
        mp3_path = os.path.join('raw_videos', f'{sanitized_title}.mp3')
        if not os.path.exists(mp3_path):
            raise FileNotFoundError(f"Downloaded file not found at {mp3_path}")

        print("Download complete.")

        # Step 2: Use Spleeter to split the audio
        print(f"Splitting audio from '{sanitized_title}' into {stems} stems...")
        
        separator = Separator(f'spleeter:{stems}stems')
        output_folder = "splitted_audios"
        separator.separate_to_file(mp3_path, output_folder)
        
        print(f"Splitting complete. The files are located in the '{os.path.join(output_folder, sanitized_title)}' folder.")
    
    except Exception as e:
        print(f"An error occurred: {e}")
        print("Please check the URL or try again.")

def check_folders():
    """Ensures necessary directories exist."""
    os.makedirs('raw_videos', exist_ok=True)
    os.makedirs('splitted_audios', exist_ok=True)

if __name__ == '__main__':
    check_folders()
    while True:
        try:
            youtube_url = input("YouTube URL (or press Enter to exit): ")
            if not youtube_url:
                print("Bye bye then")
                break
            
            stems_input = input("Enter number of stems (2, 4, or 5): ")
            stems = int(stems_input) if stems_input in ['2', '4', '5'] else "IDK"
            
            if stems == "IDK":
                print(f"I don't know what {stems} means. I'll just assume is 2")
                stems = 2
            
            download_and_split(youtube_url, stems)
        except:
            print('SOMETHING HAPPENED!!!!!!! SOMETHING FAILED!!!!!!!!')
