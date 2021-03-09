# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
import random, time


class HentaiDownloaderMiddleware:

    def process_request(self, request, spider):


        return None


