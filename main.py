import sys



def login_to_mis():
    print('logging in to mis...')
    driver.get('https://mis.bjtu.edu.cn')

    # captcha_div = WebDriverWait(driver, 10).until(
    #     expected_conditions.presence_of_element_located((By.CLASS_NAME, 'yzm'))
    # )
    # captcha = captcha_div.find_element(By.TAG_NAME, 'img')
    # print(captcha)
    # exit(0)

    # image_bytes = get_element_screenshot(captcha)
    # result = ttshitu_api(image_bytes)
    # print(result)

    name_input = driver.find_element(By.ID, 'id_loginname')
    password_input = driver.find_element(By.ID, 'id_password')
    # captcha_input = captcha_div.find_element(By.ID, 'id_captcha_1')
    submit = driver.find_element(By.CLASS_NAME, 'login').find_element(By.TAG_NAME, 'button')

    name_input.send_keys(user_id_str)
    password_input.send_keys(password_str)
    time.sleep(2)
    # captcha_input.send_keys(result)
    submit.click()

    time.sleep(2)
    # enter_course_selection()

    # 获取 cookie
    # cookies = driver.get_cookies()
    # print(cookies)

    # # 保存 cookie 到 json 文件
    # with open('cookies.json', 'w') as f:
    #     json.dump(cookies, f)


def enter_course_selection():
    driver.get('https://mis.bjtu.edu.cn/module/module/104/')
    driver.get('https://bksycenter.bjtu.edu.cn/NoMasterJumpPage.aspx?URL=jwcNjwStu&FPC=page:jwcNjwStu')
    driver.get('https://aa.bjtu.edu.cn/course_selection/courseselecttask/selects/')

if __name__ == '__main__':
    # 定义参数列表和默认值
    args_list = ['--login']
    args = dict.fromkeys(args_list, False)

    # 解析参数
    for arg in sys.argv:
        if arg in args_list:
            args[arg] = True

    if args['--login']:
        login_and_save_cookies()
        exit(0)
