from urllib.request import urlopen
import urllib.request
import urllib
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import json
from urllib.request import urlopen
from PIL import Image


def Crawling_Naver(latitude, longitude):
    url_temp = 'https://map.naver.com/v5/api/search?caller=pcweb&query=%EC%9D%8C%EC%8B%9D%EC%A0%90&type=all&searchCoord={};{}&page={}&displayCount={}&isPlaceRecommendationReplace=true&lang=ko'
    displayCount = 100  # 탐색할 가게 개수
    url = url_temp.format(latitude, longitude, 1, displayCount)
    response = urlopen(url)
    json_data = json.load(response)['result']['place']['list']
    result = []
    for place in json_data:
        result.append([place['id'], place['name'], place['category'], make_url(place['id'])])

    return result


def make_url(id):
    url = "https://pcmap.place.naver.com/restaurant/" + id + "/photo"
    return url


def scroll_down(driver):
    num_of_scroll = 7  # 스크롤 횟수 (커질수록 가져오는 이미지 양 많아짐)
    for i in range(num_of_scroll):
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)


def load_and_save_img(driver, name):
    img_info = dict()
    imgs = driver.find_elements(By.CSS_SELECTOR, 'a.place_thumb>img')
    img_url = []
    for image in imgs:
        url = image.get_attribute('src')
        img_url.append(url)

    img_folder = '../img/' + name
    if not os.path.isdir(img_folder):  # 없으면 새로 생성하는 조건문
        os.mkdir(img_folder)

    for index, link in enumerate(img_url):
        img_info[index] = link
        urllib.request.urlretrieve(link, f'{img_folder}/{name}_{index}.jpg')
        img = Image.open(f'{img_folder}/{name}_{index}.jpg')
        img_resize = img.resize((256, 256))
        img_resize.save(f'{img_folder}/{name}_{index}.jpg')

    f = open(img_folder + '/' + name + '.txt', 'w')
    for key, val in img_info.items():
        line = name+'_'+str(key) + ' : ' + val + '\n'
        f.write(line)

    return len(img_info)


if __name__ == "__main__":
    latitude = 126.93632421051524  # 현재 위도
    longitude = 37.55433832843096  # 현재 경도
    info = Crawling_Naver(latitude, longitude)
    for idx, place_info in enumerate(info):
        print(place_info[1], place_info[2],'-->', end=' ')
        place_id, name, cate, url = place_info
        driver = webdriver.Chrome('C:/Users/bob8d/OneDrive/Desktop/chromedriver_win32/chromedriver.exe')  # 사용자에 맞게 chrome driver 설치 후 위치 지정해줘야함
        driver.get(url)
        scroll_down(driver)
        img_cnt = load_and_save_img(driver, name)
        print('%s개 저장완료!' % img_cnt)
