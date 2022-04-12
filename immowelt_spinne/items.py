# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class ImmoweltSpinneItem(scrapy.Item):
    onlineId = scrapy.Field()
    globalObjectKey = scrapy.Field()
    areas = scrapy.Field()
    address = scrapy.Field()
    name = scrapy.Field()
    creationDate = scrapy.Field()
    broker = scrapy.Field()
    rooms = scrapy.Field()
    price = scrapy.Field()
    estateType = scrapy.Field()
    distributionType = scrapy.Field()
    images = scrapy.Field()
    equipment = scrapy.Field()
    # name = scrapy.Field()
    
