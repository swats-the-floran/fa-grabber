#!/usr/bin/env python

'''
This is a first version of anonimous furrafinity grabber.
You will need:
1. launched tor or address of your other proxy server
2. mozilla browser
3. solved capchas at furaffinity and cookies
4. python with requests and beautifulsoup4 libraries. to get the libraries you have to launch following commands in your shell from administrator
    pip install requests[socks]
    pip install beautifulsoup4

Configuring this script:
1. write path to your download directory
2. write path to your cookies directory

Using this script:
You can just launch this file and it will grab images from the last page of your submissions or use certain link as an argument like this:
    ./grabber.py https://www.furaffinity.net/gallery/kacey
'''

import sqlite3
import requests
import re
from os import path
from sys import argv
from http import cookiejar
from bs4 import BeautifulSoup


def get_cookies(cj, ff_cookies, filter):
    con = sqlite3.connect(ff_cookies)
    cur = con.cursor()
    cur.execute("SELECT host, path, isSecure, expiry, name, value FROM moz_cookies")
    for item in cur.fetchall():
        c = cookiejar.Cookie(0, item[4], item[5],
            None, False,
            item[0], item[0].startswith('.'), item[0].startswith('.'),
            item[1], False,
            item[2],
            item[3], item[3]=="",
            None, None, {})
        if c.domain.find(filter) != -1:
            cj.set_cookie(c)


# in future i want to add support of inkbunny and e621
base_url = 'https://furaffinity.net/'

# you need cookies for access through tor because by default you get capcha page
cookie_path = '/path/to/browser/cookies.sqlite'

# write address of directory where images should be downloaded
res_directory = '/home/user/Pictures/furaffinity/'

# User-agent is essentially important for getting page isntead of 403 error
headers = 'Mozilla/5.0 (X11; Linux x86_64; rv:61.0) Gecko/20100101 Firefox/61.0'

# without any given link it downloads the last page of your submissions. downloading the whole list of submissions and galleries is yet to be added
if len(argv) < 2:
    link72 = 'https://www.furaffinity.net/msg/submissions/old@72'
else:
    link72 = argv[1]

# you can set other proxies than just tor by replacing addresses and "socks5" to "http" and "https"
proxies = {"https": "socks5://127.0.0.1:9050", "http": "socks5://127.0.0.1:9050"}


# creating two sessions for fa and fa's cdn
sess = requests.Session()
cjar_fa = cookiejar.CookieJar()
get_cookies(cjar_fa, cookie_path, 'furaffinity')
sess.headers['User-Agent'] = headers
sess.cookies = cjar_fa

sess_cdn = requests.Session()
cjar_cdn = cookiejar.CookieJar()
get_cookies(cjar_cdn, cookie_path, 'facdn')
sess_cdn.headers['User-Agent'] = headers
sess_cdn.cookies = cjar_cdn

# open and parse start page
resp = sess.get(link72, proxies=proxies)
soup = BeautifulSoup(resp.text, 'lxml')

pattern = r'<a href="(.+?)">Download<\/a>'
quant_downloaded = 0

for timage in soup.find_all(class_ = 't-image'):
    page_link = timage.b.u.a['href']
    page = sess.get(base_url + page_link, proxies=proxies)
    image_link = re.search(pattern, page.text)
    if image_link != -1:
        file_name = re.search(r'.+\/(.+)', image_link[1])[1]
        pathtofile = path.join(res_directory + file_name)
        with open(pathtofile, 'wb') as file:
            cdn_resp = sess_cdn.get('https:' + image_link[1], proxies=proxies)
            file.write(cdn_resp.content)
            quant_downloaded += 1
            print('saved file ' + file_name)
print('total number of downloaded images: ' + str(quant_downloaded))
