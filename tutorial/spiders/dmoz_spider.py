import scrapy
from tutorial.items import TutorialItem

class DmozSpider(scrapy.Spider):
    name = "dmoz"
    allowed_domains = ["dmoz.org"]
    start_urls = [
        "https://www.resource-zone.com/forum/f/chinese.32/"
    ]

    def parse(self, response):
        for sel in response.xpath('//ol/li'):
            print(sel.xpath('div[@class="listBlock main"]/div[@class="titleText"]/h3/a[@class="PreviewTooltip"]/text()').extract())
            item = TutorialItem()
            item['title'] = sel.xpath('div[@class="listBlock main"]/div[@class="titleText"]/h3/a[@class="PreviewTooltip"]/text()').extract()
            item['link'] = sel.xpath('div[@class="listBlock main"]/div[@class="titleText"]/h3/a[@class="PreviewTooltip"]/@href').extract()
            item['user'] = sel.xpath('div[@class="listBlock main"]/*/*/div[@class="posterDate muted"]/a[@class="username"]/text()').extract()
            yield item
