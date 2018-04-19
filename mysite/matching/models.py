from django.db import models

# Create your models here.


class User(models.Model):
    openID = models.CharField(max_length=100)  # 微信用户openId
    sex = models.IntegerField(default=0)  # 用户性别
    pair_status = models.BooleanField()  # 连接状态，判断当前用户是否有匹配对象
    session_key = models.CharField(max_length=100)  # 用户的session_key,用于对加密信息的解密


class Diary(models.Model):
    diary_id = models.IntegerField(default=0)  # 日记编号
    content = models.CharField(max_length=10000)  # 日记内容，限制字数为10000
    emotion = models.IntegerField(default=0)  # 日记主要情感，用整数代替情感名
    pub_date = models.DateTimeField('date published')
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Pairing(models.Model):
    pair_id = models.IntegerField(default=0)  # 配对编号
    user_one = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user1')  # 用户1的openId
    user_two = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='user2')  # 用户2的openId
