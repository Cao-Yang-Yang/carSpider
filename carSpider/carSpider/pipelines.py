# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

import MySQLdb
from carSpider.items import CarspiderItem
from carSpider.SpidercarSubTypesItem import SpidercarSubTypesItem


class CarspiderPipeline(object):
    global hostUrl
    hostUrl = 'http://www.tzczm.com'

    def open_spider(self, spider):
        print 'spider开始'
        global conn
        conn = MySQLdb.connect(host='localhost', user='root',
                               passwd='密码', db='数据库名', charset='utf8')
        global cur
        cur = conn.cursor()
        pass

    def process_item(self, item, spider):

        if isinstance(item, CarspiderItem):
            print '总分类'
            createSql = "CREATE TABLE IF NOT EXISTS car_types (id INT(11) unsigned NOT NULL AUTO_INCREMENT,title varchar(100) DEFAULT NULL,image varchar(100) DEFAULT NULL,href varchar(50) DEFAULT NULL,PRIMARY KEY(id)) ENGINE = InnoDB AUTO_INCREMENT = 92 DEFAULT CHARSET = utf8"
            cur.execute(createSql)
            insertSql = "INSERT INTO car_types (title, image, href) VALUES ('%s', '%s%s', '%s')" % (
                item['title'], hostUrl, item['image'], item['href'])
            print '执行sql', insertSql
            cur.execute(insertSql)
            conn.commit()

        elif isinstance(item, SpidercarSubTypesItem):
            print '小分类'
            createSubSql = "CREATE TABLE IF NOT EXISTS car_sub_types (id INT(11) unsigned NOT NULL AUTO_INCREMENT,title varchar(100) DEFAULT NULL,image varchar(100) DEFAULT NULL,href varchar(50) DEFAULT NULL,father varchar(50) DEFAULT NULL,PRIMARY KEY(id)) ENGINE = InnoDB AUTO_INCREMENT = 92 DEFAULT CHARSET = utf8"
            cur.execute(createSubSql)

            insertSql = "INSERT INTO car_sub_types (title, image, href, father) VALUES ('%s', '%s%s', '%s', '%s')" % (
                item['title'], hostUrl, item['image'], item['href'], item['father'])
            print '执行sql', insertSql
            cur.execute(insertSql)
            conn.commit()

        return item

    def close_spider(self, spider):
        print 'spoder关闭'
        cur.close()
        conn.close()
        pass
