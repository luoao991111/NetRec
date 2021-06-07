from django.db import models

# Create your models here.


class User(models.Model):
    username = models.CharField(unique=True, db_index=True, max_length=200)
    password = models.CharField(max_length=50)
    userid = models.BigIntegerField(db_index=True)
    level = models.IntegerField(db_index=False)
    Signature = models.CharField(max_length=500)
    follows = models.IntegerField(db_index=False)
    follower = models.IntegerField(db_index=False)
    song_cnt = models.IntegerField(db_index=False)
    backgroundurl = models.CharField(max_length=250)
    avatarurl = models.CharField(max_length=250)
    choices = ((0, '保密'), (1, '男'), (2, '女'))
    gender = models.IntegerField(db_index=True, choices=choices)


class Song(models.Model):
    songid = models.BigIntegerField(db_index=True)
    name = models.CharField(max_length=500)
    singer = models.CharField(max_length=1500)
    collection = models.CharField(max_length=500)
    Coverurl = models.CharField(max_length=500)


class Lyric(models.Model):
    songid = models.BigIntegerField(db_index=True)
    lyr = models.TextField(max_length=52000)


class Record(models.Model):
    userid = models.BigIntegerField(db_index=True)
    songid = models.BigIntegerField(db_index=True)
    Percentage = models.FloatField()

    class Meta:
        ordering = ['-Percentage']


class user_token(models.Model):
    token = models.CharField(max_length=521)
    username = models.CharField(db_index=True, max_length=200)
