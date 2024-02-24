import json
import re
import os
import shutil


BILIBILI_JSON_PREFIX = "../bilibili/data/"

GAMENAME = "光与夜之恋"
file_path = "6880285576.json"
out_path = "LightAndNight.json"
new_media_dir = "./media/LightAndNight/"
image_dir = "../weibo/weibo/光与夜之恋/img/原创微博图片/"
video_dir = "../weibo/weibo/光与夜之恋/video/原创微博视频/"

# GAMENAME = "恋与深空"
# file_path = "7484247626.json"
# out_path = "LoveAndDeepspace.json"
# new_media_dir = "./media/LoveAndDeepspace/"
# image_dir = "../weibo/weibo/恋与深空/img/原创微博图片/"
# video_dir = "../weibo/weibo/恋与深空/video/原创微博视频/"




def find_matching_items(json_data, game_name):
    matching_items = []

    if game_name == "光与夜之恋":
        pattern = re.compile(r"✦(.+?)・(.+?)✦")
        remove_pattern = re.compile(r".*class=\"surl-text\">光与夜之恋</span></a>")

        for item in json_data:
            if 'text' in item:
                matches = pattern.findall(item['text'])
                if len(matches) == 1:
                    character_name, card_name = matches[0]
                    if not "<br />" in card_name:
                        cleaned_text = remove_pattern.sub('', item['text'])
                        matching_items.append({
                            "title": f"{character_name}・{card_name}",
                            "character_name": character_name,
                            "card_name": card_name,
                            "id": item["id"],
                            "text": cleaned_text,
                            "created_at": item["created_at"],
                        })

    elif game_name == "恋与深空":
        pattern = re.compile(r"思念「(.+?)·(.+?)」")
        remove_pattern = re.compile(r".*class=\"surl-text\">恋与深空</span></a>")
    
        for item in json_data:
            if 'text' in item:
                matches = pattern.findall(item['text'])
                # if all matches are same
                if len(matches) > 0 and all(x == matches[0] for x in matches):
                    character_name, card_name = matches[0]
                    if not "<br />" in card_name and not "<br />" in character_name:
                        cleaned_text = remove_pattern.sub('', item['text'])
                        matching_items.append({
                            "title": f"{character_name}・{card_name}",
                            "character_name": character_name,
                            "card_name": card_name,
                            "id": item["id"],
                            "text": cleaned_text,
                            "created_at": item["created_at"],
                        })

    return matching_items


# Read raw data
with open(file_path, "r", encoding="utf-8") as file:
    json_string = file.read()
json_data = json.loads(json_string)


# Process data
matching_items = find_matching_items(json_data["weibo"], game_name=GAMENAME)


# Get media
for entry in matching_items:
    item_id = str(entry['id'])
    count = 1

    for dir_path in [image_dir, video_dir]:
        for filename in os.listdir(dir_path):
            if item_id in filename:
                file_extension = os.path.splitext(filename)[1]
                new_filename = f"{item_id}_{count}{file_extension}"
                new_path = os.path.join(new_media_dir, new_filename)

                # Copy and rename the file
                shutil.copy(os.path.join(dir_path, filename), new_path)
                count += 1
    
    # add new media path to entry
    entry["media"] = []
    for i in range(1, count):
        entry["media"].append(f"{item_id}_{i}{file_extension}")

print("Media copied!")


# Match bilibili video
bilibili_data = []
if GAMENAME == "光与夜之恋":
    with open(BILIBILI_JSON_PREFIX + "LightAndNight-01.json", "r", encoding="utf-8") as file:
        bilibili_data = json.load(file)
    with open(BILIBILI_JSON_PREFIX + "LightAndNight-02.json", "r", encoding="utf-8") as file:
        bilibili_data += json.load(file)
    with open(BILIBILI_JSON_PREFIX + "LightAndNight-03.json", "r", encoding="utf-8") as file:
        bilibili_data += json.load(file)
elif GAMENAME == "恋与深空":
    with open(BILIBILI_JSON_PREFIX + "LoveAndDeepspace.json", "r", encoding="utf-8") as file:
        bilibili_data = json.load(file)


for entry in matching_items:
    for video in bilibili_data:
        if entry["card_name"] in video["title"]:
            entry["video"] = video["href"]

print("Bilibili video matched!")



# Write to file
with open(out_path, "w", encoding="utf-8") as file:
    json.dump(matching_items, file, ensure_ascii=False)

print("Done!")
