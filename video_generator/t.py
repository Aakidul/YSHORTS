import os

path = '/home/aaki/TRAPPIST-1E/video_generator/videos'

os.chdir(path)

files = os.listdir()

def get_newest_video_stamp():


    video_timestamps = []

    for videos in files:
        video_stamp = videos.split(".")
        print(video_stamp)

get_newest_video_stamp()
