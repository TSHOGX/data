import json
import os

json_data = []


CHARACTERS = [
    "萧逸",
    "陆沉",
    "齐司礼",
    "查理苏",
    "夏鸣星",
]


# parse txt files
for character in CHARACTERS:
    with open(f"./{character}.txt", "r") as file:
        lines = file.readlines()
    for line in lines[1:]:
        elements = line.split()
        if len(elements) < 5:
            elements.append("-")
        card_json = {
            "title": f"{character}-{elements[1]}",
            "character": character,
            "card name": elements[1],
            "stars": elements[0],
            "activity": elements[3],
            "type": elements[4],
            "description": f"{elements[2]}",
        }
        json_data.append(card_json)


# fix wrong name in cardstxt: 暮间诉愿 - 幕间诉愿
for card in json_data:
    if card["card name"] == "暮间诉愿":
        card["card name"] = "幕间诉愿"
        card["title"] = "夏鸣星-幕间诉愿"


# write to json file
with open(f"cardstxt.json", "w", encoding="utf-8") as file:
    json.dump(json_data, file, ensure_ascii=False, indent=4)
