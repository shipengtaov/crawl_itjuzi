# -*- coding: utf-8 -*-

from urlparse import urljoin

from scrapy.utils.response import get_base_url

def get_job_url(response):
    job_regulars = [
        u'jobs',
        u'join us',
        u'加入我们',
        u'诚聘英才',
        u'工作职位',
        u'招贤纳士',
    ]
    job_text_min_length = 2
    job_text_max_length = 10

    job_url = None

    job_a_tag_xpath = response.xpath('//a')
    for i in job_a_tag_xpath:
        text_extract = i.xpath('./text()').extract()
        if not text_extract:
            continue
        text_length = len(text_extract[0].strip())
        if text_length < job_text_min_length or text_length > job_text_max_length:
            continue

        for job_regular in job_regulars:

            if i.xpath('./text()').re(job_regular):
                job_url_tmp = i.xpath('./@href').extract()
                if job_url_tmp and job_url_tmp[0] != '#' and job_url_tmp[0].startswith('http'):
                    job_url = job_url_tmp[0]
                    break

        if job_url:
            break
    if job_url:
        return urljoin(get_base_url(response), job_url)
    else:
        return ''
