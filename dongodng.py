# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from newdongguan.items import NewdongguanItem


class DongodngSpider(CrawlSpider):
    name = 'dongdong'
    allowed_domains = ['wz.sun0769.com']
    start_urls = ['http://wz.sun0769.com/index.php/question/questionType?Type=4&page=']
    pageink = LinkExtractor(allow=("type=4"))
    contenlink = LinkExtractor(allow=(r"/html/question/\d+/\d+.shtml"))

    rules = (
        Rule(pageink, process_links="deal_links"),
        Rule(contenlink,callback="parse_item")
    )

    def deal_links(self,links):
        for each in links:
            each.url = each.url.replace("?","&").replace("Type&","Type?")
        return links

    def parse_item(self, response):
        item = NewdongguanItem()

        content = response.xpath('//div[@class="contentext"]/text()').extract()

        if len(content) == 0:
            content = response.xpath('//div[@class="c1 text14_2"]/text()').extract()
            content = "".join(content)
            item['content'] = content.replace(" ", "")
        else:
            content = "".join(content)
            item['content'] = content.replace(" ", "")

        item['title'] =response.xpath('//div[contains(@class,"pagecenter p3")]//strong/text()').extract()[0]
        item['number'] = item['title'].split(' ')[-1].split(":")[-1]
        item['url'] =response.url

        yield item

