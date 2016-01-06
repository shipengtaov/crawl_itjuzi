# -*- coding: utf-8 -*-

import os

import scrapy
from scrapy.exceptions import CloseSpider

from crawl_itjuzi.items import CompanyItem
from crawl_itjuzi import utils
from crawl_itjuzi import constant

class CompanySpider(scrapy.Spider):
    name = "company_spider"
    start_urls = [
        'http://www.itjuzi.com/company',
    ]

    # 最多允许抓取多少个
    max_count = 1000
    # 当前抓取了多少个
    current_count = 0
    # 获取的 job_url 的数量
    job_url_count = 0

    def __init__(self, max_count=None, *args, **kwargs):
        super(CompanySpider, self).__init__(*args, **kwargs)
        if max_count:
            self.max_count = int(max_count)

    def parse(self, response):
        companies = response.xpath('//ul[@class="list-main-icnset"]/li')
        for company in companies:
            info = company.xpath('.//p[@class="title"]/a/@href')
            if not info.extract():
                continue
            yield scrapy.Request(info.extract()[0], callback=self.parse_company_detail)

        if self.current_count >= self.max_count:
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
        if self.current_count >= self.max_count:
            raise CloseSpider('max_count limit: {}'.format(self.max_count))

        item = {}

        infohead = response.xpath('//div[@class="rowhead"]')
        item['product_name'] = infohead.xpath('.//span[@class="title"]/text()').extract()[0].strip()

        address_link = infohead.xpath('./div[@class="picinfo"]/div[contains(@class, "c-gray-aset")]')
        item['address'] = ' '.join([i.strip() for i in address_link.xpath('./div[contains(@class, "marr10")]//text()').extract()])
        item['url'] = address_link.xpath('./div[contains(@class, "linkset")]//i[contains(@class, "fa-link")]/../../@href').extract()[0]

        des_more = response.xpath('//div[@class="boxed"]/div[@class="main"]//div[@class="des-more"]//span/text()').extract()
        item['company_name'] = des_more[0].strip()
        item['startup_time'] = des_more[1].strip()
        item['status'] = des_more[2].strip()

        yield scrapy.Request(item['url'], meta=item, callback=self.parse_job_url)

    def parse_job_url(self, response):
        item = CompanyItem()

        meta = response.meta
        item['product_name'] = meta['product_name']
        item['address'] = meta['address']
        item['url'] = meta['url']
        item['company_name'] = meta['company_name']
        item['startup_time'] = meta['startup_time']
        item['status'] = meta['status']
        item['job_url'] = utils.get_job_url(response)

        if item['job_url']:
            self.job_url_count += 1

        self.current_count += 1

        return item

    def closed(self, reason):
        with open(os.path.join(constant.ROOT_DIR, 'logs', 'job_url_percent.log'), 'w') as f:
            f.write('共抓取{total}个公司, 抓到{job}个公司的招聘页面'.format(job=self.job_url_count, total=self.current_count))
