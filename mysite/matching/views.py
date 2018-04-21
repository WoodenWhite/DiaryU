from django.shortcuts import render
from django.http import HttpResponse
from django.db import models
from .models import User, Diary, Pairing, Word
from django.db.models import Count, Min, Max, Sum
from django.db import models
from django.shortcuts import get_object_or_404, render
import jieba
from .utils import similityCos
from . import utils
import jieba.analyse as analyse
# Create your views here.


def index(request):
    return render(request, 'matching/index.html')
    # return HttpResponse("Test")


def emotion(request):
    userid = request.POST['openid']
    cont = request.POST['diary']  # 获取openid和日记文本

    words = Word.objects.all().values('word')

    for singleword in words:
        # 取出所有的候选词，并将他们在分词库中的比重加大，优先分词
        jieba.suggest_freq((singleword['word']), True)
    cut = jieba.lcut(cont, cut_all=False)  # 分词，lcut直接返回list

    emo_vec = [0, 0, 0, 0, 0, 0, 0, 0]  # 情感向量

    for singleword in cut:  # 对于每一个分词，查找他们在数据库中是否存在，若存在则将相应的情感向量增加相应比重
        cursor = Word.objects.filter(word=singleword)
        if cursor.count() != 0:
            dim = cursor.values('emotionty')
            strg = cursor.values('strength')
            emo_vec[dim[0]['emotionty']] += strg[0]['strength']
        else:
            continue

    emoret = 0
    max0 = 0
    for emo in emo_vec:  # 判断属于哪种情感,如果有相同的返回第一种，如果值全部为0，说明这个人没什么心情，返回0代表没什么心情。
        if emo > max0:
            max0 = emo
            emoret = emo_vec.index(emo)

    # if User.objects.filter(openID=userid).count() != 0:  # 这个逻辑应该用try exception实现，以后改
    #     obj = User.objects.get(openID=userid)
    #     if obj.pair_status == True:

    articles = Diary.objects.all()
    max_similarity = 0
    userid_ret = '000000'
    string0 = ''
    if emoret == 0:  # 如果向量为空，没什么感情，那就在没什么感情的人里边随便选一个配
        for cursor in articles:
            if cursor.emotion != 0 and cursor.user.openID != userid and cursor.user.pair_status != True:
                userid_ret = cursor.user.openID
    else:
        for cursor in articles:  # 否则对所有情感向量非零的人
            if cursor.emotion == 0 or cursor.user.openID == userid or cursor.user.pair_status == True:  # 暂时还不能实现有无人匹配
                continue
            # tmp = cursor.emotion
            tmp_emo_vec = [0, 0, 0, 0, 0, 0, 0, 0]
            tmp_emo_vec[0] = cursor.strength0
            tmp_emo_vec[1] = cursor.strength1
            tmp_emo_vec[2] = cursor.strength2
            tmp_emo_vec[3] = cursor.strength3
            tmp_emo_vec[4] = cursor.strength4
            tmp_emo_vec[5] = cursor.strength5
            tmp_emo_vec[6] = cursor.strength6
            tmp_emo_vec[7] = cursor.strength7
            try:
                similarity = similityCos(emo_vec, tmp_emo_vec)
            except ZeroDivisionError:  # 有些数据向量为零但情感类型不为0
                raise Http404("数据库错误")
            # string0 += str(similarity) + ','
            # print(similarity)
            if similarity > max_similarity:
                max_similarity = similarity
                userid_ret = cursor.user.openID

    # 如果数据库中没有这个人，存储，然后根据是否找到匹配对象进行操作
    if User.objects.filter(openID=userid).count() == 0:
        if userid_ret == '000000':
            obj = User(openID=userid, pair_status=False)
        else:
            obj = User(openID=userid, pair_status=True)
        obj.save()
        obj0 = User.objects.get(openID=userid_ret)
        pair(obj, obj0)

    elif userid_ret != '000000':  # 否则如果找到某个人了，将这两个人的配对状态变为True,并在pair表中插入他们的配对状态
        obj = User.objects.get(openID=userid)
        obj.pair_status = True
        obj.save()
        obj = User.objects.get(openID=userid_ret)
        obj.pair_status = True
        obj.save()
        pair(obj, obj0)

    diary = Diary(content=cont, emotion=emoret,
                  user=User.objects.get(openID=userid),
                  strength0=emo_vec[0], strength1=emo_vec[1],
                  strength2=emo_vec[2], strength3=emo_vec[3],
                  strength4=emo_vec[4], strength5=emo_vec[5],
                  strength6=emo_vec[6], strength7=emo_vec[7]
                  )  # 存储为对应的情感向量值。
    diary.save()
    rett = userid + " : " + cont + '<br> 分词结果：' + \
        ','.join(cut) + '<br> 情感类型：' + str(emoret) + \
        '<br> 情感强度：' + str(emo_vec[emoret]) + \
        '<br>匹配用户的openID: ' + userid_ret
    return HttpResponse(rett)  # 返回的userid如果为000000则为无匹配人选


def depair(request):  # 解除关系
    return render(request, 'matching/depair.html')


def depair_action(request):  # 一方解除关系后，另一方需要接受提示？待实现
    userid = request.POST['userid']
    x = User.objects.get(openID=userid)
    utils.depair(x)
    return HttpResponse("Successful depair!")
