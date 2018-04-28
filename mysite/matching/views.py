from django.shortcuts import render
from django.http import HttpResponse, Http404
from django.db import models
from django.db.models import Count, Min, Max, Sum
from django.db import models
from django.shortcuts import get_object_or_404, render
from django.utils.timezone import now, timedelta
from .models import User, Diary, Pairing, Word
from .utils import similityCos, pair
from . import utils, secret_data
import requests
import jieba
import json
import jieba.analyse as analyse
# Create your views here.
# coding = unicode



def index(request):
    return render(request, 'matching/index.html')
    # return HttpResponse("Test")


def emotion(request):
    userid = request.POST['openId']
    cont = request.POST['diary']  # 获取openid和日记文本
    title = request.POST['title']

    if title == '' or title == None:
        if len(cont) > 100:
            title = cont[0:100]
        else:
            title = cont
    # cont = title+cont
    words = Word.objects.all().values('word')

    for singleword in words:
        # 取出所有的候选词，并将他们在分词库中的比重加大，优先分词
        jieba.suggest_freq((singleword['word']), True)
    # 分词，标题加内容，lcut直接返回list
    cut = jieba.lcut(title + ' ' + cont, cut_all=False)

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

    # 这个逻辑应该用try exception实现，以后改,
    if User.objects.filter(openId=userid).count() != 0:
        try:
            obj = User.objects.get(openId=userid)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        if obj.pair_status == True:  # 如果已经配对，直接返回配对对象。
            userid_ret_obj = Pairing.objects.get(user_one=obj)
            userid_ret = userid_ret_obj.user_two
            userid_ret = userid_ret.openId
            obj = User.objects.get(openId=userid_ret)
        # rett = '{"Emotiontype": "' + \
        #     str(emoret)+'",'+'"MatchingID": "'+userid_ret+'"}'
            # 存储日记
            diary = Diary(content=cont, title=title, emotion=emoret,
                          user=User.objects.get(openId=userid),
                          strength0=emo_vec[0], strength1=emo_vec[1],
                          strength2=emo_vec[2], strength3=emo_vec[3],
                          strength4=emo_vec[4], strength5=emo_vec[5],
                          strength6=emo_vec[6], strength7=emo_vec[7]
                          )  # 存储为对应的情感向量值。
            diary.save()
            rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+str(obj.openId)+'",' + \
                '"nickName": "'+str(obj.nickName)+'",' + '"avatarUrl": "'+str(obj.avatarUrl)+'",'+'"gender": "' + \
                str(obj.gender)+'",' + '"province": "'+str(obj.province) + \
                '",' + '"city": "'+str(obj.city)+'",' + \
                '"country": "'+str(obj.country)+'"}'
            return HttpResponse(rett)

    enddate = now()
    startdate = enddate + timedelta(days=-2)  # 只取出近两天内发布的日记
    articles = Diary.objects.filter(pub_date__range=(startdate, enddate))
    # articles = Diary.objects.all()

    max_similarity = 0
    userid_ret = '000000'
    string0 = ''
    if emoret == 0:  # 如果向量为空，没什么感情，那就在没什么感情的人选最早发布日记的没感情的没匹配的人进行配对,避免他们一直匹不到
        for cursor in articles:
            if cursor.emotion == 0 and cursor.user.openId != userid and cursor.user.pair_status == False:
                userid_ret = cursor.user.openId
                break
    else:
        for cursor in articles:  # 否则对所有情感向量非零的人
            if cursor.emotion == 0 or cursor.user.openId == userid or cursor.user.pair_status == True:  # 暂时还不能实现有无人匹配
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
            if similarity > max_similarity:  # 同等条件选取先发日记的人
                max_similarity = similarity
                userid_ret = cursor.user.openId

    # 如果数据库中没有这个人，存储，然后根据是否找到匹配对象进行操作 update:其实按照系统逻辑这里已经一定能够找到匹配对象了
    if User.objects.filter(openId=userid).count() == 0:
        if userid_ret == '000000':
            obj = User(openId=userid, pair_status=False)
            obj.save()
        else:
            obj = User(openId=userid, pair_status=True)
            obj.save()
            obj0 = User.objects.get(openId=userid_ret)
            pair(obj, obj0)

    elif userid_ret != '000000':  # 否则如果找到某个人了，将这两个人的配对状态变为True,并在pair表中插入他们的配对状态
        try:
            # 这里应该不需要exception了,但为了保险起见还是写一下
            obj = User.objects.get(openId=userid)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        obj.pair_status = True
        try:
            obj0 = User.objects.get(openId=userid_ret)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        obj0.pair_status = True
        obj0.save()
        obj.save()
        pair(obj, obj0)
        # 存储日记
    diary = Diary(content=cont, title=title, emotion=emoret,
                  user=User.objects.get(openId=userid),
                  strength0=emo_vec[0], strength1=emo_vec[1],
                  strength2=emo_vec[2], strength3=emo_vec[3],
                  strength4=emo_vec[4], strength5=emo_vec[5],
                  strength6=emo_vec[6], strength7=emo_vec[7]
                  )  # 存储为对应的情感向量值。
    diary.save()
    # rett = userid + " : " + cont + '<br> 分词结果：' + \
    #     ','.join(cut) + '<br> 情感类型：' + str(emoret) + \
    #     '<br> 情感强度：' + str(emo_vec[emoret]) + \
    #     '<br>匹配用户的openID: ' + userid_ret
    # rett = '{"a": "Hello", "b": "World"}'
    if userid_ret != '000000':
        obj = User.objects.get(openId=userid_ret)
        # rett = '{"Emotiontype": "' + \
        #     str(emoret)+'",'+'"MatchingID": "'+userid_ret+'"}'
        rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+str(obj.openId)+'",' + \
            '"nickName": "'+str(obj.nickName)+'",' + '"avatarUrl": "'+str(obj.avatarUrl)+'",'+'"gender": "' + \
            str(obj.gender)+'",' + '"province": "'+str(obj.province) + \
            '",' + '"city": "'+str(obj.city)+'",' + \
            '"country": "'+str(obj.country)+'"}'
    else:
        rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+'000000'+'",' + \
            '"nickName": "'+'000000'+'",' + '"avatarUrl": "'+'000000'+'",'+'"gender": "' + \
            '000000'+'",' + '"province": "'+'000000' + \
            '",' + '"city": "'+'000000'+'",' + '"country": "'+'000000'+'"}'
    return HttpResponse(rett)  # 返回的userid如果为000000则为无匹配人选


