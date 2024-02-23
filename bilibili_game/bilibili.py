from bs4 import BeautifulSoup
import json
import re


base_url = "https://www.bilibili.com"
file_path = "html_file"

# LoveAndDeepspace 2024-02-22 https://www.bilibili.com/video/BV1vV411X7nH/
# LightAndNight-01 2024-02-22 https://www.bilibili.com/video/BV1Tb4y1C7eS/
# LightAndNight-02 2024-02-22 https://www.bilibili.com/video/BV1dr4y1s79u/
# LightAndNight-03 2024-02-22 https://www.bilibili.com/video/BV1gv4y1V7vu/
# BeyondTheWorld 2024-02-22 https://www.bilibili.com/video/BV18K411e7sr/
json_file = "??.json"


# Read the HTML file
with open(file_path, "r", encoding="utf-8") as file:
    html_content = file.read()
soup = BeautifulSoup(html_content, "html.parser")
ul_element = soup.find("ul", class_="list-box")


# Extract tags from title
def tag_and_timestamp(title):
    character = "N/A"
    timestamp = "N/A"
    tags = "N/A"
    keywords = {
        # LightAndNight
        "萧逸": "萧逸",
        "陆沉": "陆沉",
        "齐司礼": "齐司礼",
        "查理苏": "查理苏",
        "夏鸣星": "夏鸣星",
        # LoveAndDeepspace
        "星星": "星星",
        "黎深": "黎深",
        "祁煜": "祁煜",
        "沈星回": "沈星回",
    }

    # Extract name of character if present
    for keyword, tag in keywords.items():
        if keyword in title:
            character = tag

    # Extract timestamp if present (formats "YYYY.MM" or "YYYY.M")
    match = re.search(r"\d{4}\.\d{1,2}", title)
    if match:
        timestamp = match.group()

    # Extract default tag from title
    default_tag_match = re.search(r"【(.*?)】", title)
    if default_tag_match:
        default_tag = default_tag_match.group(1)
        if timestamp in default_tag:
            default_tag = default_tag.replace(timestamp, "").strip()
        tags = default_tag
    else:
        print(f"No default tag found in {title}")

    return tags, timestamp, character


def main():
    data = []

    if ul_element:
        li_elements = ul_element.find_all("li")

        for li in li_elements:
            a_tag = li.find("a")
            item = {}
            if a_tag and "href" in a_tag.attrs and "title" in a_tag.attrs:
                item["href"] = base_url + a_tag["href"]
                item["title"] = a_tag["title"]
                tags, timestamp, character = tag_and_timestamp(item["title"])
                item["tag"] = tags
                item["character"] = character
                item["timestamp"] = timestamp
                data.append(item)

    with open(json_file, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False)

    print(f"Data extracted and stored in {json_file}")


main()
