from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome import service as fs
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
import random
from datetime import datetime
import time
import configparser


def create_body_temperature():
    body_temperature = round(random.uniform(36.0, 37.0), 1)
    return body_temperature


def rite_forms():
    options = Options()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    chrome_service = fs.Service(executable_path='/opt/chrome/chromedriver')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    driver.get(str(config['DEFAULT']['FormsUrl']))
    # クラスを選択
    element = driver.find_element(
        By.XPATH,
        str(config['DEFAULT']['Class_Element'])
    )
    element.click()

    # 名前を入力
    element = driver.find_element(
        By.XPATH,
        '//*[@id="form-main-content"]/div/div[1]/div[2]/div[2]/div[2]/div/div[3]/div/div/input'
    )
    element.send_keys(str(config['DEFAULT']['Name']))

    # 体温を入力
    element = driver.find_element(
        By.XPATH,
        '//*[@id="form-main-content"]/div/div[1]/div[2]/div[2]/div[3]/div/div[3]/div/div/input'
    )
    body_temperature = create_body_temperature()
    element.send_keys(str(body_temperature))

    # フォームを送信
    element = driver.find_element(
        By.XPATH,
        '//*[@id="form-main-content"]/div/div[1]/div[2]/div[3]/div[1]/button'
    )
    element.click()


def main():
    error_count = 1
    while error_count > 0:
        try:
            error_count = 0
            rite_forms()
        except NoSuchElementException:
            error_count += 1
            print(error_count)


if __name__ == '__main__':
    count = 0
    config = configparser.ConfigParser()
    config.read('config.ini', 'UTF-8')
    while True:
        datetime = datetime.now()
        now_hour = datetime.hour
        print(now_hour)
        if now_hour == int(config['DEFAULT']['Hour']):
            now_minute = datetime.minute
            print(now_minute)
            if now_minute != int(config['DEFAULT']['Minute']) and count == 1:
                count = 0
            if now_minute == int(config['DEFAULT']['Minute']) and count == 0:
                main()
                count = 1
        time.sleep(1.0)