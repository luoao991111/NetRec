from django.shortcuts import render
from .models import User_Static
from .models import User
from django.http import JsonResponse
from django.http import HttpResponse
from django.http import HttpResponseBadRequest
from django.http import HttpResponseNotAllowed


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
    }
    return JsonResponse(Ans)
