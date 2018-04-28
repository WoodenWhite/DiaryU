# DiaryU
Backend code of WeChat Mini Program DiaryU.

## 使用步骤：
1. 需要安装的 Python 库：
    ```
    pip3 install django &&
    pip3 install jieba &&
    pip3 install requests &&
    pip3 install django-cors-headers
    ```
1. 在 /path/to/DiaryU/mysite/matching/ 下新建 secret_data.py，内容如下：
    ```
    appid = 'your_appid'
    secret = 'your_secret'
    ```
2. 开启测试服务器
    ```
    cd mysite &&
    python3 manage.py runserver + 端口号``
    ```
3. 在浏览器中访问``localhost:端口号/matching``进行测试

## 情感类型备注：

0. 毫无感情
1. 乐
2. 好
3. 怒
4. 哀
5. 惧
6. 恶
7. 惊

## 目前可用功能

### 存储日记、识别日记心情并进行用户匹配

请求类型：``POST``

访问``localhost:端口号/matching``，向``localhost:端口号/matching/emotion``提供表单
```
<input type="text" name="openid" />
<textarea name="diary" rows="10" cols="50"></textarea>
```
若用户已匹配，返回情感类型和匹配对象的openID，否则进行匹配，若匹配成功返回情感类型和新对象的相关信息，否则只返回情感类型。返回json格式样例：
```
// 保存成功，同时匹配成功
{
    "status": "success",
    "data": {
        "emotion": "1",
        "match": {
            "user": {
                "openid": "666",
                "nickName": "None",
                "avatarUrl": "None",
                "gender": "0",
                "province": "None",
                "city": "None",
                "country": "None"
            }
        }
    }
}

// 保存成功，但是匹配失败
{
    "status": "success",
    "data": {
        "emotion": "2"
    }
}
```  

### 解除某用户匹配关系

请求类型：``POST``

访问``localhost:端口号/matching/depair``, 向``localhost:端口号/matching/depair_action``提供表单
```
<input type="text" name="userid" />
```
解除该用户的匹配关系。返回json格式样例：
```
{
    "status": "success"
}
```

### 存储用户信息（用于登陆）

请求类型：``POST``

访问``localhost:端口号/matching/store``, 向``localhost:端口号/matching/store_action``提供表单，存储用户信息。表单内容为    
```
<input type="text" name="openId" />
<input type="text" name="nickName" />
<input type="text" name="avatarUrl" />
<input type="text" name="gender" />
<input type="text" name="province" />
<input type="text" name="city" /> 
<input type="text" name="country" />
```
返回json格式样例：
```
{
    "status": "success"
}
```

### 获取用户信息

请求类型：``GET``

访问``localhost:端口号/matching/get_user``,向``localhost:端口号/matching/get_user_action``发送表单
```
<input type="text" name="openId" />
```
返回用户的详细信息和近期至多十篇文章的简略信息，返回json格式样例为：
```
{
    "data": {
        "user": {
            "openid": "666",
            "nickName": "None", 
            "avatarUrl": "None", 
            "gender": 0, 
            "province": "None", 
            "city": "None", 
            "country": "None"
        },
        "diaries": {
            {
                "diary_id": "557",
                "content": "Lorem ipsum dolor sit amet."
                "emotion": "0", 
                "publish_date": "2018-04-23"
            },
            {
                "diary_id": "582",
                "title": "真的烦", 
                "emotion": "6", 
                "publish_date": "2018-04-24"
            }
        }
    }
}
```
注：此处第一篇日记没有标题，返回了内容的前 100 字。第二篇日记有标题，直接返回标题。

### 获取日记信息

请求类型：``GET``

访问``localhost:端口号/matching/get_diary``，向``localhost:端口号/matching/get_diary_action``发送表单
```
<input type="text" name="diaryID" />
```
返回详细日记内容。返回json格式样例：
```
{
    "data": {
        "diary": {
            "diary_id": "666",
            "title": "烦！",
            "content": "我真的好烦呀，这一天天过得毫无生气，像一潭死水。"
            "emotion": "6",
            "publish_date": "2018-04-24"
        }
    }
}
```

### 获取某用户全部日记

请求类型：``GET``

访问``localhost:端口号/matching/get_user_diary``,向``localhost:端口号/matching/get_diary_action``，发送表单
```
<input type="text" name="openId" />
```
返回对应用户的所有日记简略信息。返回json样式举例：
```
{
    "data": {
        "diaries": {
            {
                "diary_id": "557",
                "content": "Lorem ipsum dolor sit amet."
                "emotion": "0", 
                "publish_date": "2018-04-23"
            },
            {
                "diary_id": "582",
                "title": "真的烦", 
                "emotion": "6", 
                "publish_date": "2018-04-24"
            }
        }
    }
}
```
注：此处第一篇日记没有标题，返回了内容的前 100 字。第二篇日记有标题，直接返回标题。

### 修改日记

请求类型：``POST``

访问``localhost:端口号/matching/alt_diary``,向``localhost:端口号/matching/alt_diary_action``发送表单，
```
<input type="text" name="diaryId" />
<input type="text" name="title" />
<input type="text" name="content" />
```
存储修改后内容，并返回新的情感分析和匹配结果。返回json格式举例
```
{
    "status": "success",
    "data": {
        "emotion": "1",
        "match": {
            "user": {
                "openid": "666",
                "nickName": "None",
                "avatarUrl": "None",
                "gender": "0",
                "province": "None",
                "city": "None",
                "country": "None"
            }
        }
    }
}
```

### 获取用户的openId

请求类型：``GET``

访问``localhost:端口号/matching/get_openId``,向``localhost:端口号/matching/get_openId_action``发送表单
```
<input type="text" name="js_code" /> 
```
获取该用户的openID和session_key。返回json格式举例
```
// 从微信 API 处获取成功
{
    "data": {
        "openid": "OPENID",
        "session_key": "SESSIONKEY"
    }
}

// 从微信 API 处获取失败
{
    "data": {
        "errcode": "40029", 
        "errmsg": "invalid code" 
    }
}
```