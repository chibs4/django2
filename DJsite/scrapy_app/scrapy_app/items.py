# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Skysports_item(scrapy.Item):
    # define the fields for your item here like:
    link = scrapy.Field()
    long_title = scrapy.Field()
    author = scrapy.Field()
    body = scrapy.Field()
    menu_link = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    image = scrapy.Field()
    pass

class CBS_item(scrapy.Item):
    link =scrapy.Field()
    author = scrapy.Field()
    body =scrapy.Field()
    menu_link = scrapy.Field()
    title = scrapy.Field()
    tags = scrapy.Field()
    image= scrapy.Field()
    long_title = scrapy.Field()
    pass
