# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html

import logging
from pymysql import cursors
import copy
import pymysql
from scrapy.utils.project import get_project_settings
class MeishichinaPipeline(object):
        def __init__(self):
            settings = get_project_settings()
            # 1. 建立数据库的连接
            self.connect = pymysql.connect(
            # localhost连接的是本地数据库
                host=settings['MYSQL_HOST'],
                # mysql数据库的端口号
                port=settings['MYSQL_PORT'],
                # 数据库的用户名
                user=settings['MYSQL_USER'],
                # 本地数据库密码
                passwd=settings['MYSQL_PASSWORD'],
                #
            # 2.数据库名
                db=settings['MYSQL_DBNAME'],
                # 编码格式
                charset=settings['MYSQL_CHARSET']
            )
            #创建一个游标cursor, 是用来操作表。
            self.cursor = self.connect.cursor()

        def process_item(self, item, spider):
            # 3. 将Item数据放入数据库，默认是同步写入。
            insert_sql = "INSERT INTO msitem(classification, src, msname, material, step) VALUES ('%s', '%s', '%s', '%s', '%s')" % (
            item['classification'], item['src'], item['msname'], item['material'], item['step'])
            self.cursor.execute(insert_sql)

            # 4. 提交操作
            self.connect.commit()

        def close_spider(self, spider):
            self.cursor.close()
            self.connect.close()


