import scrapy
from selenium import webdriver
from hentai.items import HentaiItem
import requests


class ManhuaSpider(scrapy.Spider):
    name = 'manhua'
    # allowed_domains = ['www.xxx.com']
    start_urls = ['https://zh.nyahentai.xyz/tag/full-color/']
    # driver = webdriver.ChromeOptions()
    # driver.add_argument('--ignore-certificate-errors')
    # driver.add_argument('--ignore-ssl-errors')
    # driver = webdriver.Chrome(chrome_options=driver)
    # driver.execute_cdp_cmd("Page.addScriptToEvaluateOnNewDocument", {
    #     "source": """
    #     Object.defineProperty(navigator, 'webdriver', {
    #       get: () => undefined
    #     })
    #   """
    # })


    def parse(self, response):
        url = response.xpath('//*[@id="content"]/div//div')
        for i in url:
            if i.xpath('./a/@href').extract_first():
                _url = 'https://zh.nyahentai.xyz/' + i.xpath('./a/@href').extract_first()
                yield scrapy.Request(url=_url,callback=self.img_url_)


    def img_url_(self,response):
        item = HentaiItem()
        url = response.xpath('//*[@id="thumbnail-container"]//div')
        item['title'] = response.xpath('//*[@id="info"]/h1/text()').extract_first().split(' ')[0]
        for i in url:
            img1 = 'https://zh.nyahentai.xyz/' + i.xpath('./a/@href').extract_first()
            yield scrapy.Request(url=img1,callback=self.img_url_1,meta={'item':item})


    def img_url_1(self,response):
        item = response.meta['item']
        img_url = response.xpath('//*[@id="image-container"]/a/img/@src').extract_first()
        n = img_url.split('/')
        item['name'] = n[-2] + n[-1]
        item['img_url'] = img_url
        return item







