#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on 2016年10月14日

@author: wanmaosheng
'''

import mysql.connector
from bs4 import BeautifulSoup
import re
import requests
from time import sleep

def get_conn():
    host = '10.128.160.50'
    user = 'tddl_user'
    password = 'Tdl01'
    database = 'douban_spider'
    return mysql.connector.connect(host=host, user=user, password=password, database=database)

def get_tag(conn, tag):
    cursor = conn.cursor()
    cursor.execute('select * from movie_tag where tag_name = %s', [tag,])
    return cursor.fetchone()
    
def save_tag(conn, tag):
    cursor = conn.cursor()
    cursor.execute('insert into movie_tag (tag_name) values (%s)', [tag,])
    conn.commit()
    cursor.close()

def update_tag_complete(conn, tag):
    cursor = conn.cursor()
    cursor.execute('update movie_tag set complete = 1 where tag_name = %s', [tag,])
    conn.commit()
    cursor.close()
        
def check_movie(conn, movie):
    item_id = movie.get('id')
    cursor = conn.cursor()
    cursor.execute('select * from movie where item_id = %s', [item_id,])
    if cursor.fetchone():
        return True
    else:
        return False

def save_movie(conn, movie, tag):
    item_id = movie.get('id')
    image = movie.get('image')
    name = movie.get('name')
    info = movie.get('info')
    url = movie.get('url')
    rating = movie.get('rating')
    rating_numbers = movie.get('numbers')
    cursor = conn.cursor()
    cursor.execute('insert into movie (item_id, image, name, info, url, rating, rating_numbers, tags) values (%s, %s, %s, %s, %s, %s, %s, %s)', [item_id, image, name, info, url, rating, rating_numbers, tag])
    conn.commit()
    cursor.close()

def update_movie(conn, movie, tag):
    item_id = movie.get('id')
    cursor = conn.cursor()
    cursor.execute('update movie set tags = concat(tags, ";", %s) where item_id = %s', [tag, item_id])
    conn.commit()

def get_last_url(conn):
    cursor = conn.cursor()
    cursor.execute('select * from movie_access_log order by id desc limit 1')
    return cursor.fetchone()
    
def save_access_log(conn, url):
    cursor = conn.cursor()
    cursor.execute('insert into movie_access_log (url) values (%s)', [url,])
    conn.commit()
    cursor.close()
    
def save_failed_log(conn, url):
    cursor = conn.cursor()
    cursor.execute('insert into movie_failed_log (url) values (%s)', [url,])
    conn.commit()
    cursor.close()

def parse(html):
    item_list = []
    re_number = re.compile(r'(\d+)')
    soup = BeautifulSoup(html, 'html.parser')
    tr_list = soup.select('tr.item')
    if tr_list:
        for tr in tr_list:
            item = {}
            #image
            item['image'] = tr.img['src']
            #url
            item['url'] = tr.a['href']
            #id
            item['id'] = re.findall(re_number, item['url'])[0]
            #name
            item['name'] = tr.a['title']
            #info
            if tr.select('p.pl'):
                for s in tr.select('p.pl')[0].stripped_strings:
                    item['info'] = str(s)
            else:
                item['info'] = None
            #rating
            if tr.select('span.rating_nums'):
                for s in tr.select('span.rating_nums')[0].stripped_strings:
                    item['rating'] = str(s)
            else:
                item['rating'] = None
            #rating_number
            if tr.select('span.pl'):
                for s in tr.select('span.pl')[0].stripped_strings:
                        replace_str = re.findall(re_number, str(s))
                        if replace_str:
                            item['numbers'] = replace_str[0]
                        else:
                            item['numbers'] = None
            else:
                item['numbers'] = None
            ###
            print(item)
            item_list.append(item)
        return item_list
    else:
        return None

headers = {'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
           'Accept-Encoding': 'gzip, deflate, sdch, br',
           'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
           'Cache-Control': 'max-age=0',
           'Connection': 'keep-alive',
           'Host': 'movie.douban.com',
           'Referer': 'https://movie.douban.com/',
           'Upgrade-Insecure-Requests': '1',
           'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.87 Safari/537.36'
           }
cookies = dict(ll='108296',
               bid='7t0W4shL9aA',
               gr_user_id='65eccd43-3241-4dd2-87a8-3e91b6d1e695',
               __utma='30149280.1561403780.1463727120.1465800838.1466577421.6',
               __utmz='30149280.1466577421.6.2.utmcsr=baidu|utmccn=(organic)|utmcmd=organic',
               viewed='6880158_1023045_3259440',
               ct='y',
               ps='y',
               dgc132="150248076:/e12yUscd4w",
               ck='TRNi',
               ap='1',
               #_pk_ref.100001.3ac3='%5B%22%22%2C%22%22%2C1476239187%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl%3D8pgkT792CkwcLKwf1rQyZcYKA8vC93219-n0G4DUYWJ6RP4D8gfGjVGk3QHJsBXz6oZFGnkqeYbgiNLYuxZmR_%26wd%3D%26eqid%3De27e3644000ede7c0000000357884586%22%5D', 
               _vwo_uuid_v2='7C9D31570FD2B0754A12D23795A3BB6F|33cfbca2c10d6a2e429b06c1487557db; push_noty_num=0; push_doumail_num=0', 
               #_pk_id.100001.3ac3='a35da900e5b1ea95.1465971550.5.1476244344.1475994348'
               )
    
def run():
    conn = get_conn()
    #获取tag页
    tag_response = requests.get(url='https://movie.douban.com/tag/')
    #解析tag页
    tags = re.findall('<td><a href="/tag/(.*?)">', tag_response.text, re.S)
    #遍历所有的tag
    for tag in tags:
        is_history = False
        history_tag = get_tag(conn, tag)
        if history_tag:
            if history_tag[2] == 0:
                is_history = True
            else:
                continue
        else:
            save_tag(conn, tag)
        start = 0
        try_parse_times = 0
        while True:
            url = 'https://movie.douban.com/tag/' + tag + '?start=' + str(start)
            start = start + 20
            if is_history:
                last_access_url = get_last_url(conn)
                if url != last_access_url[1]:
                    continue
                else:
                    is_history = False
            #访问每个tag中的资源
            try_url_times = 0
            current_resource_failed = False
            while True:
                if try_url_times > 6:
                    current_resource_failed = True
                    break
                try_url_times = try_url_times + 1
                resource_response = requests.get(url=url)
                save_access_log(conn, url)
                if resource_response.status_code == 200:
                    break
                sleep(try_url_times)
            #如果该资源页访问失败，则记日志，并跳过这个资源页
            if current_resource_failed == True:
                #记录没有访问到的资源页URL
                save_failed_log(conn, url)
                break
            resource_html = resource_response.text
            #解析资源页，得到电影的集合
            movies = parse(resource_html)
            if movies:
                for movie in movies:
                    #检查是否有重复
                    if check_movie(conn, movie):
                        #更新tag
                        update_movie(conn, movie, tag)
                    else:
                        #入库
                        save_movie(conn, movie, tag)
            else:
                try_parse_times = try_parse_times + 1
                if try_parse_times > 3:
                    update_tag_complete(conn, tag)
                    break
            sleep(2)

if __name__ == '__main__':
    run()