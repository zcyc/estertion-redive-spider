import os

import requests
from bs4 import BeautifulSoup

sound_url = 'https://redive.estertion.win/sound/'

movie_url = "https://redive.estertion.win/movie/"


def down_sound():
    # 首先取出 sound_url 中所有分类的路径
    category_response = requests.get(sound_url)
    category_list_html = BeautifulSoup(category_response.text, features="html.parser")
    category_list = category_list_html.select('a')
    # 然后取出每个分类中音频集合的路径
    for category in category_list[1:]:
        # 如果是 unit_common/ 就走 else 分支，直接获取音频
        if category['href'] != 'unit_common/':
            category_response = requests.get(sound_url + category['href'])
            category_list_html = BeautifulSoup(category_response.text, features="html.parser")
            category_list = category_list_html.select('a')
            # 最后取出每个音频集合中所有音频的路径
            for story in category_list[1:]:
                story_response = requests.get(sound_url + category['href'] + story['href'])
                sound_list_html = BeautifulSoup(story_response.text, features="html.parser")
                sound_list = sound_list_html.select('a')
                # 拼接出每个音频的完整路径
                for sound in sound_list[1:]:
                    file_download_url = sound_url + category['href'] + story['href'] + sound['href']
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
            story_response = requests.get(sound_url + category['href'])
            sound_list_html = BeautifulSoup(story_response.text, features="html.parser")
            sound_list = sound_list_html.select('a')
            # 拼接出 unit_common 每个音频的完整路径
            for sound in sound_list[1:]:
                file_download_url = sound_url + category['href'] + sound['href']
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


def down_movie():
    # 首先取出 movie_url 中所有视频的路径
    movie_response = requests.get(movie_url)
    movie_list_html = BeautifulSoup(movie_response.text, features="html.parser")
    movie_list = movie_list_html.select('a')
    # 拼接每个视频的完整链接
    for movie in movie_list[1:]:
        file_download_url = movie_url + movie['href']
        file_save_url = "./movie/" + movie['href']
        file_path = "./movie/" + movie['href'].split("/")[0]
        if not os.path.exists(file_path):
            os.makedirs(file_path)
        try:
            r = requests.get(file_download_url)
            with open(file_save_url, mode='wb+') as outfile:
                outfile.write(r.content)
        except Exception as e:
            print(file_download_url, e)


# 下载音乐
down_sound()
# 下载视频
down_movie()
