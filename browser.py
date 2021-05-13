# write your code here
# -*- coding: cp1251
import argparse
import os
import requests

from bs4 import BeautifulSoup
from collections import deque
from colorama import Fore


def print_from_cache(file_name):
    if os.access(file_name, os.F_OK):
        with open(file_name) as f:
            for line in f:
                print(line)
    else:
        return 'error in File'


stack_url = deque()

# 1. получить со входа имя каталога, если его не существет, создать
parser = argparse.ArgumentParser(description="Text-Based Browser")
parser.add_argument('dir', type=str, help='a directory for saved tabs')
args = parser.parse_args()
file_dir = args.dir

# if dir not exits, create it
if not os.path.isdir(file_dir):
    os.mkdir(file_dir)
else:
    pass

current_url = ''

while True:
    input_str = input()
    url = input_str.lower().lstrip('https://')
    url_name = url.replace('.com', '').replace('.org', '')  # выбрасываем все что после точки
    if url == 'exit':
        # print(os.getcwd())
        break
    elif url == 'back':
        if stack_url != deque([]):
            current_url = stack_url.pop()
            # печатаем из кеша файл с соотв. именем
            print_from_cache(os.path.join(file_dir, current_url))
    elif '.' in url:  # valid URL
        r = requests.get('https://' + url)
        if r:
            if url_name not in os.listdir(file_dir):
                # пишем в файл кеша и печатаем содержимое
                soup = BeautifulSoup(r.content, 'html.parser')
                p2 = soup.find_all({'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'ul', 'ol', 'li'})
                with open(f'{file_dir}/{url_name}', 'w', encoding='utf-8') as file:
                    stack_url.append(url_name)
                    for p in p2:
                        file.write(p.text)
                        if p.name == 'a':
                            print(Fore.BLUE + p.text)
                        else:
                            print(p.text)
            elif url_name in os.listdir(file_dir):
                #  читаем содержимое из кеша
                print_from_cache(os.path.join(file_dir, url_name))
                stack_url.append(url_name)
        else:
            print('Incorrect URL')
    else:
        print('Incorrect URL')
