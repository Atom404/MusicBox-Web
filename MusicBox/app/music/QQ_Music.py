#!/usr/bin/env python
#coding=utf-8

import urllib,urllib2
import json
from contextlib import closing 
from bs4 import BeautifulSoup

#keyword : 搜索关键词
#page_size : 每页返回的数量
#page : 页数

def search_mes(keyword,page_size = 5,page = 1):
    result = dict()
    string = urllib.quote(keyword)
    search_url = 'http://s.music.qq.com/fcgi-bin/music_search_new_platform?t=0&n={0}\
&aggr=1&cr=1&loginUin={1}&format=json&inCharset=GB2312&outCharset=utf-8\
&notice=0&platform=jqminiframe.json&needNewCode=0&p={2}&catZhida=0\
&remoteplace=sizer.newclient.next_song&w={3}'.format(page_size,0,page,string)

    try:
        with closing(urllib2.urlopen(search_url)) as f:
            page = f.read()
    except BaseException as e:
        result['error'] = 'No search result!'
        return result

    js = json.loads(page)
    if not js['data']['song']['list']:
        result['error'] = 'No search result!'
        return result
    
    for i in js['data']['song']['list']:
        ids = i['f'].split('|')
        if len(ids) < 5:
            continue
        result[i['fsong']] = dict()
        result[i['fsong']]['singername'] = i['fsinger']
        songid = ids[0]
        imageid = ids[4]
        albumname = ids[5]
        result[i['fsong']]['album_name'] = albumname
        song_url = 'http://ws.stream.qqmusic.qq.com/{0}.m4a?fromtag=0'\
                   .format(songid)
        result[i['fsong']]['url'] = song_url
        lyricurl = "http://music.qq.com/miniportal/static/lyric/\
{sp_id}/{s_id}.xml".format(sp_id = int(songid)%100,s_id = songid)
        result[i['fsong']]['lrc_url'] = lyricurl
        imageurl = "http://imgcache.qq.com/music/photo/album_{width}/\
{ip_id}/{width}_albumpic_{i_id}_0.jpg".format(ip_id = int(imageid)%100,\
                                               i_id = imageid,width = 300)
        result[i['fsong']]['imgurl'] = imageurl
        
    return result

    
