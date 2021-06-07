import time
import datetime
import hashlib
from django.shortcuts import render
from .models import User, Song, user_token
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed
from .models import Record, Lyric
from django.views.decorators.csrf import csrf_exempt
from .utils.Recom import Recomend_fun


# Create your views here.

def User_Info(request):
    Data = request.GET
    if not Data:
        return HttpResponseBadRequest("No Data")
    if 'username' not in Data and 'userid' not in Data:
        return HttpResponseBadRequest('No Data')

    if 'username' in Data:
        username = Data['username']
        user = User.objects.filter(username=username)
        if len(user) == 0:
            return HttpResponseBadRequest("No Such User")
        else:
            user = user[0]

    else:
        try:
            userid = int(Data['userid'])
        except ValueError as e:
            return HttpResponseNotAllowed("Not int Id")

        user = User.objects.filter(userid=userid)
        if len(user) == 0:
            return HttpResponseBadRequest("No Such User")
        else:
            user = user[0]

    Ans = {
        'username': user.username,
        'userid': user.userid,
        'level': user.level,
        'signature': user.Signature,
        'songcount': user.song_cnt,
        'follows': user.follows,
        'follower': user.follower,
        'backgroundurl': user.backgroundurl,
        'avatarurl': user.avatarurl
    }
    return JsonResponse(Ans)


def Song_Info(request):
    Data = request.GET
    if not Data or 'songid' not in Data:
        return HttpResponseBadRequest("No Data")

    try:
        songid = int(Data['songid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Id")
    song = Song.objects.filter(songid=songid)
    if len(song) == 0:
        return HttpResponseBadRequest("No Such Song")
    song = song[0]
    Ans = {
        'name': song.name,
        'singer': song.singer.split('@'),
        'collection': song.collection,
        'coverurl': song.Coverurl
    }
    return JsonResponse(Ans)


def Get_lyris(request):
    Data = request.GET
    if not Data or 'songid' not in Data:
        return HttpResponseBadRequest("No Data")

    try:
        songid = int(Data['songid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Id")

    song = Lyric.objects.filter(songid=songid)
    if len(song) == 0:
        Ans = {'lyrics': [""], 'time': 0}
    else:
        song = song[0]
        lyrs = song.lyr.strip()
        Time = 1 if lyrs[0] == '[' else 0
        if Time:
            lyrs = ['[' + x for x in lyrs.split('[')[1:]]
        else:
            lyrs = lyrs.split('\n')
        Ans = {'time': Time, 'lyrics': lyrs}

    return JsonResponse(Ans)


def Get_Record(request):
    Data = request.GET
    if not Data or 'userid' not in Data:
        return HttpResponseBadRequest("No Data")

    try:
        userid = int(Data['songid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Id")

    record = Record.objects.filter(userid=userid)
    Record_list = []
    for rec in record:
        Record_list.append({
            'songid': rec.songid,
            'percentage': rec.ercentage
        })

    return JsonResponse({'record': Record_list})


def generate_token(name, t):
    input = name + str(t) + str(datetime.datetime.now())
    token = hashlib.md5(input.encode('utf-8')).hexdigest()
    return token


@csrf_exempt
def Login(request):
    Data = request.POST
    if not Data or 'username' not in Data or 'password' not in Data:
        return HttpResponseBadRequest("No Data")
    username = Data['username']
    password = Data['password']
    user = User.objects.filter(username=username)
    if len(user) == 0:
        return HttpResponse("No Such User", status=401)
    user = user[0]
    if user.password == password:
        info = {}
        utoken = user_token.objects.filter(username=username)
        token = generate_token(username, int(time.time()))
        if len(utoken) == 0:
            user_token.objects.create(username=username, token=token)
        else:
            utoken[0].token = token
            utoken[0].save()
        info = {
            'userid': user.userid,
            'username': user.username,
            'token': token
        }
    else:
        return HttpResponse("Wrong Password", status=401)

    return JsonResponse(info)


def mainpage(request):
    Data = request.GET
    if not Data or 'userid' not in Data:
        return JsonResponse({'recommend': []})
    try:
        userid = int(Data['userid'])
    except ValueError as e:
        return HttpResponseNotAllowed("Not Int Id")

    songr = Record.objects.filter(userid=userid)
    if len(songr) == 0:
        return JsonResponse({'recommend': []})
    songlist = [{'songid': x.songid, 'score': x.Percentage} for x in songr]
    Rec_list = Recomend_fun(songlist, 100)
    """
    for lin in Rec_list:
        print(lin)
    """
    Ans = [{'songid': x[0]} for x in Rec_list]
    for Idx in range(len(Ans)):
        Ans[Idx]['pre'] = Ans[Idx - 1]['songid'] if Idx != 0 else Ans[-1]['songid']
        Ans[Idx]['nex'] = Ans[Idx + 1]['songid'] if Idx != len(Ans) - 1 else Ans[0]['songid']

    return JsonResponse({'recommend': Ans})
