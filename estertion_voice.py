import os
import urllib.request

import requests
from bs4 import BeautifulSoup


def main():
    # 首先取出 https://redive.estertion.win/sound/ 中所有分类的路径
    url = 'https://redive.estertion.win/sound/'
    category_response = requests.get(url)
    category_list_html = BeautifulSoup(category_response.text, features="html.parser")
    category_list = category_list_html.select('a')
    # 然后取出每个分类中音频集合的路径
    for category in category_list[1:]:
        # 如果是 unit_common/ 就走 else 分支，直接获取音频
        if category['href'] != 'unit_common/':
            category_response = requests.get(url + category['href'])
            category_list_html = BeautifulSoup(category_response.text, features="html.parser")
            category_list = category_list_html.select('a')
            # 最后取出每个音频集合中所有音频的路径
            for story in category_list[1:]:
                story_response = requests.get(url + category['href'] + story['href'])
                sound_list_html = BeautifulSoup(story_response.text, features="html.parser")
                sound_list = sound_list_html.select('a')
                # 拼接出每个音频的完整路径
                for sound in sound_list[1:]:
                    file_download_url = url + category['href'] + story['href'] + sound['href']
                    file_save_url = "./" + category['href'] + story['href'] + sound['href']
                    file_path = "./" + category['href'] + story['href']
                    if not os.path.exists(file_path):
                        os.makedirs(file_path)
                    try:
                        r = requests.get(file_download_url)
                        with open(file_save_url, mode='wb+') as outfile:
                            outfile.write(r.content)
                    except Exception as e:
                        print(file_download_url, e)
        # unit_common/ 就走这个分支，没有音频集合，直接就是音频，所以直接获得 unit_common 所有音频的路径
        else:
            story_response = requests.get(url + category['href'])
            sound_list_html = BeautifulSoup(story_response.text, features="html.parser")
            sound_list = sound_list_html.select('a')
            # 拼接出 unit_common 每个音频的完整路径
            for sound in sound_list[1:]:
                file_download_url = url + category['href'] + sound['href']
                file_save_url = "./" + category['href'] + sound['href']
                file_path = "./" + category['href']
                if not os.path.exists(file_path):
                    os.makedirs(file_path)
                try:
                    r = requests.get(file_download_url)
                    with open(file_save_url, mode='wb+') as outfile:
                        outfile.write(r.content)
                except Exception as e:
                    print(file_download_url, e)


main()
