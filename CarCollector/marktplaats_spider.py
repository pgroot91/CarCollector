import scrapy


class MarktplaatsAutoSpider(scrapy.Spider):
    name = 'marktplaats_auto'
    start_urls = ['http://www.marktplaats.nl/c/auto-s/c91.html']

    def parse(self, response):
        for option in response.xpath("//select[@name='categoryId']/optgroup[@label='Alle merken']/option"):
            print(option)
            yield {
                'brand_name': option.xpath('text()').extract(),
                'brand_id': option.xpath('@value').extract(),
            }