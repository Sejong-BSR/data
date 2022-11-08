from collections import deque
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
    num_of_scroll = 5  # 스크롤 횟수 (커질수록 가져오는 이미지 양 많아짐)
    for i in range(num_of_scroll):
        driver.find_element(By.CSS_SELECTOR, 'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(0.5)


def load_and_save_img(driver, name, cate):

    img_info = dict()
    imgs = driver.find_elements(By.CSS_SELECTOR, 'a.place_thumb>img')
    img_url = []
    for image in imgs:
        url = image.get_attribute('src')
        img_url.append(url)



    for index, link in enumerate(img_url):
        img_info[index] = link
        urllib.request.urlretrieve(link, f'{img_folder}/{name}_{index}.jpg')
        img = Image.open(f'{img_folder}/{name}_{index}.jpg')
        img_resize = img.resize((256, 256))
        img_resize.save(f'{img_folder}/{name}_{index}.jpg')

    f = open(img_folder + '/' + name + '.txt', 'w')

    f.write(name + ' | ' + '/'.join(list(cate)[1:]) +'\n')
    for key, val in img_info.items():
        line = name+'_'+str(key) + ' : ' + val + '\n'
        f.write(line)

    print("-> %d개 저장완료!" %len(img_info))


if __name__ == "__main__":
    chrome_driver_dir = 'C:/Users/bob8d/OneDrive/Desktop/chromedriver_win32/chromedriver.exe'
    options = webdriver.ChromeOptions() # 옵션 생성
    options.add_argument("headless") # 창 숨기는 옵션 추가

    ### 직접 위도, 경도 설정 필요
    latitude = 126.93632421051524  # 현재 위도
    longitude = 37.55433832843096  # 현재 경도

    info = Crawling_Naver(latitude, longitude)
    for idx, place_info in enumerate(info):
        place_id, name, cate, url = place_info
        # make category
        cate = deque(cate)
        if cate[0] != '음식점':
            cate.appendleft('음식점')
        else:
            cate.append('기타')
        print(name, list(cate), end=' ')

        # make image folder
        img_folder = '..'
        make_dir = ['img'] + list(cate)
        for c in make_dir:
            img_folder += '/' + c
            if not os.path.isdir(img_folder):
                os.mkdir(img_folder)
        store_name = img_folder + '/' + name
        if not os.path.isdir(store_name):
            os.mkdir(store_name)
        else:
            print(' << NOTICE: 이미 저장된 가게입니다 >>')
            continue

        driver = webdriver.Chrome(chrome_driver_dir, options=options)
        driver.get(url)
        scroll_down(driver)
        load_and_save_img(driver, name, cate)
