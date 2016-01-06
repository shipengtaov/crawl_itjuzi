# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CompanyItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    product_name = scrapy.Field()
    company_name = scrapy.Field()
    url = scrapy.Field()
    startup_time = scrapy.Field()
    address = scrapy.Field()
    # 公司运营状态; 运营中|未上线|已关闭|已转型
    status = scrapy.Field()
    # 融资状态
    # fund_status = scrapy.Field()
    # 阶段
    stage = scrapy.Field()

    # 招聘页面
    job_url = scrapy.Field()

