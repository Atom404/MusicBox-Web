"""
Definition of models.
"""

from django.db import models

class Song(models.Model):
    songname = models.CharField(max_length = 30)
    singername = models.CharField(max_length = 30)
    songlink = models.URLField()
    songimg = models.URLField()

    def __unicode__(self):
        return self.songname

class User(models.Model):
    username = models.EmailField()
    password = models.CharField(max_length = 100)
    imgurl = models.URLField(null=True,blank=True)
    likesong = models.ManyToManyField(Song,blank=True)

    def __unicode__(self):
        return self.username

class SimilarityMatrix(models.Model):
    songOne = models.ForeignKey(Song,related_name='songOne')
    songTwo = models.ForeignKey(Song,related_name='songTwo')
    value = models.FloatField()


