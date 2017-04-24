# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo

from scrapy.conf import settings
from scrapy.exceptions import DropItem
from scrapy import log


class DoubanTopMoviePipeline(object):
    def __init__(self):
        # 连接数据库，终端执行 mongo 运行数据库
        connection = pymongo.MongoClient('localhost', 27017)
        # 获取数据库，需提前建好
        db = connection.douban
        # 获取集合（表）,若不存在则新建
        self.collection = db.movietop

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("movie info added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
