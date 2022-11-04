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


def Crawling_Naver(la,lo):
    url_temp = 'https://map.naver.com/v5/api/search?caller=pcweb&query=%EC%9D%8C%EC%8B%9D%EC%A0%90&type=all&searchCoord={};{}&page={}&displayCount={}&isPlaceRecommendationReplace=true&lang=ko'
    latitude = la  # 현재 위도
    longitude = lo  # 현재 경도
    displayCount = 100  # 현재 위치로 부터 탐색할 가게 개수
    url = url_temp.format(longitude, latitude, 1, displayCount)
    response = urlopen(url)
    json_data = json.load(response)['result']['place']['list']
    result = []
    for place in json_data:
        result.append([place['id'], place['name'], place['category'], make_url(place['id'])])

    return result

def make_url(path):
    url = "https://pcmap.place.naver.com/restaurant/" + path + "/photo"
    return url

def scroll_down(driver):
    num_of_scroll = 5 # 숫자 커질수록 한 가게에서 뽑아오는 이미지 양 늘어남 (5 => 100장정도)
    for i in range(num_of_scroll):
        driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)

def save_img(driver,name):
    img_url = []
    imgs = driver.find_elements(By.CSS_SELECTOR, 'a.place_thumb>img')
    for image in imgs :
        url = image.get_attribute('src')
        img_url.append(url)

    img_folder = '../img/' + name
    if not os.path.isdir(img_folder) :
        os.mkdir(img_folder)
    else:
        return

    map_of_url_index = {}

    for index, link in enumerate(img_url) :
        urllib.request.urlretrieve(link, f'{img_folder}/{name}_{index}.jpg')
        img = Image.open(f'{img_folder}/{name}_{index}.jpg')
        img_resize = img.resize((256, 256))
        img_resize.save(f'{img_folder}/{name}_{index}.jpg')
        map_of_url_index[f'{index}'] = link

    with open(f'{img_folder}/{name}.txt','w',encoding='UTF-8') as f:
        for index,url in map_of_url_index.items():
            f.write(f'{index} : {url}\n')

def collect_data(path,name):
    driver = webdriver.Chrome('C:/Users/jaehoon/chromedriver')
    driver.get(make_url(path))
    scroll_down(driver)
    save_img(driver,name)

if __name__ == "__main__":

    position = [[37.530816, 127.066356],
                [37.540060, 127.070594],
                [37.546457, 127.073770],
                [37.555643, 127.078962],
                [37.564216, 127.083340],
                [37.569727, 127.083683],
                [37.560406, 127.086086],
                [37.557004, 127.084370],
                [37.555470, 127.091806],
                [37.549233, 127.090795],
                [37.543454, 127.085671],
                [37.538417, 127.084372],
                [37.535785, 127.077443],
                [37.531034, 127.080835],
                [37.534583, 127.090218],
                [37.542538, 127.094549],
                [37.553582, 127.108045],
                [37.548890, 127.105230],
                [37.542824, 127.101189],
                [37.542828, 127.092249]]

    for i in range(len(position)):
        print(i)
        start = time.time()  # 시작 시간 저장
        info = Crawling_Naver(position[i][0],position[i][1])
        for i in range(len(info)):
            collect_data(info[i][0],info[i][1])
        print("time :", time.time() - start)  # 현재시각 - 시작시간 = 실행 시간