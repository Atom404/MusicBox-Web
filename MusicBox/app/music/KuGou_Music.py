#!/usr/bin/env python
#coding=utf-8

import urllib,urllib2
import json
from contextlib import closing 
from bs4 import BeautifulSoup

#keyword : 搜索关键词
#page_size : 每页返回的数量
#page : 页数

def search_mes(keyword,page = 1,page_size = 5):
    result = dict()
    string = urllib.quote(keyword)
    search_url = 'http://mobilecdn.kugou.com/api/v3/search/song?format=jsonp&\
keyword={0}&page={1}&pagesize={2}&showtype=1&\
callback=kgJSONP238513750'.format(string,page,page_size)
    
    try:
        with closing(urllib2.urlopen(search_url)) as f:
            page = f.read()
    except BaseException as e:
        result['error'] = 'No search result!'
        return result
    
    search_js = json.loads(page[17:-1])
    if not search_js['data']['info']:
        result['error'] = 'No search result!'
        return result
    
    for i in search_js['data']['info']:
        result[i['songname']] = dict()
        result[i['songname']]['singername'] = i['singername']
        play_url = 'http://m.kugou.com/app/i/getSongInfo.php?\
hash={0}&cmd=playInfo'.format(i['hash'])

        try:
            with closing(urllib2.urlopen(play_url)) as f:
                page = f.read()
        except BaseException as e:
            result[i['songname']]['error'] = 'No play url!'
            continue
        
        play_js = json.loads(page)
        result[i['songname']]['url'] = play_js['url']
        result[i['songname']]['imgurl'] = play_js['imgUrl'].format(size = 400)
        
    return result
