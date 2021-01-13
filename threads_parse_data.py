# -*- coding: utf-8 -*-
from urllib.request import urlopen, Request
from threading import Thread
import time 
import datetime
import queue
import concurrent.futures as futures

import requests
import pandas as pd
import json
from bs4 import BeautifulSoup
from bs4.element import Comment

_MAX_CONNECTIONS = 300

MODE = 'full'
TEST = False

headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) ' 
                      'AppleWebKit/537.11 (KHTML, like Gecko) '
                      'Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'none',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive'}


def tag_visible(element):
    if element.parent.name in ['style', 'script', 'head', 'title', 'meta', '[document]']:
        return False
    if isinstance(element, Comment):
        return False
    return True

def text_from_html(body):
    soup = BeautifulSoup(body, 'html.parser')
    soup = soup.find("div", {"class": "column-3"})
    texts = soup.findAll(text=True)
    visible_texts = filter(tag_visible, texts) 
    result = "\n".join(t.strip() for t in visible_texts)
    result = result.replace('\n\n', '\n') 
    return result

full_list = []

def ping(node):
    global MODE
    global full_list 
    no_table = ''
    try:
        url = 'https://' + node['host'] + '/about/more'
        
        all_tables = []
        r = requests.get(url, headers=headers)
        try:
            tables_temp = pd.read_html(r.text)
            for t in tables_temp:
              all_tables += [_[1] for _ in json.loads(t.T.to_json()).items()]

        except Exception as table_e:
            no_table = str(table_e)
            

        about_more = text_from_html(r.text)
        
        node['moderatedServers'] = {'table' : all_tables, 'tableError': no_table}
        node['aboutMore'] = about_more
        node['error'] = ''
        print(node['host'], 'is done.', '*'*30, ' ' + no_table)
        if MODE == 'good':
            return node
        if MODE == 'full':
            node['status'] = 'updated'
            full_list.append(node)
        
    except Exception as e:
        if 'WinError 10060' in str(e):
            error = 'TimeoutError'
        elif 'WinError 10061' in str(e):
            error = 'ConnectionRefusedError'
        elif 'WinError 10054' in str(e):
            error = 'ConnectionResetError' 
        else:
            error = e
        print(node['host'], 'DENIED.', error)
        if MODE == 'bad':
            return {'host': node['host'], 'error': e}
        if MODE == 'full':
            node['status'] = 'denied'
            node['moderatedServers'] = {'table' : '', 'tableError': no_table}
            node['aboutMore'] = ''
            if e != error:
                node['error'] = str(e) + ' / ' + error
            else:
                node['error'] = str(e)
            full_list.append(node)



with open('restructured_dump.json', encoding='utf-8') as fh:
    data = json.load(fh)

if TEST:
    data = data[:100]

time1 = time.time()

print('Starting...')

with futures.ThreadPoolExecutor(max_workers=_MAX_CONNECTIONS) as executor:
    results = executor.map(ping, data)
    

all = list(results)

if MODE == 'good':
    with open('new_data.json', 'w', encoding='utf8') as json_file:
        json.dump(all, json_file, ensure_ascii=False)
    print(MODE, len(all))

if MODE == 'bad':
    with open('denied.json', 'w', encoding='utf8') as json_file:
        json.dump(all, json_file, ensure_ascii=False)
    print(MODE, len(all))

if MODE == 'full':
    with open('full.json', 'w', encoding='utf8') as json_file:
        json.dump(full_list, json_file, ensure_ascii=False)
    print(MODE, len(full_list))


print('\n', time.time() - time1)