def depair(request):  # 解除关系
    return render(request, 'matching/depair.html')


def depair_action(request):  # 一方解除关系后，另一方需要接受提示？待实现
    userid = request.POST['openId']

    if User.objects.filter(openId=userid, pair_status=True).count() == 0:
        ret = '{"result:", "Failed"}'
    else:
        x = User.objects.get(openId=userid)
        utils.depair(x)
        ret = '{"result:", "Successful"}'
    return HttpResponse(ret)


def store(request):
    return render(request, 'matching/store.html')


def store_action(request):
    openId = request.POST['openId']
    nickName = request.POST['nickName']
    avatarUrl = request.POST['avatarUrl']
    gender = request.POST['gender']
    province = request.POST['province']
    city = request.POST['city']
    country = request.POST['country']

    if User.objects.filter(openId=openId).count() == 0:
        obj = User(
            openId=openId, nickName=nickName, avatarUrl=avatarUrl, gender=gender, province=province, city=city, country=country)
        obj.save()  # 应该要try exception
    ret = '{"result:", "Successful"}'
    return HttpResponse(ret)
    # def get_user(request):
    #     return render(request, 'matching/get_user.html')


def get_openId(request):
    return render(request, 'matching/get_openId.html')


def get_openId_action(request):
    # appid = request.POST['appid']
    # secret = request.POST['secret']
    appid = secret_data.appid
    secret = secret_data.secret
    js_code = request.POST['js_code']
    # grant_type = request.POST['grant_type']
    r = requests.get(
        'https://api.weixin.qq.com/sns/jscode2session?appid='+appid+'&secret='+secret+'&js_code='+js_code+'&grant_type=authorization_code')
    # result = json.loads(r)
    return HttpResponse(r)


