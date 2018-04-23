# DiaryU
Server's code of little program DiaryU.

### 使用步骤：
1. 需要安装django：``pip3 install django``
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
1. 访问``localhost:端口号/matching``，向``localhost:端口号/matching/emotion``提供表单 ``<input type="text" name="openid" />`` 和``<textarea name="diary" rows="10" cols="50"></textarea>``，若用户已匹配，返回情感类型和匹配对象的openID，否则进行匹配，若匹配成功返回情感类型和新对象的openID，否则返回情感类型和’000000‘
2. 访问``localhost:端口号/matching/depair``, 向``localhost:端口号/matching/depair_action``提供表单``<input type="text" name="userid" />``,解除该用户的匹配关系。