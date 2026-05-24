import sys
import os
import subprocess
import time
sys.path.append("/home/aaki/TRAPPIST-1E/image_generator")
from image_sort import get_img_path_new



time_now = str(int(time.time()))

image_path = str(get_img_path_new())
music_path = "bg_music.mp3"
output_dir = "/home/aaki/TRAPPIST-1E/video_generator" + "/videos"
output_path = os.path.join(output_dir, str(time_now) + ".mp4")

# Ensure output directory exists
os.makedirs(output_dir, exist_ok=True)

# FFmpeg command: crop bottom 100px, scale to 1080x1920, loop image for 10s with music

"""
 f'ffmpeg -loop 1 -i "{image_path}" -i "{music_path}" '

"""

def generate_video():
    ffmpeg_cmd = (
        f'ffmpeg -loop 1 -i "{image_path}"'
        f' -t 10 '
        f'-vf "crop=iw:ih-130:0:0,'  # crop 130px from bottom
        f'zoompan=z=\'zoom+0.0008\':x=\'iw/4\':y=0:d=250,'  # subtle zoom
        f'rotate=PI/180*0.3,'  # slight rotation
        f'vignette,'  # vignette effect
        f'eq=contrast=1.1:brightness=0.02:saturation=1.05,'  # color adjust
        f'unsharp=5:5:0.5,'  # sharpen
        f'scale=1080:1920" '
        f'-c:v libx264 -c:a aac -shortest -pix_fmt yuv420p -crf 18 "{output_path}" -y'
    )

    print("[DEBUG] video generated using image:", image_path)

    subprocess.run(ffmpeg_cmd, shell=True, check=True)
    return 0

