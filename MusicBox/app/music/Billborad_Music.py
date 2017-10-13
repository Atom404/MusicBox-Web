#!/usr/bin/env python
#coding=utf-8

import KuGou_Music as KG
import json
import random
import urllib,urllib2
import demjson
from contextlib import closing 


count = 0
new_billborad = 'http://music.qq.com/musicbox/shop/v3/data/hit/hit_newsong.js'
total_billborad = 'http://music.qq.com/musicbox/shop/v3/data/hit/hit_all.js'
song_url = 'http://ws.stream.qqmusic.qq.com/{0}.m4a?fromtag=0'

def billborad_qq(billborad_url,song_list):
    global count
    try:
        with closing(urllib2.urlopen(billborad_url)) as f:
            page = f.read()
        js = demjson.decode(page[13:-48].decode("gbk"))
    except BaseException as e :
        print e
        js = { 'error' : 'No billborad list'}

    if 'error' not in js:
        for i in range(20):
            index = random.randint(0,99)
            count += 1
            song = dict()
            song['songid'] = count
            song['songname'] = js['songlist'][index]['songName']
            song['singername'] = js['songlist'][index]['singerName']
            song['url'] = song_url.format(js['songlist'][index]['id'])
            imgres = KG.search_mes(js['songlist'][index]['songName'].encode('utf-8'),1,1)
            if 'error' not in imgres:
                for i,j in imgres.items():
                    song['img'] = j['imgurl']
                    if 'default_singer' in j['imgurl'] or 'default' in j['imgurl'] or j['imgurl'] == "":
                        song['img'] = '/static/app/img/default.png'
            else:
                song['img'] = '/static/app/img/default.png'
            song_list['songmes'].append(song)
            song_list['num'] = count

def billborad_music(billborad = 1):
    global count
    song_list = dict()
    song_list['name'] = 'billborad_songlist'
    song_list['num'] = count
    song_list['songmes'] = list()

    if billborad == 1:
        billborad_qq(new_billborad,song_list)
    elif billborad == 0:
        billborad_qq(total_billborad,song_list)

    js = json.dumps(song_list)
    count = 0
    return js
    

