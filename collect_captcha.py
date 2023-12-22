import io
from io import BytesIO

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from PIL import Image
import base64
import json
import requests
from configparser import ConfigParser
import threading

driver = webdriver.ChromiumEdge()
conf = ConfigParser()
conf.read("init.conf", encoding="utf8")

wait = WebDriverWait(driver, 10)

import os
def getNum():
    return len(os.listdir('captcha'))

import sys
if __name__ == '__main__':
    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')

    driver.add_cookie({'name': 'sessionid', 'value': 'cmw6518tl04yrv20hhf4wyitcm5tripr', 'domain': 'aa.bjtu.edu.cn', 'path': '/'})
    driver.add_cookie({'name': 'csrftoken', 'value': 'T41FUZF39ai0ZxOcPZQPSrTwEvNyZkXt', 'domain': 'aa.bjtu.edu.cn', 'path': '/'})

    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')
    time.sleep(2)

    while True:
        driver.refresh()
        try:
            courses_div = driver.find_element(By.ID, 'current')
            courses_table = courses_div.find_element(By.CLASS_NAME, 'table')
            checkbox = courses_table.find_element(By.XPATH, f'//input[@name="checkboxs"and@kch]')
            checkbox = checkbox.find_element(By.XPATH, "..")
            checkbox.click()

            time.sleep(0.2)
            try:
                btn_ok = driver.find_element(By.CLASS_NAME, 'modal-footer').find_element(By.CLASS_NAME, 'btn-info')
                btn_ok.click()
            except e:
                pass

            time.sleep(0.4)
            submit = driver.find_element(By.ID, 'select-submit-btn')
            submit.send_keys(Keys.ENTER)

            time.sleep(0.5)
            captcha_div = driver.find_element(By.XPATH, '//div[@class="captcha-dialog"]/img[@src]')
            captcha_div.screenshot(f"captcha/captcha{getNum()}.png")

            # 保存图片到本地
            # img.save(f"captcha/saved_image{getNum()}.jpg")
        except Exception as e:
            print(e)
            pass
        # exit(0)

        time.sleep(4)
