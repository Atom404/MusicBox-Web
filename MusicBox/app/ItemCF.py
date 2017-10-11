#!/bin/usr/env python
#coding=utf-8

'''
input:
    train = {
        "U1": [ "I1","I2","I3"...],
        "U2": [ "I2","I4","I6"...],
        "U2": [ "I3","I5","I6"...],
        ...
    }
output:
    W[i][j]

'''
import math
import operator

import os,sys,django
sys.path.append(r'..\..\MusicBox')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "MusicBox.settings")
import MusicBox.settings
django.setup()
from app.models import *


def ItemSimilarity(train):
    N = dict()              #物品-用户数表
    C = dict()              #共现矩阵
    for u,items in train.items():
        for i in items:
            if i not in N:
                N[i] = 0
            N[i] += 1
            C[i] = dict()
            for j in items:
                if i == j:
                    continue
                if j not in C[i]:
                    C[i][j] = 0
                C[i][j] += 1 / math.log(1 + len(items) * 1.0)
                
    W = dict()
    for i,related_items in C.items():
        W[i] = dict()
        for j,cij in related_items.items():
            W[i][j] = cij /math.sqrt(N[i] * N[j])
            
    for i,related_items in W.items():               #归一化
        maxvalue = max(related_items.values())
        for j,wij in related_items.items():
            W[i][j] = W[i][j] / maxvalue
    return W

def GenerationMatrix():
    train = dict()
    users = User.objects.all()
    for i in users:
        train[i.id] = []
        for j in i.likesong.all():
            train[i.id].append(j.id)
    W = ItemSimilarity(train)
    for i,related_items in W.items():
        for j,wij in related_items.items():
            s = SimilarityMatrix.objects.get_or_create(songOne = Song.objects.get(id = i),\
                                                   songTwo = Song.objects.get(id = j),value = 0)
            s[0].value = wij
            s[0].save()

def Recommendation(user_id,K):
    rank =dict()
    W = dict()
    
    S = SimilarityMatrix.objects.all()
    for i in S:
        if i.songOne.id not in W:
            W[i.songOne.id] = dict()
        W[i.songOne.id][i.songTwo.id] = i.value
        
    u = User.objects.get(id = user_id)
    ru = []
    for i in u.likesong.all():
        ru.append(i.id)
    
    for i in ru:
        if i not in W:
            continue
        for j,wj in sorted(W[i].items(),\
                           key=operator.itemgetter(1),reverse=True)[0:K]:
            if j in ru:
                continue
            if j not in rank:
                rank[j] = 0
            rank[j] += wj
    return rank


if __name__ == '__main__':
    print 'Starting to generate the matrix...'
    GenerationMatrix()
    print 'Finished generating the matrix.'
    
