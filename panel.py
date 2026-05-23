import os
import hashlib
import sys
import subprocess
import time
import random

sys.path.append("/home/aaki/TRAPPIST-VIEW")
from imagine import search_image

sys.path.append("/home/aaki/TRAPPIST-1E/modules")
from sleepy import tsleep

sys.path.append("/home/aaki/TRAPPIST-1E/video_generator")
from video_sort import get_new_video_path

sys.path.append("/home/aaki/TRAPPIST-1E/platforms")
from youtube_uploader import upload_video

sys.path.append("/home/aaki/TRAPPIST-1E/spider-web")
from GOOGLE_NEWS_SCRAPER import get_news

sys.path.append("/home/aaki/TRAPPIST-1E/image_generator")

sys.path.append("/home/aaki/TRAPPIST-1E/video_generator")
from get_video2 import generate_video

news = get_news()

hashes = []
news_with_hash = []


for newz in news:
    newy = str(newz)
    content = newy.encode("utf-8")
    hash = hashlib.sha256(content).hexdigest()
    hashes.append(hash)
    news_with_hash.append({hash: newz})

#REMOVING DUPLICATE NEWS, GETTING FRESH
def check_duplicate():

    hash_readed = []
    try:
        with open("/home/aaki/TRAPPIST-1E/logs.txt", "r") as f:
            try:
                for lines in f:
                    hash_read = lines.strip()
                    hash_readed.append(hash_read)

            except Exception as e:
                print("NO DATA ERROR")
    except Exception as e:
        print("FILE ERROR")


    fresh_news = []
    combined = set(hashes) - set(hash_readed)
    for news_data in news_with_hash:
        for unique_hashes in combined:
            o = news_data.get(unique_hashes)
            fresh_news.append(o)

    unique_news = []
    for freash_news in fresh_news:
        if freash_news != None:
            unique_news.append(freash_news)
    with open("/home/aaki/TRAPPIST-1E/logs.txt", 'a') as fw:
         combined = list(combined)
         for unique_hashes_in_combined in combined:
            fw.write(str(unique_hashes_in_combined) + '\n')


    return unique_news


def news_to_views():

    news_list = check_duplicate()
    if len(news_list) > 1:
        x = 1
        y = 0
        for item in news_list:
            for keys, values in item.items():
                if len(str(keys)) > 1 and len(str(values)) > 1:
                    title = str(values) + "  DATE: " + str(keys) + "."
                    date = str(keys)
                    image_path = search_image(title)
                    path = generate_video(image_path, title)
                    video_path = str(path)
                    print(f"[+] CONTENT GENERATED {x}")
                    print(f"[+] TITLE: {title}")
                    print(f"[+] DATE: {date}")
                    print(f"[+] VIDEO PATH {video_path}")


                    try:
                        if len(title) <= 100:
                            str(title)
                            upload_video(video_path=video_path, title=title, description=title)
                            #os.remove(video_path)
                            x += 1
                            tsleep(8640)


                        elif len(title) > 100:
                             hook_titles = [f"BREAKING NEWS {date} | FULL DETAILS IN DESCRIPTION", f"JUST IN {date} — CHECK DESCRIPTION FOR UPDATE", f"ALERT {date} | LATEST NEWS IN DESCRIPTION", f"DEVELOPING STORY {date} | DETAILS BELOW", f"CONFIRMED UPDATE {date} | READ DESCRIPTION", f"EXCLUSIVE NEWS {date} | FULL STORY IN DESCRIPTION", f"URGENT REPORT {date} | CHECK DESCRIPTION NOW", f"LIVE UPDATE {date} | MORE INFO IN DESCRIPTION", f"OFFICIAL NEWS {date} | DETAILS INSIDE DESCRIPTION", f"TRENDING NOW {date} | SEE DESCRIPTION", f"SHOCKING UPDATE {date} | FULL DETAILS BELOW", f"BREAKING ALERT {date} | DESCRIPTION HAS DETAILS", f"NEW REPORT {date} | CHECK DESCRIPTION", f"MUST SEE UPDATE {date} | READ DESCRIPTION", f"LATEST DEVELOPMENT {date} | DETAILS BELOW", f"IMPORTANT NEWS {date} | FULL INFO IN DESCRIPTION", f"BREAKING UPDATE {date} | SEE DESCRIPTION NOW", f"NEWS UPDATE {date} | DETAILS IN DESCRIPTION", f"CRITICAL UPDATE {date} | READ FULL STORY BELOW", f"JUST RELEASED {date} | CHECK DESCRIPTION"]
                             random_hook_title  = random.choice(hook_titles)
                             h_title = str(random_hook_title)
                             upload_video(video_path=video_path, title=h_title, description=title)
                             #os.remove(video_path)
                             x += 1
                             tsleep(8640)

                        else:
                            print("[+] YOUTUBE ERROR")
                            continue

                    except Exception as e:
                        print(e)
                        y += 1
                        
                else:
                   continue


    else:
        print("[+] NO NEWS")
        time.sleep(120)
        

try:
    news_to_views()

except Exception as e:
    print(e)