def get_user(request):  # 获取用户信息
    return render(request, 'matching/get_user.html')


def get_user_action(request):
    openId = request.POST['openId']
    try:
        obj = User.objects.get(openId=openId)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    diaries = Diary.objects.filter(user=obj)
    cnt = 0
    # rett = '{"nickName": "'+str(obj.nickName)+'", ' + '"avatarUrl": "'+str(obj.avatarUrl)+'", '+'"gender": "' + \
    #     str(obj.gender)+'", ' + '"province": "'+str(obj.province) + \
    #     '", ' + '"city": "'+str(obj.city)+'", ' + \
    #     '"country": "'+str(obj.country)+'", "diaries": ['
    rett = {
        'nickName': str(obj.nickName),
        'avatarUrl': str(obj.avatarUrl),
        'gender': obj.gender,
        'province': str(obj.province),
        'city': str(obj.city),
        'country': str(obj.country),
        'diaries': [],
    }

    cnt = 0
    for diary in diaries:
        if cnt < 10:
            cnt += 1
            rett['diaries'].append({diary.id: [diary.title,
                                               diary.emotion, str(diary.pub_date)[0:10]]})
        else:
            break
    return HttpResponse(json.dumps(rett, ensure_ascii=False))


def get_diary(request):  # 获取日记内容
    return render(request, 'matching/get_diary.html')


def get_diary_action(request):
    diaryid = request.POST['diaryId']
    try:
        obj = Diary.objects.get(id=diaryid)
    except Diary.DoesNotExist:
        raise Http404("Diary does not exist")
    ret = {
        'content': obj.content, }
    return HttpResponse(json.dumps(ret, ensure_ascii=False))


def get_user_diary(request):  # 找到用户的日记
    return render(request, 'matching/get_user_diary.html')


def get_user_diary_action(request):
    userid = request.POST['openId']
    try:
        obj = User.objects.get(openId=userid)
    except User.DoesNotExist:
        raise Http404("User does not exist")
    diaries = Diary.objects.filter(user=obj)
    rett = []
    for diary in diaries:
        rett.append({diary.id: [diary.title,
                                diary.emotion, str(diary.pub_date)[0:10]]})
    return HttpResponse(json.dumps(rett, ensure_ascii=False))


def alt_diary(request):
    return render(request, 'matching/alt_diary.html')


