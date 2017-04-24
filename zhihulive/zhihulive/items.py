# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class ZhihuliveItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    live_subject = scrapy.Field()    # 标题
    live_description = scrapy.Field()  # 简介
    live_tag = scrapy.Field()    # 分类
    seats_taken = scrapy.Field()    #参与人数
    review_count = scrapy.Field()    # 评价数量
    review_score = scrapy.Field()    # 评分

    speaker_name = scrapy.Field()    # 主讲人
    speaker_headline = scrapy.Field()    # 主讲人身份
    speaker_gender = scrapy.Field()  # 主讲人性别

