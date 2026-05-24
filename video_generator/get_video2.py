import sys
import os
import subprocess
import time
from voice import save_10s_voice
from gtts import gTTS

time_now = str(int(time.time()))

music_path = "bg_music.mp3"
output_dir = "/home/aaki/TRAPPIST-1E/video_generator" + "/videos"
output_path = os.path.join(output_dir, str(time_now) + ".mp4")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# FFmpeg command: crop bottom 100px, scale to 1080x1920, loop image for 10s with music

"""
 f'ffmpeg -loop 1 -i "{image_path}" -i "{music_path}" '

"""



def generate_video(image_path, speech):
    music_file =  save_10s_voice(speech)
    music_path = str(music_file)
    ffmpeg_cmd = (
    f'ffmpeg -y '
    f'-loop 1 -i "{image_path}" '
    f'-i "{music_path}" '
    f'-t 10 '
    f'-vf "scale=1080:1920:force_original_aspect_ratio=increase,'
    f'crop=1080:1920,setsar=1,setdar=9/16,fps=30" '
    f'-c:v libx264 -preset slow -crf 18 '
    f'-pix_fmt yuv420p '
    f'-movflags +faststart '
    f'-c:a aac -b:a 128k -shortest '
    f'"{output_path}"'
)



    print("[DEBUG] video generated using image:", image_path)

    subprocess.run(ffmpeg_cmd, shell=True, check=True)
    return output_path



