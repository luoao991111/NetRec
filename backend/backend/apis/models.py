from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(unique=True, db_index=True, max_length=200)
    password = models.CharField(max_length=50)
    userid = models.IntegerField(db_index=True)
    level = models.IntegerField(db_index=False)
    Signature = models.CharField(max_length=500)
    follows = models.IntegerField(db_index=False)
    follower = models.IntegerField(db_index=False)
    song_cnt = models.IntegerField(db_index=False)


class Song(models.Model):
    songid = models.IntegerField(db_index=True)
    name = models.CharField(max_length=128)
    singer = models.CharField(max_length=128)
    collection = models.CharField(max_length=128)
    Coverurl = models.CharField(max_length=500)
    Songurl = models.CharField(max_length=500)


class Lyric(models.Model):
    songid = models.IntegerField(db_index=True)
    lyr = models.CharField(max_length=1200)


class Record(models.Model):
    userid = models.IntegerField(db_index=True)
    songid = models.IntegerField(db_index=True)
    Percentage = models.FloatField()

    class Meta:
        ordering = ['-Percentage']
