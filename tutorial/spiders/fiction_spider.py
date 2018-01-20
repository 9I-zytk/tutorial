import scrapy
from tutorial.items import fictionList,fiction

class DmozSpider(scrapy.Spider):
    name = "fiction"
    allowed_domains = ["www.biqudu.com"]
    start_urls = [
        "https://www.biqudu.com/paihangbang/"
    ]

    def parse(self, response):
        for sel in response.xpath('//table[@class="tbo"]'):
            fictionType = sel.xpath('tbody/*/*/span[@class="btitle"]/text()').extract()
            print('小说类型：',fictionType)
            # 总榜
            for list in sel.xpath('tbody/*/*/*/ul[1]/li'):
                itemList = fictionList()
                itemList['type'] = fictionType
                fictionName = list.xpath('a/text()').extract_first()
                fictionUrl = list.xpath('a/@href').extract_first()
                itemList['name'] = fictionName
                itemList['url'] = fictionUrl
                url = response.urljoin(fictionUrl)
                yield scrapy.Request(url, callback=self.parse_dir_contents)

    def parse_dir_contents(self, response):
        info = response.xpath('//div[@id="info"]')
        item = fiction()
        item['name'] = str(info.xpath('h1/text()').extract_first())
        item['url'] = response.url
        item['author'] = str(info.xpath('p[1]/text()').extract_first()).split(':')[1]
        item['latestTime'] = info.xpath('p[3]/text()').extract_first()
        item['latest'] = info.xpath('p[4]/a/text()').extract_first()
        item['desc'] = str(response.xpath('//div[@id="intro"]/p[1]/text()').extract_first())
        url = info.xpath('p[4]/a/@href').extract_first()
        fictionUrl = response.urljoin(url)
        request = scrapy.Request(fictionUrl, callback=self.parse_fiction_contents)
        request.meta['item'] = item
        yield request

    def parse_fiction_contents(self, response):
        content = response.xpath('//div[@id="content"]/text()').extract_first()
        item = response.meta['item']
        item['contents'] = str(content)
        return item