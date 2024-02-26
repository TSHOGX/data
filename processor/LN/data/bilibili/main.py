import json
import os


LightAndNight = []

# merge all LightAndNight from bilibili processed json to one json
for filename in os.listdir("./"):
    if filename.startswith("LightAndNight"):
        with open(f"./{filename}", "r", encoding="utf-8") as file:
            LightAndNight.extend(json.load(file))


# fix wrong name in bilibili: 囚镜 - 囚境; 炽热烟尘 - 炽热尘烟; 时光玫瑰 - 时与玫瑰; 昼日疑魂 - 昼日凝魂; 指尖心音 - 指间心音
for item in LightAndNight:
    if "囚镜" in item["title"]:
        item["title"] = item["title"].replace("囚镜", "囚境")
    if "炽热烟尘" in item["title"]:
        item["title"] = item["title"].replace("炽热烟尘", "炽热尘烟")
    if "时光玫瑰" in item["title"]:
        item["title"] = item["title"].replace("时光玫瑰", "时与玫瑰")
    if "昼日疑魂" in item["title"]:
        item["title"] = item["title"].replace("昼日疑魂", "昼日凝魂")
    if "指尖心音" in item["title"]:
        item["title"] = item["title"].replace("指尖心音", "指间心音")


# save to file
with open(f"bilibili.json", "w", encoding="utf-8") as file:
    json.dump(LightAndNight, file, ensure_ascii=False, indent=4)
