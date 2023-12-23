import json
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

COURSES = [('C112002B', 2)]

def ring():
    os.system("afplay /System/Library/Sounds/Ping.aiff")

class sound(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        ring()
        # winsound.Beep(800, 1000)
        self._running = True


def login_and_save_cookies(driver):
    print('[login_and_save_cookies]')
    driver.get('https://mis.bjtu.edu.cn')

    print('waiting for login...')
    print('press enter to continue')
    input()

    driver.get('https://mis.bjtu.edu.cn/module/module/104/')
    driver.get('https://bksycenter.bjtu.edu.cn/NoMasterJumpPage.aspx?URL=jwcNjwStu&FPC=page:jwcNjwStu')
    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')

    # 获取 cookie
    cookies = driver.get_cookies()
    print(cookies)

    # 保存 cookie 到 json 文件
    with open('cookies.json', 'w') as f:
        json.dump(cookies, f)


def enter_course_selection():
    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')
    time.sleep(1)

    # 加载 cookies
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')


# 必修课、专业选修课
def phase1(driver, courses: [(str, int)]):
    enter_course_selection()

    time.sleep(2)
    while True:
        driver.refresh()
        for course_number, course_index in courses:
            try:
                courses_div = driver.find_element(By.ID, 'current')
                courses_table = courses_div.find_element(By.CLASS_NAME, 'table')
                checkboxs = courses_table.find_elements(By.XPATH, f'//input[@name="checkboxs"and@kch="{course_number}"]')
                threadSound = sound()
                threadSound.start()
                checkbox = checkboxs[course_index - 1].find_element(By.XPATH, "..")
                checkbox.click()
                print('它出现了！')

                time.sleep(0.2)
                try:
                    btn_ok = driver.find_element(By.CLASS_NAME, 'modal-footer').find_element(By.CLASS_NAME, 'btn-info')
                    btn_ok.click()
                except e:
                    pass

                time.sleep(0.4)
                submit = driver.find_element(By.ID, 'select-submit-btn')
                submit.send_keys(Keys.ENTER)

                keep_running = input('退出？(y/n)')
                if keep_running == 'y':
                    exit(0)
            except Exception as e:
                pass

        time.sleep(0.3)


# 任选课、其他专业课程
def phase2(driver, courses: [(str, int)]):
    enter_course_selection()

    time.sleep(2)
    in_iframe = False
    if not in_iframe:
        driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
        in_iframe = True

    while True:
        for course_number, course_index in courses:
            course_number_input = driver.find_element(By.XPATH, '//input[@name="kch"]')
            course_number_input.send_keys(course_number)
            course_index_input = driver.find_element(By.XPATH, '//input[@name="kxh"]')
            course_index_input.send_keys(course_index)
            search_btn = driver.find_element(By.XPATH, '//button[@name="submit"]')
            if not in_iframe:
                driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
                in_iframe = True
            search_btn.click()

            td = driver.find_element(By.XPATH, '//table/tbody/tr/td')
            try:
                checkbox = td.find_element(By.TAG_NAME, 'input')
                threadSound = sound()
                threadSound.start()
                checkbox.click()
                print('它出现了！')

                time.sleep(0.2)
                if in_iframe:
                    driver.switch_to.default_content()
                    in_iframe = False
                btn_ok = driver.find_element(By.CLASS_NAME, 'modal-footer').find_element(By.CLASS_NAME, 'btn-info')
                btn_ok.click()

                time.sleep(0.2)
                if not in_iframe:
                    driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))
                    in_iframe = True
                submit = driver.find_element(By.ID, 'select-submit-btn')
                submit.click()

                # time.sleep(0.2)
                # driver.switch_to.default_content()
                # captcha_div = WebDriverWait(driver, 10).until(
                #     expected_conditions.presence_of_element_located((By.CLASS_NAME, 'captcha-dialog'))
                # )
                # captcha = captcha_div.find_element(By.TAG_NAME, 'img')

                # print('正在识别验证码...')
                # image_bytes = get_element_screenshot(captcha)
                # result = ttshitu_api(image_bytes, 16)
                # print(f'识别结果：{result}')
                #
                # captcha_input = captcha_div.find_element(By.TAG_NAME, 'input')
                # captcha_input.send_keys(result)
                #
                # btn_ok = driver.find_element(By.CLASS_NAME, 'modal-footer').find_element(By.CLASS_NAME, 'btn-info')
                # btn_ok.click()
                # print('选上辣！')
                keep_running = input('退出？(y/n)')
                if keep_running == 'y':
                    exit(0)
            except Exception as e:
                pass
                # print(e)

            time.sleep(0.3)


import argparse
def parse_arguments():
    parser = argparse.ArgumentParser(description="BJTU-CC")

    parser.add_argument("--ring", action="store_true", help="test ring")
    parser.add_argument("--login", action="store_true", help="login and save cookies")
    parser.add_argument("--phase", type=int, default=1, help="phase 1 or 2")

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_arguments()

    if args.ring:
        ring()
        exit(0)

    driver = webdriver.ChromiumEdge()

    if args.login:
        login_and_save_cookies(driver)
    
    if args.phase == 1:
        phase1(driver, COURSES)
    elif args.phase == 2:
        phase2(driver, COURSES)
