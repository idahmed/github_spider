import os

import scrapy


class BaseSpider(scrapy.Spider):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.download_delay = 0.25
        
        # self.rest_id = kwargs["rest_id"]
