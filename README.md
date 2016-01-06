抓取 itjuzi.com 的公司信息
========================

运行
----

	$ scrapy crawl company_spider -o logs/companies.json
	$ scrapy crawl company_spider -a max_count=10 -o logs/companies.json ＃ 可以自定义抓取数量. 默认1000

* logs/companies.json 保存抓取到的公司信息(每次运行时需重新清空文件内容，否则会打乱json格式)
* logs/job_url_percent.log 保存抓取到多少个公司的招聘页面信息，以及本次一共抓取了多少公司

