'''
	Scrapy CrawlSpider for bing.com results based on search for appx apps in the windows phone store

	Author: Bogdan Copos, bcopos@ucdavis.edu
'''



from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.selector import Selector
from windows_store_appx.items import WindowsStoreAppxItem

import time, random



query_string = "site%3Awindowsphone.com+AppxManifest.xml"

class WSAppxSpider(CrawlSpider):
	name = "appx"
	allowed_domains = ["bing.com"]
	start_urls = ["http://www.bing.com/search?q="+query_string]

	# Next page button: <a href title=Next, class="sb_pagN">
	# '//a[re:test(@title, "Next ")]//@href'
	rules = (Rule(LxmlLinkExtractor(restrict_xpaths=('//a[contains(@title, "Next ")]')), callback='parse_page', follow=True),)

	def __init__(self, outputfile=None, *args, **kwargs):
		super(WSAppxSpider, self).__init__(*args, **kwargs)
		self.outputfile = outputfile

	def parse_page(self, response):
		sel = Selector(response)
		links = sel.xpath('//a[contains(@href, "xap")]')
		appx_list = []
		for link in links:
			app = link.xpath('@href').extract()[0]
			item = WindowsStoreAppxItem()
			item['link'] = app
			appx_list.append(item)

			if self.outputfile != "":
				f = open(self.outputfile, 'a')
				f.write(app.encode('utf-8').strip()+"\n")
				f.close()

		# random sleep to avoid detection
		time.sleep(random.randint(0, 30))

		return appx_list