def alt_diary_action(request):
    diaryid = request.POST['diaryId']
    cont = request.POST['content']
    title = request.POST['title']
    if title == '' or title == None:
        if len(cont) > 100:
            title = cont[0:100]
        else:
            title = cont

    try:
        altered = Diary.objects.get(id=diaryid)
    except Diary.DoesNotExist:
        raise Http404("Diary does not exist")

    altered.content = cont
    altered.title = title

    # 重新进行情感分析
    words = Word.objects.all().values('word')
    for singleword in words:
        # 取出所有的候选词，并将他们在分词库中的比重加大，优先分词
        jieba.suggest_freq((singleword['word']), True)
    # 分词，标题加内容，lcut直接返回list
    cut = jieba.lcut(title + ' ' + cont, cut_all=False)

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

    # 存储心情
    altered.emotion = emoret
    altered.strength0 = emo_vec[0]
    altered.strength1 = emo_vec[1]
    altered.strength2 = emo_vec[2]
    altered.strength3 = emo_vec[3]
    altered.strength4 = emo_vec[4]
    altered.strength5 = emo_vec[5]
    altered.strength6 = emo_vec[6]
    altered.strength7 = emo_vec[7]

    altered.save()
    # 直接复用之前的代码
    userid = altered.user.openId
    if User.objects.filter(openId=userid).count() != 0:
        try:
            obj = User.objects.get(openId=userid)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        if obj.pair_status == True:  # 如果已经配对，直接返回配对对象。
            userid_ret_obj = Pairing.objects.get(user_one=obj)
            userid_ret = userid_ret_obj.user_two
            userid_ret = userid_ret.openId
            obj = User.objects.get(openId=userid_ret)
        # rett = '{"Emotiontype": "' + \
        #     str(emoret)+'",'+'"MatchingID": "'+userid_ret+'"}'
            rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+str(obj.openId)+'",' + \
                '"nickName": "'+str(obj.nickName)+'",' + '"avatarUrl": "'+str(obj.avatarUrl)+'",'+'"gender": "' + \
                str(obj.gender)+'",' + '"province": "'+str(obj.province) + \
                '",' + '"city": "'+str(obj.city)+'",' + \
                '"country": "'+str(obj.country)+'"}'
            return HttpResponse(rett)

    enddate = now()
    startdate = enddate + timedelta(days=-2)  # 只取出近两天内发布的日记
    articles = Diary.objects.filter(pub_date__range=(startdate, enddate))
    # articles = Diary.objects.all()

    max_similarity = 0
    userid_ret = '000000'
    string0 = ''
    if emoret == 0:  # 如果向量为空，没什么感情，那就在没什么感情的人选最早发布日记的没感情的没匹配的人进行配对,避免他们一直匹不到
        for cursor in articles:
            if cursor.emotion == 0 and cursor.user.openId != userid and cursor.user.pair_status == False:
                userid_ret = cursor.user.openId
                break
    else:
        for cursor in articles:  # 否则对所有情感向量非零的人
            if cursor.emotion == 0 or cursor.user.openId == userid or cursor.user.pair_status == True:  # 暂时还不能实现有无人匹配
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
            if similarity > max_similarity:  # 同等条件选取先发日记的人
                max_similarity = similarity
                userid_ret = cursor.user.openId

    # 如果数据库中没有这个人，存储，然后根据是否找到匹配对象进行操作 update:其实按照系统逻辑这里已经一定能够找到匹配对象了
    if User.objects.filter(openId=userid).count() == 0:
        if userid_ret == '000000':
            obj = User(openId=userid, pair_status=False)
            obj.save()
        else:
            obj = User(openId=userid, pair_status=True)
            obj.save()
            obj0 = User.objects.get(openId=userid_ret)
            pair(obj, obj0)

    elif userid_ret != '000000':  # 否则如果找到某个人了，将这两个人的配对状态变为True,并在pair表中插入他们的配对状态
        try:
            # 这里应该不需要exception了,但为了保险起见还是写一下
            obj = User.objects.get(openId=userid)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        obj.pair_status = True
        try:
            obj0 = User.objects.get(openId=userid_ret)
        except User.DoesNotExist:
            raise Http404("User does not exist")
        obj0.pair_status = True
        obj0.save()
        obj.save()
        pair(obj, obj0)

    if userid_ret != '000000':
        obj = User.objects.get(openId=userid_ret)
        # rett = '{"Emotiontype": "' + \
        #     str(emoret)+'",'+'"MatchingID": "'+userid_ret+'"}'
        rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+str(obj.openId)+'",' + \
            '"nickName": "'+str(obj.nickName)+'",' + '"avatarUrl": "'+str(obj.avatarUrl)+'",'+'"gender": "' + \
            str(obj.gender)+'",' + '"province": "'+str(obj.province) + \
            '",' + '"city": "'+str(obj.city)+'",' + \
            '"country": "'+str(obj.country)+'"}'
    else:
        rett = '{"Emotiontype": "'+str(emoret)+'",' + '"MatchingID": "'+'000000'+'",' + \
            '"nickName": "'+'000000'+'",' + '"avatarUrl": "'+'000000'+'",'+'"gender": "' + \
            '000000'+'",' + '"province": "'+'000000' + \
            '",' + '"city": "'+'000000'+'",' + '"country": "'+'000000'+'"}'
    return HttpResponse(rett)  # 返回的userid如果为000000则为无匹配人选
