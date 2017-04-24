#coding=utf-8
__author__ = 'DixonShen'

import scrapy
from scrapy.spider import CrawlSpider
from scrapy.selector import Selector
from scrapy.http import Request
from scrapy.utils.url import urljoin_rfc
from carsales.items import CarsalesItem
import codecs

class CarsalesSpider(CrawlSpider):
	name = 'carsalesSpider'
	allowed_domains = ''
	start_urls = ["https://www.carsales.com.au/cars/"]
	
	page_count = 0
	car_count = 0
	
	def parse(self, response):
		self.page_count += 1
		print '------------------------------------------------------------------' \
		      '-------------------------------------------------------------------' \
		      '                       %s pages have been reached                  ' \
		      '-------------------------------------------------------------------' \
		      '-------------------------------------------------------------------' % str(self.page_count)
		hxs = Selector(response)
		item = CarsalesItem()
		divs = hxs.xpath('//div[@class="n_width-max title "]')
		# print divs
		for div in divs:
			url = div.xpath('.//a/@href').extract()[0]
			item['link'] = urljoin_rfc('https://www.carsales.com.au', url)
			# print url
			yield Request(item['link'], callback=self.parse_detail)
		try:
			# print 'this is next page step'
			next_page = CarsalesItem()
			next_url = hxs.xpath('//a[@id="ctl09_p_ctl14_ctl01_footerPagination_hlNextLink"]/@href').extract()[0]
			next_page['link'] = urljoin_rfc('https://www.carsales.com.au', next_url)
			# print next_page['link']
			yield Request(next_page['link'], callback=self.parse)
		except:
			pass
		
	def parse_detail(self, response):
		self.car_count += 1
		hxs = Selector(response)
		car_title = hxs.xpath('//head/title/text()').extract()[0].strip()
		filename = car_title + '_' + str(self.car_count) + '.txt'
		with codecs.open(filename, 'wb') as f:
			f.write(response.body)
		f.close()
		print '--------------------------------------------------------------------------------------' \
              '---------------------------------------------------------------------------------------' \
              '                  Num %s car: %s has been saved as txt,                                ' \
              '---------------------------------------------------------------------------------------' \
              '---------------------------------------------------------------------------------------' \
		      % (str(self.car_count), car_title)
