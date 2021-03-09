# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class HentaiItem(scrapy.Item):
    title = scrapy.Field()
    name = scrapy.Field()
    img_url = scrapy.Field()
    pass
