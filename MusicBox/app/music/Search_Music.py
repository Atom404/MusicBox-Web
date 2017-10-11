#!/usr/bin/env python
#coding=utf-8

import KuGou_Music as KG
import QQ_Music as QQ
import json

count = 0

def append_song(res,song_list):
    global count
    if 'error' not in res:
        for k,v in res.items():
            count += 1
            song = dict()
            song['songid'] = count
            song['songname'] = k
            song['singername'] = v['singername']
            imgres = KG.search_mes(v['singername'].encode('utf-8'),1,1)
            if 'error' not in imgres:
                for i,j in imgres.items():
                    song['img'] = j['imgurl']
                    if 'default_singer' in j['imgurl'] or 'default' in j['imgurl'] or j['imgurl'] == "":
                        song['img'] = '/static/app/img/default.png'
            else:
                song['img'] = '/static/app/img/default.png'
            song['url'] = v['url']
            song_list['songmes'].append(song)
            song_list['num'] = count

def search_music(keyword,page_size = 10,page = 1):
    global count
    song_list = dict()
    song_list['name'] = 'search_songlist'
    song_list['num'] = count
    song_list['songmes'] = list()
    
    res = QQ.search_mes(keyword,page_size,page)
    append_song(res,song_list)
    
    res = KG.search_mes(keyword,page_size,page)
    append_song(res,song_list)
    
    js = json.dumps(song_list)
    count = 0
    return js





