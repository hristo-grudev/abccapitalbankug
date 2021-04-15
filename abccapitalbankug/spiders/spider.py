import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import AbccapitalbankugItem
from itemloaders.processors import TakeFirst


class AbccapitalbankugSpider(scrapy.Spider):
	name = 'abccapitalbankug'
	start_urls = ['https://www.abccapitalbank.co.ug/blog/blog-news/']

	def parse(self, response):
		post_links = response.xpath('//div[contains(@class,"blog-post-more")]/a/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

		next_page = response.xpath('//span[@class="page-link"]/a/@href').getall()
		yield from response.follow_all(next_page, self.parse)

	def parse_post(self, response):
		title = response.xpath('//h3[@class="page-tree-text"]/text()').get()
		description = response.xpath('//div[@class="blog-post-detail"]//text()[normalize-space() and not(ancestor::div[@class="fb-background-color"])]').getall()
		description = [p.strip() for p in description if '{' not in p]
		description = ' '.join(description).strip()
		date = response.xpath('//div[@class="blog-post-info"]/span/span/text()').get()
		date = re.findall(r'[A-Za-z]+\s\d{1,2},\s\d{4}', date)[0]

		item = ItemLoader(item=AbccapitalbankugItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
