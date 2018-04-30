# DiaryU
Backend code of WeChat Mini Program DiaryU.

## 使用步骤：
0. 需要安装的 Python 库：
    ```
    pip3 install django &&
    pip3 install jieba &&
    pip3 install requests &&
    pip3 install django-cors-headers &&
    pip3 install channels
    ```
    需要安装Redis，macOs下使用homebrew直接安装，Linux下在官网安装，网上教程很详细，安装完成后,macOs下使用命令:
    ```
    brew services start redis
    ```
    Linux下启动服务暂未测试，待添加，默认监听端口为6379，如出现错误请检查默认端口配置。
1. 在 /path/to/DiaryU/mysite/matching/ 下新建 secret_data.py，内容如下：
    ```
    appid = 'your_appid'
    secret = 'your_secret'
    ```
2. 开启测试服务器
    ```
    cd mysite &&
    python3 manage.py runserver + 端口号
    ```
3. 在浏览器中访问``localhost:端口号/matching``进行测试

## 情感类型备注：

| 代码 | 中文名 | 英文名 | 色彩 | 备注 |
| :-: | :-: | :-: | :-: | :-: |
| 0 | 静 | Peaceful | 紫黑 | 无情感 |
| 1 | 乐 | Happy | 绿 | 积极 |
| 2 | 好 | Satisfied | 绿 | 积极 |
| 3 | 怒 | Angry | 红 | 强烈 |
| 4 | 哀 | Sad | 蓝 | 消极 |
| 5 | 惧 | Worried | 蓝 | 消极 |
| 6 | 恶 | Disgusted | 红 | 强烈 |
| 7 | 惊 | Surprised | 红 | 强烈 |

## 目前可用功能

### 存储日记、识别日记心情并进行用户匹配

请求类型：``POST``

