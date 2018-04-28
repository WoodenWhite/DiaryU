# DiaryU
Server's code of little program DiaryU.

### 使用步骤：
1. 需要安装的 Python 库：
    ```
    pip3 install django &&
    pip3 install jieba &&
    pip3 install requests &&
    pip3 install django-cors-headers
    ```
1. ``git clone https://github.com/WoodenWhite/DiaryU.git``
2. 进入mysite文件夹，``python3 manage.py runserver + 端口号``
3. 访问``localhost:端口号/matching``进行配对
### 情感类型备注：

0. 毫无感情
1. 乐
2. 好
3. 怒
4. 哀
5. 惧
6. 恶
7. 惊

### 目前可用功能
1. 存储日记，识别日记心情并进行用户匹配：访问``localhost:端口号/matching``，向``localhost:端口号/matching/emotion``提供表单 ``<input type="text" name="openid" />`` 和``<textarea name="diary" rows="10" cols="50"></textarea>``，若用户已匹配，返回情感类型和匹配对象的openID，否则进行匹配，若匹配成功返回情感类型和新对象的openID，否则返回情感类型和’000000‘,返回json格式样例：``{"Emotiontype": "1","MatchingID": "1233241","nickName": "None","avatarUrl": "None","gender": "0","province": "None","city": "None","country": "None"}``
2. 解除某用户匹配关系：访问``localhost:端口号/matching/depair``, 向``localhost:端口号/matching/depair_action``提供表单``<input type="text" name="userid" />``,解除该用户的匹配关系。返回json格式样例：{"result:", "Successful"}
3. 存储用户信息（用于登陆）：访问``localhost:端口号/matching/store``, 向``localhost:端口号/matching/store_action``提供表单，存储用户信息。表单内容为    
    - ``<input type="text" name="openId" /> ``
    - ``<input type="text" name="nickName" />``
    - ``<input type="text" name="avatarUrl" />``
    - ``<input type="text" name="gender" />``
    - ``<input type="text" name="province" />`` 
    - ``<input type="text" name="city" /> ``
    - ``<input type="text" name="country" />``
    
    返回json格式样例：{"result:", "Successful"}
4. 获取用户信息：访问``localhost:端口号/matching/get_user``,向``localhost:端口号/matching/get_user_action``发送表单`` <input type="text" name="openId" />``,返回用户的详细信息和近期至多十篇文章的标题、情感、发布日期，返回json格式样例为：``{"nickName": "None", "avatarUrl": "None", "gender": 0, "province": "None", "city": "None", "country": "None", "diaries": [{"557": [null, 0, "2018-04-23"]}, {"582": ["真的烦", 6, "2018-04-24"]}]}``注：此处第一篇文章没有标题是测试数据，实际应用时所有文章均有标题。也就是传入标题或文章的至多前100个字。

5. 获取日记信息：访问``localhost:端口号/matching/get_diary``, 向``localhost:端口号/matching/get_diary_action``发送表单``<input type="text" name="diaryID" />``,返回日记内容，返回json格式样例：``{"content": "我真的好烦呀，这一天天过得毫无生气，像一潭死水。"}``

6. 获取某用户全部日记：访问``localhost:端口号/matching/get_user_diary``,向``localhost:端口号/matching/get_diary_action``，发送表单``<input type="text" name="openId" />``，返回对应用户的所有日记id、标题、心情、发布日期等信息。返回json样式举例：``[{"557": [null, 0, "2018-04-23"]}, {"582": ["真的烦", 6, "2018-04-24"]}]``
7. 修改日记：访问``localhost:端口号/matching/alt_diary``,向``localhost:端口号/matching/alt_diary_action``发送表单，``<input type="text" name="diaryId" /> <input type="text" name="title" /> <input type="text" name="content" />``,存储修改后内容，并返回新的情感分析和匹配结果。返回json格式举例``{"Emotiontype": "1","MatchingID": "1233241","nickName": "None","avatarUrl": "None","gender": "0","province": "None","city": "None","country": "None"}``
8. 获取用户的openId：访问``localhost:端口号/matching/get_openId``,向``localhost:端口号/matching/get_openId_action``发送表单，``<input type="text" name="js_code" /> ``,获取该用户的openID和session_key。返回json格式举例``{"openid": "OPENID","session_key": "SESSIONKEY", }``或``{ "errcode": 40029, "errmsg": "invalid code" }``