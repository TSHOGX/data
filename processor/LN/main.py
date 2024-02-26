import json
import os


CHARACTERS = [
    "萧逸",
    "陆沉",
    "齐司礼",
    "查理苏",
    "夏鸣星",
]


with open(f"./data/weibo/weibo.json", "r", encoding="utf-8") as file:
    weibo_json = json.load(file)

with open(f"./data/cardstxt/cardstxt.json", "r", encoding="utf-8") as file:
    card_json = json.load(file)

with open(f"./data/bilibili/bilibili.json", "r", encoding="utf-8") as file:
    bilibili_json = json.load(file)


# match bilibili_video and card
for card in card_json:
    card["bilibili_video"] = []
    for video in bilibili_json:
        if card["card_name"] in video["title"]:
            card["bilibili_video"].append(video["href"])
    if (
        len(card["bilibili_video"]) == 0
        and card["stars"] in ["5", "6"]
        and card["type"] not in ["邂逅"]
    ):
        # fix wrong name in bilibili: 囚镜 - 囚境; 炽热烟尘 - 炽热尘烟; 时光玫瑰 - 时与玫瑰; 昼日疑魂 - 昼日凝魂; 指尖心音 - 指间心音
        # fix wrong name in cardstxt: 暮间诉愿 - 幕间诉愿
        print(card["card_name"], card["bilibili_video"])
# with open(f"./card_and_video.json", "r", encoding="utf-8") as file:
#     card_json = json.load(file)


# match weibo with card
for card in card_json:
    card_name = card["card_name"]
    card["weibo"] = []
    for weibo in weibo_json:
        for text in weibo["text"]:
            if card_name in text:
                card["weibo"].append(weibo["id"])
    # pick one match
    if len(card["weibo"]) >= 2 and card["stars"] in ["5", "6"]:
        for weiboid in card["weibo"]:
            weibo_texts = [item["text"] for item in weibo_json if item["id"] == weiboid]
            for text in weibo_texts[0]:
                if (
                    "卡面高清截修" in text
                    or "卡面截修" in text
                    or ("高清截修" in text and "pv" not in text)
                    or "高清修复" in text
                    or "游戏内卡面修复" in text
                    or "活动卡面修复" in text
                    or "4652052145245340" == str(weiboid)
                    or "4676487820607975" == str(weiboid)
                ):
                    card["weibo"] = [weiboid]
                    break
    if len(card["weibo"]) != 1 and 4624605711697957 in card["weibo"]:
        card["weibo"].remove(4624605711697957)
    # make sure all 5 or 6 stars card has one weibo
    if len(card["weibo"]) != 1 and card["stars"] in ["5", "6"]:
        print(card["card_name"], card["weibo"])
    # for other stars card, make sure all weibo has no more than one card (can be missing)
    if len(card["weibo"]) >= 2:
        for weiboid in card["weibo"]:
            weibo_texts = [item["text"] for item in weibo_json if item["id"] == weiboid]
            for text in weibo_texts[0]:
                if (
                    "高清截修" in text
                    or "【常驻卡面｜" in text
                    or "游戏内卡面修复" in text
                    or "活动卡面修复" in text
                ):
                    card["weibo"] = [weiboid]
                    break
    if len(card["weibo"]) >= 2:
        print(card["card_name"], card["weibo"])

# add matched weibo to weibo set
weibo_set = []
weiboid_set = []
for card in card_json:
    for weiboid in card["weibo"]:
        if weiboid not in weiboid_set:
            weibo = [item for item in weibo_json if item["id"] == weiboid]
            weibo_set.append(weibo[0])
            weiboid_set.append(weiboid)
weibo_json = weibo_set


# remove problematic weibo_imgs
for item in weibo_json:
    if item["id"] in [4867860037895975, 4864857613275374, 4809555885688941]:
        item["pics"] = item["pics"][:-1]
    if item["id"] in [
        4824770937619128,
        4730604229233807,
        4757160087521830,
        4839009992574751,
    ]:
        weibo_json.remove(item)
    if item["id"] in [4912621062981422]:
        item["pics"] = item["pics"][:5] + item["pics"][6:-1]
    if item["id"] in [4624182967801389]:
        for text in item["text"]:
            if "一段" in text:
                item["text"].remove(text)
        item["pics"] = [item["pics"][0]] + [item["pics"][2]] + item["pics"][4:12]
    if item["id"] in [4624605711697957]:
        new_text = []
        for text in item["text"]:
            if "萧逸" in text and "一段" not in text:
                if "不驯" in text:
                    text = text.replace("不驯", "不训")
                new_text.append(text)
        item["text"] = new_text
        item["pics"] = [item["pics"][1]] + [item["pics"][5]] + item["pics"][9:12]
    if item["id"] in [4853488766432058]:
        count = 1
        new_pics = []
        for pic in item["pics"]:
            if count % 3 != 0:
                new_pics.append(pic)
            count += 1
        item["pics"] = new_pics


# add item["matched"]
for item in weibo_json:
    item["matched"] = []
    for text in item["text"]:
        for card in card_json:
            card_name = card["card_name"]
            matched_name = f"{card_name}-{card['stars']}"
            if card_name in text and matched_name not in item["matched"]:
                item["matched"].append(matched_name)
    # remove problematic matched
    if "瑰焰燎原-6" in item["matched"]:
        item["matched"].remove("燎原-6")
    if "迷途启示-3" in item["matched"] or "迷途誓约-5" in item["matched"]:
        item["matched"].remove("迷途-4")
    if "长日酣梦-2" in item["matched"]:
        item["matched"].remove("酣梦-6")
    if item["id"] in [4875917077778144]:
        item["matched"] = ["莫逆与共-6"]
    if item["id"] in [4876712493712935]:
        item["matched"] = ["一触即发-3"]

