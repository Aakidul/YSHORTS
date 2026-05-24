from gtts import gTTS
import subprocess
import json
import os

RAW = "raw.mp3"
FINAL = "/home/aaki/TRAPPIST-1E/video_generator/music/voice_10s.mp3"
TARGET = 10.0  # target duration in seconds

def save_10s_voice(text, output_path=FINAL):
    """
    Generate gTTS audio from `text`, adjust speed to exactly 10s, and save as MP3.
    """
    # 1) Generate initial gTTS mp3
    gTTS(text=text, lang="en", slow=False).save(RAW)

    # 2) Measure original duration
    def duration(file):
        r = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration",
             "-of", "json", file],
            capture_output=True, text=True, check=True
        )
        return float(json.loads(r.stdout)["format"]["duration"])

    orig_dur = duration(RAW)

    # 3) Build atempo chain
    def build_atempo_chain(factor):
        filters = []
        while factor < 0.5:
            filters.append("atempo=0.5")
            factor /= 0.5
        filters.append(f"atempo={factor:.6f}")
        return ",".join(filters)

    speed_factor = orig_dur / TARGET
    if speed_factor <= 0:
        speed_factor = 1.0
    chain = build_atempo_chain(speed_factor)

    # 4) Apply chain, pad and cut to exactly TARGET seconds
    cmd = [
        "ffmpeg", "-y",
        "-i", RAW,
        "-af", f"{chain},apad=pad_dur={int(TARGET)}",
        "-t", str(TARGET),
        output_path
    ]
    subprocess.run(cmd, check=True)

    # Remove raw temporary mp3
    if os.path.exists(RAW):
        os.remove(RAW)

    print(f"✔ Saved {output_path} | original={orig_dur:.2f}s → target={TARGET}s")
    return output_path
