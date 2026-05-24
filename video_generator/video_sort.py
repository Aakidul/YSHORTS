import os

VIDEO_DIR = "/home/aaki/TRAPPIST-1E/video_generator/videos"

def get_newest_video_stamp():
    files = os.listdir(VIDEO_DIR)

    video_timestamps = []

    for video in files:
        if not video.endswith(".mp4"):
            continue

        timestamp = video.replace(".mp4", "")
        video_timestamps.append(int(timestamp))

    if not video_timestamps:
        raise FileNotFoundError("No video files found")

    sorted_timestamp = sorted(video_timestamps, reverse=True)
    return sorted_timestamp[0]


def get_new_video_path():
    data = get_newest_video_stamp()
    new_video_path = os.path.join(VIDEO_DIR, f"{data}.mp4")
    return new_video_path
