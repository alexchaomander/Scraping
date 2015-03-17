import scrapy
from scrapy.contrib.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
from officedepot.items import OfficedepotItem


class OfficeDepotSpider(CrawlSpider):
    name = 'officedepot'
    allowed_domains = ['www.officedepot.com']
    start_urls = [
        'http://www.officedepot.com/',
        'http://www.officedepot.com/a/products/355141/Toshiba-Satellite-C55-B-Laptop-Computer/?componentName=content&id=355141&tab=2'
    ]
    rules = (
      Rule(LinkExtractor(allow='products/\d*/.*&tab=2'), callback='parse_product', follow=True),
      Rule(LinkExtractor(allow='/a/products/'), follow=True),
      Rule(LinkExtractor(allow='/a/browse/'), follow=True),
    )

    def extract_text(self, selector):
        extracted = selector.extract()
        if len(extracted) < 1:  # if extract() doesn't find anything, it returns a blank list
            return ''           # return a blank string indicating not found
        return extracted[0].strip()

    def parse_product(self, response):
        product = OfficedepotItem()

        name = self.extract_text(response.css('#skuHeading > h1 > span::text'))
        sku  = self.extract_text(response.css('#omxSku::text'))

        image_urls = response.css('#mainSkuProductImage::attr(src)').extract()
        rows       = response.css('#skuDetails > div.skudetailbox.show.tab_content_container > div.sku_det.tab_block_content.show > table > tr')

        details    = {}

        for row in rows:
            key          = self.extract_text(row.css('th::text'))
            value        = self.extract_text(row.css('td::text'))
            details[key] = value

        product['name']       = name
        product['details']    = details
        product['sku']        = sku
        product['image_urls'] = image_urls
        product['url']        = response.url
        return product
