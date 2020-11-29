from requests import get
from sys import argv
from re import findall
from pathlib import Path
from json import dump
from multiprocessing import Pool

from bs4 import BeautifulSoup
from tqdm import tqdm

d = Path('data')
d.mkdir(exist_ok=True)


def deal_one(line):
    try:
        url = line.strip()
        filename = d / (url.split('/')[-1].split('.')[0] + '.json')
        if filename.exists():
            return
        soup = BeautifulSoup(get(url).text, 'lxml')
        data = {
            'title': soup.find(class_='headline').text.strip(),
            'source': soup.find(class_='comeFrom').find('a').text.strip(),
            'time': soup.find(class_='time').text.strip(),
            'content': soup.find(class_='artical-main-content').text.strip(),
        }
        dump(data, open(filename, 'w'), ensure_ascii=False)
    except Exception as e:
        print(url, e)


def detail():
    lines = open('list.txt').readlines()
    # A multiprocess trick as simple as OpenMP with a process bar from tqdm
    # refer: https://stackoverflow.com/questions/41920124/multiprocessing-use-tqdm-to-display-a-progress-bar
    with Pool(8) as p:
        list(tqdm(p.imap(deal_one, lines), total=len(lines)))


def index():
    if len(argv) != 3:
        print('usage: python crawler.py index <first_page> <last_page>')
    url = 'https://voice.hupu.com/soccer/tag/496-%d.html'
    file = open('list.txt', 'a')
    for page in tqdm(range(int(argv[2]), int(argv[3]) + 1)):
        try:
            text = get(url % page).text
            data = findall(
                '<a href="(https://voice.hupu.com/soccer/\d*\.html)"', text)
            print('\n'.join(set(data)), file=file)
        except Exception as e:
            print(url % page, e)
    file.close()


if __name__ == "__main__":
    if len(argv) < 2:
        print('usage: python crawler.py [ index | detail ] ...')
    elif argv[1] == 'index':
        index()
    elif argv[1] == 'detail':
        detail()
