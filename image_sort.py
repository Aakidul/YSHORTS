import os

path = "/home/aaki/TRAPPIST-1E/image_generator/images"
os.chdir(path)

files = os.listdir()

def get_newest_img_stamp():
    index_list = []
    for images in files:
        images_stamp = images.split(".")
        # extract the integer timestamp from filename
        index = int(images_stamp[0])
        index_list.append(index)

    sorted_index = sorted(index_list, reverse=True)
    return sorted_index


def get_img_path_new():
    data = get_newest_img_stamp()
    if not data:
        print("[ERROR] No images found in directory.")
        return None  # or raise FileNotFoundError

    new_img = str(data[0]) + '.jpg'
    old_img = str(data[-1]) + '.jpg'
    c_path = os.getcwd()
    full_path = os.path.join(c_path, new_img)
    return full_path
