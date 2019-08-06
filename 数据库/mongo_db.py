#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/25 19:14
# @Author  : Paulson
# @File    : mongo_db.py
# @Software: PyCharm
# @define  : function

import pymongo
from pymongo import MongoClient

class TestMongo():
    def __init__(self):
        client = MongoClient(host="127.0.0.1", port=27017)
        self.collection = client['newtestdb']['t1']   # 使用方括号的方式选择数据库和集合
        
    def test_insert(self):
        """insert 字典， 返回 objectId"""
        ret = self.collection.insert_one({"name":"test100111", "age":33})
        print(ret)
    
    def test_insert_many(self):
        item_list = [{"name":"test_many{}".format(i)} for i in range(10)]
        # insert_many 接受一个列表， 列表中为所有需要插入的字典
        t = self.collection.insert_many(item_list)
        # t.inserted_id 为所有需要插入的字典
        for i in t.inserted_ids:
            print(i)
    
    def find_one(self):
        t = self.collection.find_one({"name": "test100111"})
        print(t)
        
    def find_all(self):
        t = self.collection.find()
        for i in t:
            print(i)
    
    def try_updata_one(self):
        self.collection.update_one({"name":"test100111"}, {"$set":{"name":"new_test"}})

    def try_updata_many(self):
        self.collection.update_many({"name": "test100111"}, {"$set": {"name": "new_test"}})


if __name__ == '__main__':
    testmongo = TestMongo()
    # testmongo.test_insert()
    # testmongo.test_insert_many()
    # testmongo.find_all()