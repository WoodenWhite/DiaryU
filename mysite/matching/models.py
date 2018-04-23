from django.db import models

# Create your models here.


class User(models.Model):
    openID = models.CharField(max_length=100)  # 微信用户openId
    sex = models.IntegerField(
        default=0, choices=[(x, str(x)) for x in range(0, 2)], null=True)  # 用户性别
    pair_status = models.BooleanField(default=False)  # 连接状态，判断当前用户是否有匹配对象
    session_key = models.CharField(
        max_length=100, null=True)  # 用户的session_key,用于对加密信息的解密


class Diary(models.Model):
    title = models.CharField(max_length=10000, null=True)  # 日记标题
    content = models.CharField(max_length=10000)  # 日记内容，限制字数为10000
    # 日记主要情感，用整数代替情感名
    emotion = models.IntegerField(
        default=0, choices=[(x, str(x)) for x in range(0, 8)])
    pub_date = models.DateTimeField(auto_now_add=True)  # 发布日期第一次更新，其余时候不更新
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # 外键，日记用户
    strength0 = models.IntegerField(default=0)
    strength1 = models.IntegerField(default=0)
    strength2 = models.IntegerField(default=0)
    strength3 = models.IntegerField(default=0)
    strength4 = models.IntegerField(default=0)
    strength5 = models.IntegerField(default=0)
    strength6 = models.IntegerField(default=0)
    strength7 = models.IntegerField(default=0)


class Pairing(models.Model):
    user_one = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user1')  # 用户1的openId
    user_two = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user2')  # 用户2的openId


class Word(models.Model):
    word = models.CharField(max_length=100)
    emotionty = models.IntegerField(
        default=0, choices=[(x, str(x)) for x in range(0, 8)])
    strength = models.IntegerField(default=0)
