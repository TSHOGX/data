import json
import os
import sys
import time

import requests
from requests.adapters import HTTPAdapter


with open(f"LN.json", "r", encoding="utf-8") as file:
    card_json = json.load(file)


def download_one_file(url, file_path, weibo_id):
    """下载单个文件(图片/视频)"""

    cookie = "SUB=_2A25I04K-DeThGeBK41oV8ynIzziIHXVrkJp2rDV6PUJbktANLUTXkW1NR20WYX8KPe42b7HMjw9MitX45jqcAT4i; SUBP=0033WrSXqPxfM725Ws9jqgMF55529P9D9WFQerzbsIEm3YpV3LzrnSIb5JpX5KzhUgL.FoqX1hnXe0MXShB2dJLoI0qLxKnLBoMLB-qLxKBLBonL12BLxK-L12qLB-qLxKBLB.zLBK-LxKnL1hMLB-2LxKBLB.qLB--t; SSOLoginState=1708651246; ALF=1711243246; _T_WM=f3ced68a88cadc3581b28635fdd7eee3; WEIBOCN_FROM=1110006030; MLOGIN=1; M_WEIBOCN_PARAMS=fid%3D10080864eeb90c049c2e6f19f614bf63b6fe8e_-_feed%26uicode%3D10000011"
    user_agent = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36"
    self_headers = {"User_Agent": user_agent, "Cookie": cookie}

    try:

        file_exist = os.path.isfile(file_path)
        need_download = not file_exist

        if not need_download:
            print("[MESSAGE] already downloaded " + file_path)
            return

        s = requests.Session()
        s.mount(url, HTTPAdapter(max_retries=5))
        try_count = 0
        success = False
        MAX_TRY_COUNT = 3
        while try_count < MAX_TRY_COUNT:
            downloaded = s.get(url, headers=self_headers, timeout=(5, 10), verify=False)
            try_count += 1
            fail_flg_1 = url.endswith(
                ("jpg", "jpeg")
            ) and not downloaded.content.endswith(b"\xff\xd9")
            fail_flg_2 = url.endswith("png") and not downloaded.content.endswith(
                b"\xaeB`\x82"
            )

            if fail_flg_1 or fail_flg_2:
                print("[DEBUG] failed " + url + "  " + str(try_count))
            else:
                success = True
                print("[DEBUG] success " + url + "  " + str(try_count))
                break

        if success:
            # 需要分别判断是否需要下载
            if not file_exist:
                with open(file_path, "wb") as f:
                    f.write(downloaded.content)
                    print("[DEBUG] save " + file_path)
            # if (not sqlite_exist) and ("sqlite" in self.write_mode):
            #     self.insert_file_sqlite(file_path, weibo_id, url, downloaded.content)
        else:
            print("[DEBUG] failed " + url + " TOTALLY")
    except Exception as e:
        # error_file = self.get_filepath(type) + os.sep + "not_downloaded.txt"
        error_file = "not_downloaded.txt"
        with open(error_file, "ab") as f:
            url = str(weibo_id) + ":" + file_path + ":" + url + "\n"
            f.write(url.encode(sys.stdout.encoding))
        print(e)


# download file
if not os.path.isdir("./media"):
    os.makedirs("./media")

count = 0
for card in card_json:
    if count % 50 == 0:
        # sleep for 10 seconds
        time.sleep(10)
    weibo_id = card["weibo"]
    title = card["title"]
    card["local pics"] = []
    if len(card["weibo pics"]) == 1:
        file_path = f"./media/{title}.{pic_url.split('.')[-1]}"
        download_one_file(pic_url, file_path, weibo_id)
        card["local pics"].append(f"{title}.{pic_url.split('.')[-1]}")
    else:
        for index, pic_url in enumerate(card["weibo pics"]):
            file_path = f"./media/{title}-{index}.{pic_url.split('.')[-1]}"
            download_one_file(pic_url, file_path, weibo_id)
            card["local pics"].append(f"{title}-{index}.{pic_url.split('.')[-1]}")
    count += 1


# save to file
with open(f"LNlocal.json", "w", encoding="utf-8") as file:
    json.dump(card_json, file, ensure_ascii=False, indent=4)
