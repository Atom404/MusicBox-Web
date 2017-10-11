"""
Definition of views.
"""

from django.shortcuts import render
from django.http import HttpRequest
from django.template import RequestContext
from datetime import datetime
from django.http.response import HttpResponse, HttpResponseBadRequest

from app.models import *
import music.Search_Music as SM 
import music.Billborad_Music as BM
from app.ItemCF import Recommendation
import json


def mainpage(request):
    if request.method == 'GET':
        return render(request,'app/mainpage.html')
    else:
        return HttpResponseBadRequest('wrong method!')

def search_info(request):
    if request.method == 'GET':
        key = request.GET.get('keyword','')
        size = int(request.GET.get('size',10))
        page = int(request.GET.get('page',1))
        if key == "":
            content = '{ "name" : "search_songlist","num" : 0,"songmes" : []} '
        else:
            content = SM.search_music(key.encode('utf-8'),size,page)
        return HttpResponse(content,content_type = 'application/json')
    else:
        return HttpResponseBadRequest('wrong method!')

def get_info(request):
    if request.method == 'GET':
        key = int(request.GET.get('key',1))
        content = BM.billborad_music(key)
        return HttpResponse(content,content_type = 'application/json')
    else:
        return HttpResponseBadRequest('wrong method!')

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        userpass = request.POST.get('userpass','')
        user = User.objects.filter(username = username,password = userpass)
        if user:
            usermes = dict()
            usermes['name'] = 'usermes'
            usermes['userid'] = user[0].id
            usermes['username'] = user[0].username
            if not user[0].imgurl:
                usermes['userimg'] = '/static/app/img/c.jpg'
            else:
                usermes['userimg'] = user[0].imgurl
            usermes['usermotto'] = 'To be,or not to be.'
            content = json.dumps(usermes)
            return HttpResponse(content,content_type = 'application/json')
        else:
            return HttpResponse('incorrect')
    else:
        return HttpResponseBadRequest('wrong method!')


def regist(request):
    if request.method == 'POST':
        username = request.POST.get('username','')
        userpass = request.POST.get('userpass','')
        if User.objects.filter(username = username):
            return HttpResponse('incorrect')
        else:
            User.objects.create(username = username,password = userpass)
            return HttpResponse('correct')
    else:
        return HttpResponseBadRequest('wrong method!')

def imgset(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        username = req['username']
        imgurl = req['imgurl']
        user = User.objects.get(username = username)
        user.imgurl = imgurl
        user.save()
        return HttpResponse('correct')
    else:
        return HttpResponseBadRequest('wrong method!')

def like(request):
    if request.method == 'POST':
        req = json.loads(request.body)
        songname = req['songmes'].split('_')[0]
        singername = req['songmes'].split('_')[1]
        if not Song.objects.filter(songname = songname) :
            s = Song.objects.create(songname = songname,singername = singername,\
                songlink = req['songurl'],songimg = req['imgurl'])
        else:
            s = Song.objects.get(songname = songname)
        p = User.objects.get(username = req['username'])
        p.likesong.add(s)
        return HttpResponse('correct')
    else:
        return HttpResponseBadRequest('wrong method!')

def recommend(request):
    if request.method == 'GET':
        username = request.GET.get('username','')
        u = User.objects.get(username = username)
        rank = Recommendation(u.id,10)
        rec = dict()
        rec['name'] = 'RecommendMusic'
        rec['num'] = len(rank)
        rec['songmes'] = list()
        for i,j in rank.items():
            s = Song.objects.get(id = i)
            song = dict()
            song['songid'] = s.id
            song['songname'] = s.songname
            song['singername'] = s.singername
            song['img'] = s.songimg
            song['url'] = s.songlink
            rec['songmes'].append(song)
        content = json.dumps(rec)
        return HttpResponse(content,content_type = 'application/json')
    else:
        return HttpResponseBadRequest('wrong method!')

'''
def home(request):
    """Renders the home page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/index.html',
        {
            'title':'Home Page',
            'year':datetime.now().year,
        }
    )

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        }
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        }
    )
'''