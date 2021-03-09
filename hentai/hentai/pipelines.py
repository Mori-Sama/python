# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
import os
from scrapy.pipelines.images import ImagesPipeline

class MyImage(ImagesPipeline):
    # 该方法是用来对媒体资源进行请求的，item就是爬虫类提交的
    def get_media_requests(self,item,info):
        yield scrapy.Request(item['img_url'],meta={'item':item})
    # 指明数据的存储路径
    def file_path(self,request,response=None,info=None):
        item = request.meta['item']

        return f'{item["title"]}/{item["name"]}'

    def item_complated(self,results,item,info):
        return item





