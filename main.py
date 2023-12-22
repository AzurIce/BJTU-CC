import json
import os
import sys
import threading
import time

from selenium import webdriver
from selenium.webdriver import Keys
from selenium.webdriver.common.by import By

driver = webdriver.ChromiumEdge()

class sound(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

    def run(self):
        os.system("afplay /System/Library/Sounds/Ping.aiff")
        # winsound.Beep(800, 1000)
        self._running = True


def login_and_save_cookies():
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


def current_semester(course_numbers: [str]):
    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')
    time.sleep(2)

    # 加载 cookies
    with open('cookies.json', 'r') as file:
        cookies = json.load(file)
    for cookie in cookies:
        driver.add_cookie(cookie)

    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')
    time.sleep(2)

    while True:
        driver.refresh()
        for course_number in course_numbers:
            try:
                courses_div = driver.find_element(By.ID, 'current')
                courses_table = courses_div.find_element(By.CLASS_NAME, 'table')
                checkbox = courses_table.find_element(By.XPATH, f'//input[@name="checkboxs"and@kch="{course_number}"]')
                threadSound = sound()
                threadSound.start()
                checkbox = checkbox.find_element(By.XPATH, "..")
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

        time.sleep(0.2)


if __name__ == '__main__':
    # 定义参数列表和默认值
    args_list = ['--login', '--current']
    args = dict.fromkeys(args_list, False)

    # 解析参数
    for arg in sys.argv:
        if arg in args_list:
            args[arg] = True

    if args['--login']:
        login_and_save_cookies()
    
    if args['--current']:
        current_semester(['M410019B'])