访问``localhost:端口号/matching``，向``localhost:端口号/matching/emotion``提供表单
```
<input type="text" name="openId" />
<input type="text" name="title" />
<textarea name="diary" rows="10" cols="50"></textarea>
```
若用户已匹配，返回情感类型和匹配对象的openId，否则进行匹配，若匹配成功返回情感类型和新对象的相关信息，否则只返回情感类型。返回json格式样例：
```
// 保存成功，同时匹配成功
{
    "status": "success",
    "data": {
        "emotion": "1",
        "match": {
            "user": {
                "openId": "666",
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
<!-- 
调用API:``localhost:端口号/matching/get_user_action/用户openId`` -->

访问``localhost:端口号/matching/get_user``,向``localhost:端口号/matching/get_user_action``发送请求
```
<input type="text" name="openId" />
```
返回用户的详细信息和近期至多十篇文章的简略信息，返回json格式样例为：
```
// 有配对时
{
    "data": {
        "user": {
            "openId": "666",
            "nickName": "None", 
            "avatarUrl": "None", 
            "gender": 0, 
            "province": "None", 
            "city": "None", 
            "country": "None"
        },
        "diaries": [
            {
                "diary_id": "557",
                "title": "Lorem ipsum dolor sit amet."
                "content": "Lorem ipsum dolor sit amet.",
                "emotion": "0", 
                "publish_date": "2018-04-23"
            },
            {
                "diary_id": "582",
                "title": "真的烦", 
                "content": "哇今天是真的烦",
                "emotion": "6", 
                "publish_date": "2018-04-24"
            }
        ],
        "match": {
            "user": {
                "openId": "666",
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

// 无配对时
{
    "data": {
        "user": {
            "openId": "666",
            "nickName": "None", 
            "avatarUrl": "None", 
            "gender": 0, 
            "province": "None", 
            "city": "None", 
            "country": "None"
        },
        "diaries": [
            {
                "diary_id": "557",
                "title": "Lorem ipsum dolor sit amet."
                "content": "Lorem ipsum dolor sit amet.",
                "emotion": "0", 
                "publish_date": "2018-04-23"
            },
            {
                "diary_id": "582",
                "title": "真的烦", 
                "content": "哇今天是真的烦",
                "emotion": "6", 
                "publish_date": "2018-04-24"
            }
        ]
    }
}
```
注：此处第一篇日记没有标题，返回了内容的前 100 字。第二篇日记有标题，直接返回标题。

### 获取日记信息

请求类型：``GET``

<!-- 调用API:``localhost:端口号/matching/get_diary_action/日记Id`` -->

访问``localhost:端口号/matching/get_diary``，向``localhost:端口号/matching/get_diary_action``发送GET请求
```
<input type="text" name="diaryId" />
```
返回详细日记内容。返回json格式样例：
```
{
    "data": {
        "diary": {
            "diary_id": "666",
            "title": "烦！",
            "content": "我真的好烦呀，这一天天过得毫无生气，像一潭死水。",
            "emotion": "6",
            "publish_date": "2018-04-24"
        }
    }
}
```

### 获取某用户全部日记

请求类型：``GET``

<!-- 调用API:``localhost:端口号/matching/get_user_diary_action/用户openId`` -->
访问``localhost:端口号/matching/get_user_diary``,向``localhost:端口号/matching/get_diary_action``，发送GET请求
```
<input type="text" name="openId" />
```
返回对应用户的所有日记简略信息。返回json样式举例：
```
{
    "data": {
        "diaries": [
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
        ]
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
    }
}
```
### 修改日记

请求类型：``GET``

访问``localhost:端口号/matching/delete_diary``,向``localhost:端口号/matching/delete_diary_action``发送表单，
```
<input type="text" name="diaryId" />
```
删除日记并返回删除结果。返回json格式举例
```
{
    "status": "success",
}
```

### 获取用户的openId

请求类型：``GET``

<!-- 调用API``localhost:端口号/matching/get_openId_action/用户js_code`` -->
访问``localhost:端口号/matching/get_openId``,向``localhost:端口号/matching/get_openId_action``发送GET请求
```
<input type="text" name="js_code" /> 
```
获取该用户的openId和session_key。返回json格式举例
```
// 从微信 API 处获取成功
{
    "data": {
        "openId": "openId",
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
## 聊天功能初步

### 功能简介

访问``localhost:端口号/matching/select_chat_room``,进入某个房间，在``localhost:端口号/matching/chat/房间号``进行聊天。处在同一个聊天室的人可以看到彼此发送的信息。

关于建立websocket连接的格式详见目录``/mysite/matching/templates/chat``下的两个文件
### 基本思路(部分实现)
用户配对成功之后，后台会存储这个配对的编号，当用户发送聊天请求时，返回该用户的配对号，前端根据配对号发送请求拉取历史消息，然后建立websocket连接，发送消息（包括openId），如果用户同时在线，即可互相交流，不在线的话，后台服务器存储用户聊天的每一句话，待另一方选择匹配项时拉取聊天记录。

### 获取用户房间号
请求类型：``GET``
访问``localhost:端口号/matching/get_pair``，输入用户id，向``localhost:端口号/matching/get_pair_action``发送GET请求:
```
    <input type="text" name="openId" />
```
返回用户所在的房间id。返回json格式示例如下：
```
{
    "data": {
        "pair_id": "1"
    }
}
```

### 获取房间的聊天记录

请求类型：``GET``

访问``localhost:端口号/matching/get_history`` ，输入房间号，向``localhost:端口号/matching/get_history_action`` 发送get请求:
```
    <input type="text" name="pair_id" />
```
返回该房间的所有聊天记录，返回json格式示例如下：
```
{
    "data": {
        "messages": [
            {
                "publish_date": "2018-04-29 12:46:41",
                "content": "123",
                "openId": "小猪佩奇1",
            }, 
            {
                "publish_date": "2018-04-29 12:46:56",
                "content": "hello",
                "openId": "小猪佩奇2",
            }, 
            {
                "publish_date": "2018-04-29 12:46:59",
                "content": "看得到嘛", 
                "openId": "小猪佩奇2"
            },
            {
                "publish_date": "2018-04-29 12:47:21",
                "content": "完全ojkb",
                "openId": "小猪佩奇1",
            }
        ]
    }
}
```
