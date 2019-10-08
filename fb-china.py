import time
import re
import requests
from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from lxml import etree

browser = webdriver.Chrome()
wait = WebDriverWait(browser, 5)

def login():
    browser.get('https://www.facebook.com')
    input_phone = browser.find_element_by_xpath('//*[@id = "email"]')
    input_phone.send_keys('')
    input_password = browser.find_element_by_xpath('//*[@id = "pass"]')
    input_password.send_keys('')
    button = browser.find_element_by_xpath('//*[@id="loginbutton"]')
    button.click()

    #我的chrome 为什么登陆之后 浏览器会弹出对话框，问是否允许……一下5秒是为了流出时间手工点击允许
    time.sleep(5)

    #facebook网站本身也会弹出对话框，如果没有弹出，这几行就不要了
    # try:
    #     button1 = browser.find_element_by_xpath('//*[@id="facebook"]/body/div[18]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/a[1]')
    #     button1.click()
    #
    # except:
    #     button1 = browser.find_element_by_xpath('//*[@id="facebook"]/body/div[19]/div[2]/div/div/div/div/div[3]/div/div/div[2]/div/a[1]')
    #
    #     button1.click()

def crawler(url):
    #现在先爬的网址是18年2月的，这个网址里有一个2018-02可以对其进行修改，调整月份
    global c
    browser.get(url)
    #现在只下拉50次，基本30多次就会看到 the end
    for i in range(50):
       button_see_mores = browser.find_elements_by_class_name('_307z')
       for button_see_more in button_see_mores:
           browser.execute_script("arguments[0].scrollIntoView();", button_see_more)
           time.sleep(1)

           #以下都是为了点击展开 see more部分，先后尝试点击2x4v和2ye3
           try:
              bottom = button_see_more.find_element_by_xpath('.//a[@class="_2x4v"]')
              ActionChains(browser).click(bottom).perform()
           except Exception:
              try:
                  website = button_see_more.find_element_by_xpath('.//div[@class="_2ye3"]')
                  ActionChains(browser).click(website).perform()
              except:
                  pass
           time.sleep(1)

       #滚动到底，周jj说休息时间长一点，然而我看并没有什么卵用
       try:
          browser.execute_script('window.scrollTo(0, document.body.scrollHeight)')
          time.sleep(3)
       except Exception:
          break



    #滚动完成之后，一次性写入txt，这时候cpu占用率会爆炸，周jj说我太爱惜电脑
    f = open('E:/python/fb-china 2012.txt','a',encoding='utf-8')

    current_page = browser.page_source
    selector = etree.HTML(current_page)
    whole_posts = selector.findall('.//div[@class="_1dwg _1w_m _q7o"]')  #展开过的posts
    posts = selector.findall('.//div[@class="_307z"]')  #因各种原因没被展开的


    for whole_post in  whole_posts:
       sentence = whole_post.xpath('.//p/text()')
       passage = ''.join(sentence)
       print(passage)
       posted_time = whole_post.xpath('.//span[@class="timestampContent"]/text()')
       posted_time1 = posted_time[0]
       print(posted_time1)
       c = c + 1
       print(c)
       try:
         f.write(passage +'\n')
         f.write(posted_time1 + '\n')

       except:
           pass

    for post in posts:
        sentence2 = post.xpath('.//span[@class="_5-jo"]')[0]
        passage2 = sentence2.xpath('string(.)')
        passage2 = str(passage2)
        content = ''.join(passage2)
        print(content)
        posted_time2 = post.xpath('.//span[@class="timestampContent"]/text()')
        posted_time3 = posted_time2[0]
        print(posted_time3)
        c = c + 1
        print(c)

        try:
            f.write(content +'\n')
            f.write(posted_time3 + '\n')

        except:
            pass
    f.close()

    time.sleep(1)


def main():

    login()
    c = 0
    year = ['2012-', '2013-', '2014-', '2015-', '2016-','2017-']
    month = ['01','02','03','04','05','06','07','08','09','10','11','12']
    for i in year:
        for j in month:
            k=i+j
            url_1='https://www.facebook.com/search/str/china/stories-keyword/stories-opinion?see_more_ref=eyJzaWQiOiIiLCJyZWYiOiJoZWFkZXJfc2VlX2FsbCJ9&filters_rp_creation_time=%7B%22name%22%3A%22creation_time%22%2C%22args%22%3A%22%7B%5C%22start_month%5C%22%3A%5C%22'
            url_2='%5C%22%2C%5C%22end_month%5C%22%3A%5C%22'
            url_3='%5C%22%7D%22%7D'
            url=url_1 +k+ url_2 +k+ url_3
            crawler(url)
    browser.close()


if __name__ == '__main__':
    main()