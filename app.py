#!/usr/bin/env 
# coding:utf-8


import requests
import os
import urlparse
from pyquery import PyQuery as pq


def load_app(url):
    r = requests.get(url)
    html = r.content
    str_dir = url.split('/')[-1] if url.split('/')[-1]!='' else url.split('/')[-2]

    #创建目录
    if not os.path.exists(str_dir):
        os.mkdir(str_dir)

    #创建首页
    str_file = '{0}/index.html'.format(str_dir)
    save_file(url,str_file)

    load_plugin(str_dir,url,html)



def load_plugin(str_dir,url,html):
    #解析
    v = pq(html)
    links = v('link')
    scripts = v('script')

    for link in links:
        l = v(link).attr('href')
        if l:
            remote_url = urlparse.urljoin(url,l)
            local_file_path = os.path.join(str_dir,l)
            save_file(remote_url,local_file_path)

    for script in scripts:
        l = v(script).attr('src')
        if l:
            remote_url = urlparse.urljoin(url,l)
            local_file_path = os.path.join(str_dir,l)
            save_file(remote_url,local_file_path)



def save_file(remote_url,local_file_path): 
    local_path = os.path.dirname(local_file_path)

    if not os.path.exists(local_path):
        os.makedirs(local_path)

    r = requests.get(remote_url)
    with open(local_file_path,'wb') as f:
        f.write(r.content)
 

if __name__ == '__main__':
    url = 'http://yx8.com/game/shizijunfangyuzhan/'
    load_app(url)
