import json
import os
import shutil
import re

file_path = "./weibo.json"

BILIBILI_JSON_PREFIX = "../bilibili/data/"


GAMENAME = "蓝咕咕图像站"

out_path = f"{GAMENAME}.json"
new_media_dir = f"./media/{GAMENAME}/"
image_dir = f"../weibo/weibo/{GAMENAME}/img/原创微博图片/"
video_dir = f"../weibo/weibo/{GAMENAME}/video/原创微博视频/"


with open("weibo.json", "r", encoding="utf-8") as file:
    data = json.load(file)


def clean_title(title):
    # Remove '·卡面高清截修' and emojis
    title = title.replace("·卡面高清截修", "").strip()
    title = re.sub(r"[^\w\s·]", "", title)
    return title


def get_character_name(title):
    names = ["夏鸣星", "齐司礼", "陆沉", "查理苏", "萧逸"]
    for name in names:
        if name in title:
            return name
    return None


def copy_rename_images(item_id, character_name, card_name, flag):
    count = 1
    new_filename_list = []

    for dir_path in [image_dir, video_dir]:
        for filename in os.listdir(dir_path):
            if str(item_id) in filename:
                if flag == 2:
                    file_extension = os.path.splitext(filename)[1]
                    new_filename = (
                        f"{character_name}·{card_name[0]}_{count}{file_extension}"
                    )
                    new_path = os.path.join(new_media_dir, new_filename)

                    shutil.copy(os.path.join(dir_path, filename), new_path)

                    count += 1
                    new_filename_list.append(new_filename)

                elif flag == 3:
                    file_extension = os.path.splitext(filename)[1]
                    if count == 1:
                        new_filename = (
                            f"{character_name}·{card_name[0]}{file_extension}"
                        )
                    else:
                        new_filename = (
                            f"{character_name}·{card_name[1]}_{count-1}{file_extension}"
                        )
                    new_path = os.path.join(new_media_dir, new_filename)

                    shutil.copy(os.path.join(dir_path, filename), new_path)

                    count += 1
                    new_filename_list.append(new_filename)

                if count == flag + 1:
                    return new_filename_list

    return new_filename_list


def copy_rename_images_all(item_id, card_name, flag):
    new_filename_list = []
    name_count = 0
    count = 1

    if flag == 1:
        for dir_path in [image_dir, video_dir]:
            for filename in os.listdir(dir_path):
                if str(item_id) in filename:
                    card = card_name[name_count]
                    file_extension = os.path.splitext(filename)[1]
                    new_filename = f"{card}{file_extension}"
                    new_path = os.path.join(new_media_dir, new_filename)

                    shutil.copy(os.path.join(dir_path, filename), new_path)

                    new_filename_list.append(new_filename)

                    name_count += 1
                    if name_count == len(card_name):
                        return new_filename_list
    elif flag == 2:
        for dir_path in [image_dir, video_dir]:
            for filename in os.listdir(dir_path):
                if str(item_id) in filename:
                    card = card_name[name_count]
                    file_extension = os.path.splitext(filename)[1]
                    new_filename = f"{card}_{count}{file_extension}"
                    new_path = os.path.join(new_media_dir, new_filename)

                    shutil.copy(os.path.join(dir_path, filename), new_path)

                    count += 1
                    new_filename_list.append(new_filename)

                    if count == 3:
                        name_count += 1
                        count = 1
                    if name_count == len(card_name):
                        return new_filename_list
    else:
        for dir_path in [image_dir, video_dir]:
            for filename in os.listdir(dir_path):
                if str(item_id) in filename:
                    card = card_name[name_count]
                    file_extension = os.path.splitext(filename)[1]
                    new_filename = f"{card}_{count}{file_extension}"
                    new_path = os.path.join(new_media_dir, new_filename)

                    shutil.copy(os.path.join(dir_path, filename), new_path)

                    count += 1
                    new_filename_list.append(new_filename)

                    # 2 * 4 + 2
                    if count == 3:
                        name_count += 1
                        if name_count >= 4:
                            count = 2
                        else:
                            count = 1
                    if name_count == len(card_name):
                        return new_filename_list

    return new_filename_list


# Process each entry
for entry in data:
    entry["title"] = clean_title(entry["title"])
    character_name = get_character_name(entry["title"])
    entry["character_name"] = (
        character_name if character_name else "Multiple Characters"
    )

    # Process text and images
    if character_name:
        card_names = re.findall(r"·(.*?)<br />", entry["text"])
        if len(card_names) == 0:
            card_names = [entry["title"].split("·")[-1]]

        if entry["id"] in [
            4931811354872716,
            4931807411706596,
            4931806073981669,
            4924842044037280,
        ]:
            # not neccessary to print (浮梦夏日长切片, 查理苏生日 pv)
            pass
        elif entry["id"] in [4876712493712935]:
            # seems failed to download original images
            pass
        elif entry["id"] in [4864857613275374]:
            entry["media"] = copy_rename_images(
                entry["id"], character_name, card_names, 2
            )
        elif entry["id"] in [4837831224330920]:
            entry["media"] = copy_rename_images(entry["id"], "陆沉", "此信承期", 2)
        elif (
            len(card_names) == 1
            and len(entry["pics_weibo"]) == 2
            or len(entry["pics_weibo"]) == 1
        ):
            #  one card, two images (one image for 4795440731525506)
            entry["media"] = copy_rename_images(
                entry["id"], character_name, card_names, 2
            )
        elif len(card_names) == 2 and len(entry["pics_weibo"]) == 3:
            #  two card, three images
            entry["media"] = copy_rename_images(
                entry["id"], character_name, card_names, 3
            )
        else:
            print(
                f"no match for {entry['id']}, card_names: {card_names}, pics_weibo: {len(entry['pics_weibo'])}"
            )

    else:
        card_names = entry["text"].split("<br />")
        if entry["id"] in [4820367930032689, 4788908741365286]:
            # 2 * 4 + 2
            entry["media"] = copy_rename_images_all(entry["id"], card_names, 3)
        elif entry["id"] in [4912621062981422]:
            # 寂静撞击
            pass
        elif (
            entry["id"] in [4757000946974894]
            or len(entry["pics_weibo"]) == 5
            or len(entry["pics_weibo"]) == 2
        ):
            # one name, one image
            if entry["id"] == 4759223349806541:
                card_names = ["查理苏·澄澈遐想·夜幕缭绕"]
            elif entry["id"] == 4761017853152081:
                card_names = ["陆沉·永恒盛会·奇诞破晓"]
            entry["media"] = copy_rename_images_all(entry["id"], card_names, 1)
        else:
            # one name, two images
            entry["media"] = copy_rename_images_all(entry["id"], card_names, 2)

    # Drop unnecessary fields
    entry.pop("video_weibo", None)
    entry.pop("card_name", None)
    entry.pop("text", None)


# Save modified data
with open("蓝咕咕图像站.json", "w", encoding="utf-8") as file:
    json.dump(data, file, ensure_ascii=False, indent=4)


print("Processing complete!")
