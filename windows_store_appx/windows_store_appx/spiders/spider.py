from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from windows_store_appx.items import WindowsStoreAppxItem

query_string = "site%3Awindowsphone.com+AppxManifest.xml"

class MySpider(CrawlSpider):
	name = "appx"
	allowed_domains = ["bing.com"]
	start_urls = ["http://www.bing.com/search?q="+query_string]

	# Next page button: <a href title=Next, class="sb_pagN">
	# '//a[re:test(@title, "Next ")]//@href'
	rules = (Rule(LxmlLinkExtractor(restrict_xpaths=('//a[contains(@title, "Next ")]')), callback='parse_page', follow=True),)

	def parse_page(self, response):
		sel = Selector(response)
		links = sel.xpath('//a[contains(@href, "xap")]')
		appx_list = []
		for link in links:
			app = link.xpath('@href').extract()
			item = WindowsStoreAppxItem()
			item['link'] = app
			appx_list.append(item)
		return appx_list

