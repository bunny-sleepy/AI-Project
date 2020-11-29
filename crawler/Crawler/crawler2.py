from selenium import webdriver  # 用来驱动浏览器的
from selenium.webdriver import ActionChains  # 破解滑动验证码的时候用的 可以拖动图片
from selenium.webdriver.common.by import By  # 按照什么方式查找，By.ID,By.CSS_SELECTOR
from selenium.webdriver.common.keys import Keys  # 键盘按键操作
from selenium.webdriver.support import expected_conditions as EC  # 和下面WebDriverWait一起用的
from selenium.webdriver.support.wait import WebDriverWait  # 等待页面加载某些元素
import json
from json import dump
from pathlib import Path
import time
import re
import random

d = Path('data2')
d.mkdir(exist_ok=True)

def function1():
    urls = re.compile(r'https://movie.douban.com/subject/\d+/')

    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    url = "https://movie.douban.com/typerank?type_name=%E5%89%A7%E6%83%85%E7%89%87&type=11&interval_id=85:75&action="
    urlset = set()

    driver.get(url)

    for i in range(40):
        scroll = "window.scrollTo(0, document.body.scrollHeight)"
        driver.execute_script(scroll)
        time.sleep(1)
    for single in urls.findall(driver.page_source):
        urlset.add(single)

    file = open('urls2.txt','w')
    for i in urlset:
        print(i,file=file)
        print('\n')
    file.close

def function2():
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    file = open('urls.txt','r')
    name = re.compile(r'<span property="v:itemreviewed">(.*)</span>')
    celebrity = re.compile(r'<a href="/celebrity/(\d+)/" rel="v:starring">([^"]*?)</a>')
    summary = re.compile(r'<span property="v:summary" class="">([\s\S]*?)</span>')
    summary_hidden = re.compile(r'<span class="all hidden">([\s\S]*?)</span>')
    img = re.compile(r'<img src="([^<]*?)" title="点击看更多海报" alt="[^<]*?" rel="v:image">')
    runtime = re.compile(r'<span property="v:runtime" content="\d+?">([^"]+?)</span>')
    comment = re.compile(r'<div class="comment">([\s\S]*?)</div>')
    comment_hideitem = re.compile(r'<span class="hide-item full">([\s\S]*?)</span>')
    comment_short = re.compile(r'<span class="short">([\s\S]*?)</span>')
    urlset = set()
    num = 1462
    for i in range(num):
        url = file.readline()
        url = re.sub('\n','',url)
        urlset.add(url)
    file.close()

    for single in urlset:
        try:
            form = dict()
            filename_ = re.search(r'\d+',single)
            filename = (filename_.group())
            driver.get(single)
            time.sleep(random.uniform(0,1))
            data = driver.page_source
            form['name'] = name.search(data).group(1)
            form['celebrity'] = celebrity.findall(data)
            try:
                summary_text = summary.search(data).group(1)
            except AttributeError:
                summary_text = summary_hidden.search(data).group(1)
            summary_text = re.sub(r'\s', '', summary_text)
            summary_text = re.sub('<br>', '\n', summary_text)
            form['summary'] = summary_text
            form['imgsrc'] = img.search(data).group(1)
            form['runtime'] = runtime.search(data).group(1)
            comment_data = comment.findall(data)
            comments = list()
            for single_comment in comment_data:
                try:
                    comments.append(comment_hideitem.search(single_comment).group(1))
                except AttributeError:
                    try:
                        comments.append(comment_short.search(single_comment).group(1))
                    except AttributeError:
                        pass
            form['comments'] = comments
            file = open('./data/%s.json' % filename, 'w',encoding="utf-8")
            dump(form, file, ensure_ascii=False)
            file.close()
        except Exception as e:
            print(single, e)
    driver.close()

def function3():
    driver = webdriver.Chrome("C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe")
    begin = 3734112
    end = 34875370

    '''summary = re.compile(r'<span class="short">([\s\S]*?)</span>')'''
    gender = re.compile(r'<li>\s*?<span>性别</span>\s*?:\s*?([\S]*?)\s*?</li>')
    summary_hidden = re.compile(r'<span class="all hidden">([\s\S]*?)</span>')
    summary_bd = re.compile(r'<div id="intro" class="mod">\s*?<div class="hd">[\s\S]*?</div>\s*?<div class="bd">([\s\S]*?)</div>\s*?</div>')
    imgsrc = re.compile(r'<img alt="[\s\S]*?" title="点击看大图" src="([\s\S]*?)">')
    birthday = re.compile(r'<li>\s*?<span>出生日期</span>:\s*?(\S*?)\s*?</li>')
    birth_and_death = re.compile(r'<li>\s*?<span>生卒日期</span>\s*?:\s*?(\S*?)\s*?至\s*?(\S*?)\s*?</li>')

    for i in range(begin,end):
        try:
            form = json.load(open('./data/%d.json' % i,encoding='utf-8'))
        except FileNotFoundError:
            continue

        for actor in form["celebrity"]:
            try:
                filename = d / ('%s.json' % actor[1])
                if filename.exists():
                    print("ok")
                    continue
                actor_form = dict()
                actor_form["name"] = actor[1]
                actor_url = "https://movie.douban.com/celebrity/%s/" % actor[0]
                driver.get(actor_url)
                time.sleep(random.uniform(0,3.0))
                data = driver.page_source
                try:
                    actor_form["gender"] = gender.search(data).group(1)
                except AttributeError as e:
                    actor_form["gender"] = "notFound"
                    '''print(i, actor_url, actor[1], "genderNotFound")'''
                try:
                    summary_text = summary_hidden.search(data).group(1)
                except AttributeError:
                    try:
                        summary_text = summary_bd.search(data).group(1)
                    except AttributeError as e:
                        summary_text = "notFound"
                        '''print(i, actor_url, actor[1], "SummaryNotFound")'''
                summary_text = re.sub(r'\s', '', summary_text)
                summary_text = re.sub('<br>', '\n', summary_text)

                '''print(summary_text)'''

                actor_form["summary"] = summary_text
                try:
                    actor_form["imgsrc"] = imgsrc.search(data).group(1)
                except AttributeError as e:
                    actor_form["imgsrc"] = "notFound"
                    '''print(i, actor_url, actor[1], "imgNotFound")

                print(actor_form["imgsrc"])'''

                try:
                    actor_form["birth"] = birth_and_death.search(data).group(1)
                    actor_form["death"] = birth_and_death.search(data).group(2)
                except AttributeError:
                    try:
                        actor_form["birth"] = birthday.search(data).group(1)
                        actor_form["death"] = "notFound"
                    except AttributeError as e:
                        actor_form["birth"] = "notFound"
                        actor_form["death"] = "notFound"
                        '''print(i, actor_url, actor[1], "birthAndDeathNotFound")'''
                '''print(actor_form["birth"])'''

                if actor_form["summary"] == "notFound" and actor_form["gender"] == "notFound" and actor_form["birth"] == "notFound":
                    return

                dump(actor_form, open(filename, 'w', encoding='utf-8'), ensure_ascii=False)
            except Exception as e:
                print(i, actor_url, e)

if __name__ == '__main__':
    function3()