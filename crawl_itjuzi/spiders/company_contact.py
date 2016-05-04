# -*- coding: utf-8 -*-

from __future__ import absolute_import,print_function

'''
create: 2016年5月4日

抓取国内公司联系信息
'''

import os

import scrapy
from scrapy.exceptions import CloseSpider

from crawl_itjuzi.items import CompanyContactItem
from crawl_itjuzi import utils
from crawl_itjuzi import constant

class CompanyContactSpider(scrapy.Spider):
    name = "company_contact_spider"
    start_urls = [
    ]

    # 从第几页开始抓取
    start_page = None
    # 最多允许抓取多少个
    max_count = None
    # 当前抓取了多少个
    current_count = 0

    def __init__(self, start_page=None, max_count=None, *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        start_url = 'http://www.itjuzi.com/company'

        if start_page:
            self.start_page = int(start_page)
            start_url += '?page={}'.format(self.start_page)
        if max_count:
            self.max_count = int(max_count)

        self.start_urls.append(start_url)

    def parse(self, response):
        companies = response.xpath('//ul[@class="list-main-icnset"]/li')
        for company in companies:
            info = company.xpath('.//p[@class="title"]/a/@href')
            if not info.extract():
                continue
            yield scrapy.Request(info.extract()[0], callback=self.parse_company_detail)

        if self.max_count is not None and self.current_count >= self.max_count:
            raise CloseSpider('max_count limit: {}'.format(self.max_count))

        # 下一页
        page_xpath = response.xpath('//div[contains(@class, "ui-pagechange")]/a')
        next_page = None
        for i in page_xpath:
            if i.xpath('./text()').re(u'.*下一页.*'):
                next_page = i
                break
        if next_page:
            next_page_url = next_page.xpath('./@href').extract()
            if next_page_url:
                yield scrapy.Request(next_page_url[0], callback=self.parse)

    def parse_company_detail(self, response):
        if self.max_count is not None and self.current_count >= self.max_count:
            raise CloseSpider('max_count limit: {}'.format(self.max_count))

        item = CompanyContactItem()

        infohead = response.xpath('//div[@class="rowhead"]')
        item['product_name'] = infohead.xpath('.//span[@class="title"]//text()').extract()[0].strip()
        item['scope'] = '-'.join([i.strip() for i in infohead.xpath('.//span[contains(@class, "scope")]//text()').extract() if i.strip()])
        item['url'] = infohead.xpath('.//a[@class="weblink"]/@href').extract()[0]

        des_more = response.xpath('//div[@class="boxed"]/div[@class="main"]//div[@class="des-more"]//span/text()').extract()
        item['company_name'] = des_more[0].strip()
        item['startup_time'] = des_more[1].strip()
        item['status'] = des_more[2].strip()

        for li in response.xpath('//ul[contains(@class, "aboutus")]/li'):
            if li.xpath('./*[contains(@class, "fa-phone")]'):
                item['phone'] = ''.join(li.xpath('.//text()').extract()).strip()
            elif li.xpath('./*[contains(@class, "fa-envelope")]'):
                item['email'] = ''.join(li.xpath('.//text()').extract()).strip()
            elif li.xpath('./*[contains(@class, "fa-map-marker")]'):
                item['address'] = ''.join(li.xpath('.//text()').extract()).strip()

        self.current_count += 1
        return item

    def closed(self, reason):
        pass
