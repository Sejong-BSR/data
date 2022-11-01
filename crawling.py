import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs4
import time
from selenium.webdriver.support.ui import WebDriverWait as wait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from urllib.request import urlopen
from urllib.parse import quote_plus
import urllib.request
import urllib
from PIL import Image
import ssl
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
import time
import warnings
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import NoSuchElementException,StaleElementReferenceException
from urllib import parse
import json
from urllib.request import urlopen
from PIL import Image
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import tqdm

def Crawling_Naver():
    temp = []
    for page in range(1,10):
        url_temp = 'https://map.naver.com/v5/api/search?caller=pcweb&query=%EC%9D%8C%EC%8B%9D%EC%A0%90&type=all&searchCoord={};{}&page={}&displayCount={}&isPlaceRecommendationReplace=true&lang=ko'
        latitude = 126.93632421051524 # 현재 위도
        longitude = 37.55433832843096 # 현재 경도
        displayCount = 5 # 탐색할 가게 개수
        url = url_temp.format(latitude, longitude, page,displayCount)
        response = urlopen(url)
        json_data = json.load(response)['result']['place']['list']
        temp = []
        for place in json_data:
            temp.append([place['id'],place['name'],place['category']])

    return temp

def make_url(paths):
    url_lst = []
    for i in range(len(paths)):
        url = "https://pcmap.place.naver.com/restaurant/" + paths[i] + "/photo"
        url_lst.append(url)
    return url_lst

def scroll_down(driver):
    num_of_scroll = 2 # 스크롤 횟수 (커질수록 가져오는 이미지 양 많아짐)
    for i in range(num_of_scroll):
        driver.find_element(By.CSS_SELECTOR,'body').send_keys(Keys.PAGE_DOWN)
        time.sleep(1)

def load_img(driver,names,i):
    imgs = driver.find_elements(By.CSS_SELECTOR, 'a.place_thumb>img')
    img_url = []
    for image in imgs :
        url = image.get_attribute('src')
        img_url.append(url)

    img_folder = './img/' + names[i]
    if not os.path.isdir(img_folder) : # 없으면 새로 생성하는 조건문
        os.mkdir(img_folder)

    for index, link in enumerate(img_url) :
        urllib.request.urlretrieve(link, f'{img_folder}/{index}.jpg')
        img = Image.open(f'{img_folder}/{index}.jpg')
        img_resize = img.resize((256, 256))
        img_resize.save(f'{img_folder}/{index}.jpg')

def set_chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def main(paths,names):
    url_lst = make_url(paths) # all store url
    for i in tqdm(range(len(url_lst))):
        #driver = webdriver.Chrome('C:/Users/jaehoon/chromedriver') # 사용자에 맞게 chrome driver 설치 후 위치 지정해줘야함
        driver = set_chrome_driver()
        driver.get(url_lst[i])
        scroll_down(driver)
        load_img(driver,names,i)


if __name__ == "__main__":
    id,names = [], []
    info = Crawling_Naver()
    for i in range(len(info)):
        id.append(info[i][0])
        names.append(info[i][1])
    main(id,names)