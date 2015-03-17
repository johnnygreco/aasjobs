# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class Job(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    jobid = scrapy.Field()
    title = scrapy.Field()
    org = scrapy.Field()
    postdate = scrapy.Field()
    link = scrapy.Field()
    category = scrapy.Field()
    deadline = scrapy.Field()
    description = scrapy.Field()
    

