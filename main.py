from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from time import sleep
from os import remove, mkdir
from os.path import exists
from parse_answer import *
from answer import *

current_path = path.dirname(__file__)
with open(current_path + '/config.json', "r", encoding='utf8') as f:
    config = json.load(f)

#safe_mode = input('想拿多少分？（最高100）：')
#safe_mode = int(safe_mode)
safe_mode = 93

user = config['username']
passwd = config['password']
browser = webdriver.Chrome()
browser.get(config['root'])
wait = WebDriverWait(browser, 3)
current = 1  # 题号
ansll = []  # 答案列表
question_quantity = 0  # 这张卷子的问题总数


def login(name, password):
    try:
        sleep(0.5)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#tbName'))).send_keys(name)
        wait.until(EC.presence_of_element_located(
            (By.CSS_SELECTOR, '#tbPwd'))).send_keys(password)
        wait.until(EC.element_to_be_clickable(
            (By.CSS_SELECTOR, '#btnLogin'))).click()
    except:
        login(name, password)


def intotest(is_first=1):
    try:
        sleep(1)
        browser.switch_to.default_content()
        browser.switch_to.frame('mainFrame')
        print('switched')
        if is_first:
            try:
                wait.until(EC.element_to_be_clickable(
                    (By.CSS_SELECTOR, '#ctl00_cphContent_divWarning > div > div.homework_3 > ul > li.homework_3_2 > span > a'))).click()
            except TimeoutException:
                browser.close()
                print('没有测试!!!')
                return False
        try:
            sleep(1)
            wait.until(EC.element_to_be_clickable(
                (By.XPATH, '//table[@class="DataGridTable"]/tbody/tr/td/span/span/input[@value!=" 查 看 "]'))).click()  # 点进入测试的按钮
            wait3 = WebDriverWait(browser, 1)
            try:
                wait3.until(EC.alert_is_present()).accept()  # 可能会出提示框，点掉
            except:
                pass
            return True
        except TimeoutException:
            try:
                wait.until(EC.element_to_be_clickable(
                    (By.XPATH, '//*[@id="ctl00_ContentPlaceHolder1_CourseTestTask1_dgTestTask_ctl19_PAGER"]/div/ul/li[14]/a'))).click()  # 下一页按钮
                return intotest(0)
            except TimeoutException:
                print('做完了')
                browser.close()
                return False

    except (TimeoutError, TimeoutException):
        intotest(is_first)


def define_question_content(question):  # 判断问题类型
    if question.find_element_by_xpath("./following-sibling::*[1]").tag_name == 'input':
        return 'fill_blank'
    elif question.find_element_by_xpath("./following-sibling::*[1]").tag_name == 'li':
        if question.find_element_by_xpath("./../li/input").get_attribute('type') == 'radio':
            return 'radio'
        if question.find_element_by_xpath("./../li/input").get_attribute('type') == 'text':
            return 'translation'
    elif question.find_element_by_xpath('..').tag_name == 'li':
        return 'reading'
    else:
        return ''


def get_answers():
    global ansll
    global question_quantity
    sleep(2)
    pageSource = browser.page_source
    try:
        with open(current_path+'/temp/source.html', 'w+', encoding='utf-8') as f:
            f.write(pageSource)
    except FileNotFoundError:
        mkdir(current_path + '/temp')
        with open(current_path+'/temp/source.html', 'w+', encoding='utf-8') as f:
            f.write(pageSource)

    prase_result()   # get the answers and save them into EnglishAnswer.html
    ansll = callback(safe_mode)  # get all of the answers
    question_quantity = len(ansll)


def answer_part_x(part_x=1):
    global ansll
    global current
    global question_quantity
    browser.switch_to.default_content()
    wait.until(EC.presence_of_element_located(
        (By.CSS_SELECTOR, '#aPart'+str(part_x)))).click()  # P
    browser.switch_to.frame('mainFrame')

    # anlist contains all the questions of current part
    anlist = wait.until(EC.presence_of_all_elements_located((By.XPATH,
                                                             '//span[contains(@id,"question_")]')))
    print(len(anlist))

    for question in anlist:
        wait2 = WebDriverWait(question, 3)
        question_type = define_question_content(question)
        if question_type == 'radio':
            wait2.until(EC.element_to_be_clickable(
                (By.XPATH, '../li/input[@id="'+ansll[current-1]+'"]'))).click()
            print('第'+str(current)+'题是选择题，填了'+ansll[current-1])
        if question_type == 'fill_blank':
            blank = wait2.until(
                EC.visibility_of_element_located((By.XPATH, './following-sibling::*[1]')))
            blank.clear()
            blank.send_keys(ansll[current - 1])
            print('第'+str(current)+'题是填空题，填了'+ansll[current-1])
        if question_type == 'reading':
            wait2.until(EC.element_to_be_clickable(
                (By.XPATH, '../../li/input[@id="'+ansll[current-1]+'"]'))).click()
            print('第'+str(current)+'题是选择题，填了'+ansll[current-1])
        if question_type == 'translation':
            # blank = question.find_element_by_xpath('../li/input')
            blank = wait2.until(
                EC.visibility_of_element_located((By.XPATH, '../li/input')))
            blank.clear()
            blank.send_keys(ansll[current - 1])
            print('第'+str(current)+'题是翻译题，填了'+ansll[current-1])
        current += 1

    # it means when the test is finished, auto submit
    if current >= question_quantity:
        browser.switch_to.default_content()
        wait.until(EC.element_to_be_clickable(
            (By.XPATH, '//*[@id="divHeader"]/div/div[4]/ul[2]/li[3]/input'))).click()
        wait.until(EC.alert_is_present()).accept()


def main(user, passwd):
    global current
    global question_quantity
    login(user, passwd)
    is_first = True
    while intotest(is_first):
        is_first = False
        get_answers()
        flag = 1
        current = 1

        # Auto finist Part 1 ~ Part n
        while current < question_quantity:
            answer_part_x(flag)
            flag += 1


if __name__ == '__main__':
    main(user, passwd)
