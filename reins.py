import time
import json
import re
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

from selenium.webdriver.support.ui import Select

chrome_options = Options()
prefs = {"profile.managed_default_content_settings.images": 2}
chrome_options.add_experimental_option("prefs", prefs)

# 物件種別１, 2
estate_types = {        
    '01',	# : '売土地',
    '02',	# : '売一戸建',
    '03',	# : '売マンション',
    '04'	# : '売外全(住宅以外建物全部)',
}

# 都道府県名
prefecture_names = [        
    '神奈川県',
    '東京都'
]

city_names = [
    # 所在地名1
    [        
        '相模原市',
        '座間市',
        '厚木市',
        '愛甲郡愛川町'
    ],
    # 所在地名3
    [        
        '町田市',
        '八王子市'
    ]
]

def getGoodInfo(link):
    
    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
    driver.get(link)
    
    # soup = BeautifulSoup(driver.page_source, 'html.parser')
    # ImageCarousel = soup.find('div', {'class': 'ImageCarousel84'})

    # ログイン page start
    wait = WebDriverWait(driver, 10)
    wait.until(EC.presence_of_element_located((By.ID, "__BVID__13")))

    id_element = driver.find_element(By.ID, "__BVID__13")
    id_element.send_keys("137076210520")

    wait.until(EC.presence_of_element_located((By.ID, "__BVID__16")))
    pwd_element = driver.find_element(By.ID, "__BVID__16")
    pwd_element.send_keys("v2dtjx")

    wait.until(EC.presence_of_element_located((By.ID, "__BVID__18")))
    lem_capt = driver.find_element(By.XPATH, '//*[@class="p-checkbox-input custom-control custom-checkbox"]/label')
    lem_capt.click()

    wait.until(EC.presence_of_element_located((By.ID, "__BVID__20")))
    lem_capt = driver.find_element(By.XPATH, '//*[@class="p-checkbox-input custom-control custom-checkbox b-custom-control-lg"]/label')
    lem_capt.click()

    # btn_label = "ログイン"
    loginbtn = driver.find_element(By.XPATH, "//button[(text() = 'ログイン')]")
    loginbtn.click()    
    # lem_capt = driver.find_element(By.CLASS_NAME, "btn-primary")
    # lem_capt.click()

    # ログイン page end

    # メイン page start
    time.sleep(10)
    # btn_label = "売買 物件検索"
    wait.until(EC.presence_of_element_located((By.ID, "osrslink")))
    search_btn = driver.find_element(By.XPATH, "//button[(text() = '売買 物件検索')]")
    search_btn.click()    
    # メイン page end

    # 売買検索条件入力 page start
    # time.sleep(10)

    # 物件種別１
    wait.until(EC.presence_of_element_located((By.ID, "__BVID__241")))

    estate_type1 = Select(driver.find_element(By.ID, "__BVID__241"))

    for estate_type in estate_types:
        # select by value 
        estate_type1.select_by_value(estate_type)
        # time.sleep(2)
    
        # 物件種別2
        estate_type2 = Select(driver.find_element(By.ID, "__BVID__250"))
        for estate_type in estate_types:
            # select by value 
            estate_type2.select_by_value(estate_type)
            time.sleep(2)
            
            # 都道府県名
            prefecture_name_value = driver.find_element(By.ID, "__BVID__311")
            # prefecture_name_value.clear()
            # 所在地名
            city_name_value = driver.find_element(By.ID, "__BVID__315")
            # city_name_value.clear()

            idx1 = 0

            for prefecture_name in prefecture_names:
                prefecture_name_value.clear()
                # city_name_value.clear()

                # city_name_value = driver.find_element(By.ID, "__BVID__315")
                prefecture_name_value.send_keys(prefecture_name)

                for city_name in city_names[idx1]:
                    wait.until(EC.presence_of_element_located((By.ID, "__BVID__241")))
                
                    city_name_value.clear()
                    city_name_value.send_keys(city_name)

                    # 前日 radio button click
                    date_element1 = driver.find_elements(By.XPATH, "//label[contains(text(),'前日')]/preceding-sibling::input")
                    
                    for date_element in date_element1:
                        with open('./jquery.js', errors='ignore') as f:
                            driver.execute_script(f.read())
                        driver.execute_script("$(arguments[0]).click();", date_element)

                    time.sleep(2)
                    # 検索 button click
                    search_btn = driver.find_element(By.XPATH, "//button[contains(text(),'検索')]")
                    search_btn.click()
                    
                    time.sleep(15)

                    # 売買検索結果一覧（在庫） page start
                    checkbox_btn1 = driver.find_elements(By.XPATH, '//*[@class="p-checkbox-input custom-control custom-checkbox"]/input')
                    for checkbox_btn in checkbox_btn1:
                        with open('./jquery.js', errors='ignore') as f:
                            driver.execute_script(f.read())
                        driver.execute_script("$(arguments[0]).click();", checkbox_btn)
                        
                        # 図面一括取得 button click
                        get_btn = driver.find_element(By.XPATH, "//button[(text() = '図面一括取得')]")
                        get_btn.click()    

                        # uncheck
                        time.sleep(5)
                        driver.execute_script("$(arguments[0]).click();", checkbox_btn)
                        time.sleep(40)

                    time.sleep(10)
                    # 売買検索結果一覧（在庫） page end

                    # back button click
                    back_btn = driver.find_element(By.XPATH, '//*[@class="p-frame-backer"]')
                    back_btn.click()
                    time.sleep(2)

                idx1 = idx1 + 1

    # 売買検索条件入力 page end


    print('okkkkkkkkkkkkkkk')

    # time.sleep(15)

    driver.quit()

getGoodInfo('https://system.reins.jp/login/main/KG/GKG001200')