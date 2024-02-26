import json
import os
import re


CHARACTERS = [
    "萧逸",
    "陆沉",
    "齐司礼",
    "查理苏",
    "夏鸣星",
]


# merge all weibo to one json
weibo_json = []
for filename in os.listdir("./"):
    if filename.startswith("7576045538"):
        with open(f"./{filename}", "r", encoding="utf-8") as file:
            weibo_json.extend(json.load(file)["weibo"])


# remove duplicates (same id) from weibo_json
new_weibo_json = []
for item in weibo_json:
    if item["id"] not in [i["id"] for i in new_weibo_json]:
        new_weibo_json.append(item)
weibo_json = new_weibo_json

# remove item if "壁纸" in text
weibo_json = [
    item
    for item in weibo_json
    if "壁纸" not in item["text"]
    or "匿名姐妹一颗不知名的柠檬糖提供截图" in item["text"]
]

# fix wrong name in weibo: 指尖心音 - 指间心音; 昼日疑魂 - 昼日凝魂; 瑰色迷梦 - 瑰色谜梦; 和风熙日 - 和风煦日; 一现昙华 - 一现昙花; 微醺十分 - 微醺时分
for item in weibo_json:
    if "指尖心音" in item["text"]:
        item["text"] = item["text"].replace("指尖心音", "指间心音")
    if "昼日疑魂" in item["text"]:
        item["text"] = item["text"].replace("昼日疑魂", "昼日凝魂")
    if "瑰色迷梦" in item["text"]:
        item["text"] = item["text"].replace("瑰色迷梦", "瑰色谜梦")
    if "和风熙日" in item["text"]:
        item["text"] = item["text"].replace("和风熙日", "和风煦日")
    if "一现昙华" in item["text"]:
        item["text"] = item["text"].replace("一现昙华", "一现昙花")
    if "微醺十分" in item["text"]:
        item["text"] = item["text"].replace("微醺十分", "微醺时分")


# remove pattern
remove_pattern = re.compile(r".*class=\"surl-text\">光与夜之恋</span></a><br />")
for item in weibo_json:
    if "text" in item:
        item["text"] = remove_pattern.sub("", item["text"])

# turn pics to list
for item in weibo_json:
    if "pics" in item:
        item["pics"] = item["pics"].split(",")

# split text with <br />
for item in weibo_json:
    if "text" in item:
        item["text"] = item["text"].split("<br />")


# save to file
with open(f"weibo.json", "w", encoding="utf-8") as file:
    json.dump(weibo_json, file, ensure_ascii=False, indent=4)
