#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/4/28 23:24
# @Author  : Paulson
# @File    : download_video.py
# @Software: PyCharm
# @define  : function


# 1. 准备工作
import pymysql

# 2. 连接数据库
db = pymysql.connect(host='localhost', user='root', password='mima', port=3306, db='spiders')
cursor = db.cursor()
# cursor.execute('SELECT VERSION()')
# data = cursor.fetchone()
# print('Database version:', data)
# cursor.execute("CREATE DATABASE IF NOT EXISTS spiders DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci")
# db.close()


# 3. 创建表
# sql = 'CREATE TABLE IF NOT EXISTS students (id VARCHAR(255) NOT NULL, name VARCHAR(255) NOT NULL, age INT NOT NULL, PRIMARY KEY (id))'
# cursor.execute(sql)
# db.close()


# 4. 插入数据


# data = {
#     'id': '20120001',
#     'name': 'Bob',
#     'age': 20
# }
# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
#
# sql = 'INSERT INTO {table}({keys}) VALUES ({values})'.format(table=table, keys=keys, values=values)
# try:
#     if cursor.execute(sql, tuple(data.values())):
#         print('Successful')
#         db.commit()  # 执行 db 对象的 commit() 方法才可实现数据插入，这个方法才是真正将语句提交到数据库执行的方法，对于数据插入、更新、删除操作都需要调用该方法才能生效。
# except:
#     print('Failed')
#     db.rollback()  # 如果执行失败，则调用rollback() 执行数据回滚，相当于什么都没有发生过一样。
#     raise
#
# db.close()


# 5. 更新数据
# 数据更新操作实际上也是执行 SQL 语句，最简单的方式就是构造一个 SQL 语句然后执行：
# sql = 'UPDATE students SET age = %s WHERE name = %s'
# try:
#     cursor.execute(sql, (28, 'Bob'))
#     db.commit()
# except:
#     db.rollback()
# db.close()

# data = {
#     'id': '20120001',
#     'name': 'Bob',
#     'age': 21
# }
#
# table = 'students'
# keys = ', '.join(data.keys())
# values = ', '.join(['%s'] * len(data))
#
# # ON DUPLICATE KEY UPDATE 使得主键已存在的数据进行更新，后面跟的是更新的字段内容。所以这里就变成了 6 个 %s。所以在后面的 execute() 方法的第二个参数元组就需要乘以 2 变成原来的 2 倍。
# sql = 'INSERT INTO {table}({keys}) VALUES ({values}) ON DUPLICATE KEY UPDATE'.format(table=table, keys=keys, values=values)
# update = ','.join([" {key} = %s".format(key=key) for key in data])
# sql += update
#
# try:
#     if cursor.execute(sql, tuple(data.values())*2):
#         print('Successful')
#         db.commit()
# except:
#     print('Failed')
#     db.rollback()
# db.close()


# 6. 删除数据
# 删除操作相对简单，使用 DELETE 语句即可，需要指定要删除的目标表名和删除条件，而且仍然需要使用 db 的 commit() 方法才能生效，实例如下：
# table = 'students'
# condition = 'age > 20'
# sql = 'DELETE FROM {table} WHERE {condition}'.format(table=table, condition=condition)
# try:
#     cursor.execute(sql)
#     db.commit()
# except:
#     db.rollback()
#
# db.close()


# 7. 查询数据
sql = 'select * from students where age >= 20'

try:
    cursor.execute(sql)
    print('Count:', cursor.rowcount)
    one = cursor.fetchone()
    print('One:', one)
    results = cursor.fetchall()
    print('Results:', results)
    print('Results Type:', type(results))
    for row in results:
        print(row)
except:
    print('Error')
