# coding:utf-8

import os
os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'

'''
Django 版本大于等于1.7的时候，需要加上下面两句
import django
django.setup()
否则会抛出错误 django.core.exceptions.AppRegistryNotReady: Models aren't loaded yet.
'''
import django

if django.VERSION >= (1, 7):  # 自动判断版本
    django.setup()

from matching.models import Word
import xlrd  # excel读工具

data = xlrd.open_workbook('words.xlsx')  # 打开文件
table = data.sheet_by_index(0)  # 获取工作表
nrows = table.nrows  # 行数
ncols = table.ncols  # 列数
colnames = table.row_values(0)
WorkList = []
x = y = z = 0
for i in range(1, nrows):
    row = table.row_values(i)  # 获取每行值
    for j in range(0, ncols):
        if type(row[j]) == float:  # 如果值为float则转换为int,避免出现1输出为1.0的情况
            row[j] = int(row[j])
    if row:  # 查看行值是否为空
        # 判断该行值是否在数据库中重复
        if Word.objects.filter(word=row[0], emotionty=row[1], strength=row[2]).exists():
            x = x + 1  # 重复值计数
        else:
            y = y + 1  # 非重复计数
            WorkList.append(Word(
                word=row[0], emotionty=row[1], strength=row[2],
            )
            )
    else:
        z = z + 1  # 空行值计数
Word.objects.bulk_create(WorkList)

print('数据导入成功,导入'+str(x)+'条,重复'+str(y)+'条,有'+str(z)+'行为空!')
