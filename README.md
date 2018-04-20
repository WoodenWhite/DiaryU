# DiaryU
Server's code of little program DiaryU.

### 使用步骤：
1. git clone https://github.com/WoodenWhite/DiaryU.git
2. 进入mysite文件夹，python3 manage.py runserver + 端口号
3. 访问localhost:端口号/matching
4. 输入用户id和日记内容，返回：用户名和日记内容，分词结果，情感类型，情感强度以及与其匹配的openID
5. openID为000000代表无可匹配用户
### 情感类型备注：

0. 毫无感情
1. 乐
2. 好
3. 怒
4. 哀
5. 惧
6. 恶
7. 惊
