from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import User, Diary, Pairing
from django.db.models import Count, Min, Max, Sum
from django.db import models
import jieba
import jieba.analyse as analyse
# Create your views here.


def index(request):
    return render(request, 'matching/index.html')
    # return HttpResponse("Test")


def emotion(request):
    userid = request.POST['openid']
    cont = request.POST['diary']  # 获取openid和日记文本
    emo = analyse.extract_tags(cont, 50, withWeight=False)  # 提取关键词（暂时未实现）
    if User.objects.filter(openID=userid).count() == 0:  # 如果数据库中没有这个人，存储
        obj = User(openID=userid, pair_status=False)
        obj.save()
    diary = Diary(content=cont, emotion=0,
                  user=User.objects.get(openID=userid))  # 存储日记，暂时所有情感都为0
    diary.save()
    return HttpResponse(userid + ":" + cont)