# test matched number with pics
for item in weibo_json:
    matched_number = 0
    for matched in item["matched"]:
        if "5" in matched or "6" in matched:
            matched_number += 2
        else:
            matched_number += 1
    if len(item["pics"]) != matched_number:
        print(item["matched"], matched_number, len(item["pics"]))
        print(item["id"])


# make a new json file with card_name: pics
matched_cards = []  # [{card_name:"", pics:[]}]
for item in weibo_json:
    temp = {}
    count = 0
    for matched in item["matched"]:
        card_name, star = matched.split("-")
        temp[card_name] = []
        if star in ["5", "6"]:
            temp[card_name].append(item["pics"][count])
            temp[card_name].append(item["pics"][count + 1])
            count += 2
        else:
            temp[card_name].append(item["pics"][count])
            count += 1
    for key, value in temp.items():
        if key not in [item["card_name"] for item in matched_cards]:
            matched_cards.append({"card_name": key, "pics": value})
# # write to json file
# with open(f"weibo_card.json", "w", encoding="utf-8") as file:
#     json.dump(matched_cards, file, ensure_ascii=False, indent=4)


# add to card json
for card in card_json:
    card["weibo_imgs"] = []
    for matched in matched_cards:
        if card["card_name"] == matched["card_name"]:
            card["weibo_imgs"] = matched["pics"]


# final fix missing weibo_imgs
missing_weibo = [
    {
        "card_name": "不训",
        "weibo_imgs": [
            "https://wx4.sinaimg.cn/large/008gIjwSgy1gpf5mril05j31901wc7wi.jpg"
        ],
        "weibo": [4624605711697957],
    },
    {
        "card_name": "黑色沉沦",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx27pad7ij31o02jhx6p.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "尘埃银河",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx27pad7ij31o02jhx6p.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "与你同坠",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx27dzsglj31o02jdu0y.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "迷迭暗巷",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx275mo32j61o02jf1ky02.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "暗巷沉沉",
        "weibo_imgs": [
            "https://wx4.sinaimg.cn/large/008gIjwSgy1grx26scmnoj31o02jd1ky.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "急流",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx272503nj31o02jfkjm.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "即刻启程",
        "weibo_imgs": [
            "https://wx4.sinaimg.cn/large/008gIjwSgy1grx284l39mj31o02jde82.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "奇妙伙伴",
        "weibo_imgs": [
            "https://wx4.sinaimg.cn/large/008gIjwSgy1grx278jiakj31o02jbb2a.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "专属方向",
        "weibo_imgs": [
            "https://wx4.sinaimg.cn/large/008gIjwSgy1grx27t0wpij31o02ja1kz.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "火之洗礼",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1grx287qtmjj31o02jgkjm.jpg"
        ],
        "weibo": [4652786367858167],
    },
    {
        "card_name": "燎原",
        "weibo_imgs": [
            "https://wx1.sinaimg.cn/large/008gIjwSgy1hhq4ms9w10j33m8554u1d.jpg",
            "https://wx2.sinaimg.cn/large/008gIjwSgy1hhq4n4alh6j35eg30m4r7.jpg",
        ],
        "weibo": [4944008478982911],
    },
]

for card in card_json:
    if card["weibo_imgs"] == [] or card["weibo"] == []:
        for missing in missing_weibo:
            if card["card_name"] == missing["card_name"]:
                card["weibo_imgs"] = missing["weibo_imgs"]
                card["weibo"] = missing["weibo"]
    if len(card["weibo"]) != 1:
        print(card["card_name"], card["weibo"])
    card["weibo"] = str(card["weibo"][0])


# search ealest created_at time in 6880285576.json with card_name in text
with open(f"./data/weibo/6880285576.json", "r", encoding="utf-8") as file:
    weibo_688 = json.load(file)["weibo"]
for card in card_json:
    card["created_at"] = "2025-01-01 00:00:00"
    for weibo in weibo_688:
        if card["card_name"] in weibo["text"]:
            if weibo["created_at"] < card["created_at"]:
                card["created_at"] = weibo["created_at"]
    if card["created_at"] == "2025-01-01 00:00:00":
        card["created_at"] = "2020-01-01 00:00:00"

# sort card_json by created_at, inverse order
card_json = sorted(card_json, key=lambda x: x["created_at"], reverse=True)

# assign unique id to each card
for i, card in enumerate(card_json):
    card["id"] = str(i + 1)


# write to json file
with open(f"LN.json", "w", encoding="utf-8") as file:
    json.dump(card_json, file, ensure_ascii=False, indent=4)


# # write to json file
# for item in weibo_json:
#     item.pop("user_id")
#     item.pop("screen_name")
#     item.pop("article_url")
#     item.pop("source")
#     item.pop("attitudes_count")
#     item.pop("comments_count")
#     item.pop("reposts_count")
#     item.pop("topics")
#     item.pop("at_users")
#     item.pop("location")
#     item.pop("video_url")
#     item.pop("full_created_at")
# with open(f"weibo_list.json", "w", encoding="utf-8") as file:
#     json.dump(weibo_json, file, ensure_ascii=False, indent=4)
