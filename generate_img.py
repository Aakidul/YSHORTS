import requests as rq
import time
import sys
import os

sys.path.append("/home/aaki/TRAPPIST-1E/video_generator")
from get_video import generate_video
sys.path.append("/home/aaki/TRAPPIST-1E/video_generator")
from video_sort import get_new_video_path

IMG_DIR = '/home/aaki/TRAPPIST-1E/image_generator/images'
os.makedirs(IMG_DIR, exist_ok=True)

RETRY_WAIT = 60  # 1 minute between attempts
MAX_RETRIES = 3  # optional per attempt

def image_get(prompt):
    """
    Poll Pollinations API until an image is successfully generated.
    Only returns video path when both image and video are ready.
    Infinite retry every RETRY_WAIT seconds.
    """
    prompt_safe = prompt.replace(' ', '+')

    while True:  # infinite loop
        attempt = 0
        while attempt < MAX_RETRIES:
            attempt += 1
            stamp = int(time.time())
            content_name = f'{stamp}.jpg'
            image_path = os.path.join(IMG_DIR, content_name)
            url = 'https://www.imfin.it/api/generate?prompt=' + str(prompt_safe) + '&model=gemini&size=1024x1792'


            try:
                res = rq.get(url, timeout=300)
                if res.status_code == 200 and res.content:
                    # save image fully
                    with open(image_path, 'wb') as f:
                        f.write(res.content)
                        f.flush()
                        os.fsync(f.fileno())
                    print(f"[DEBUG] Image generated for: {prompt}")
                    print(f"[SAVED] IMG SAVED at {image_path}")

                    # generate video immediately
                    generate_video()
                    video_path = get_new_video_path()
                    if video_path:
                        return str(video_path)
                    else:
                        print("[ERROR] Video path not found after generation, retrying...")

                else:
                    print(f"[ERROR] Image API returned status: {res.status_code} (Attempt {attempt}/{MAX_RETRIES})")

            except Exception as e:
                print(f"[ERROR] Exception occurred: {e} (Attempt {attempt}/{MAX_RETRIES})")

            # non-blocking wait between retries
            start = time.time()
            while time.time() - start < RETRY_WAIT / MAX_RETRIES:
                pass  # busy-wait small fraction of RETRY_WAIT

        print(f"[INFO] All {MAX_RETRIES} attempts failed, retrying in {RETRY_WAIT} seconds...")

        # wait 1 minute before next infinite loop iteration
        start = time.time()
        while time.time() - start < RETRY_WAIT:
            pass
