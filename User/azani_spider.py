import scrapy
from scrapy.crawler import CrawlerProcess

items = []


class AzaniSpider(scrapy.Spider):
    name = "azani"
    custom_settings = {
        'FEED_FORMAT': 'csv',
        'FEED_URI': 'User/export.csv'
    }
    start_urls = [
        'https://www.liveyoursport.com/squash/?search_query=&page=1&limit=36&sort=featured&category=353&is_category_page=1']

    def parse(self, response):
        page_list = []
        for product in response.css('ul.ProductList li'):
            product_link = product.css('div.ProductDetails a::attr(href)').extract_first()
            yield scrapy.Request(product_link, callback=self.parse_product, meta={'url': product_link})

        # Handling Pagination
        for li in response.css('ul.PagingList li'):
            page_num = li.css('a::text').extract_first()
            page_list.append(page_num)

        active_page = page_list.index(None)
        if active_page == 0:
            next_page_index = 2
        else:
            next_page_index = int(page_list[active_page - 1]) + 2
        next_page = self.get_next_url(next_page_index)
        yield scrapy.Request(next_page, callback=self.parse)

    @staticmethod
    def get_next_url(page_no):
        return 'https://www.liveyoursport.com/squash/?search_query=&page=' + str(
            page_no) + '&limit=36&sort=featured&category=353&is_category_page=1'

    @staticmethod
    def parse_product(response):
        product_name = response.css('div.ProductMain h1::text').extract_first()
        product_cost = response.css('div.PriceRow em.ProductPrice::text').extract_first()
        product_description = ''.join(response.css('div.ProductDescription span *::text').extract())
        product_link = response.meta.get('url')

        items.append({
            'Product Name': u''.join(product_name).encode('utf-8').strip(),
            'Price': u''.join(product_cost).encode('utf-8').strip(),
            'Description': u''.join(product_description).encode('utf-8').strip(),
            'URL': u''.join(product_link).encode('utf-8').strip()
        })
        yield {
            'Product Name': product_name,
            'Price': product_cost,
            'Description': product_description,
            'URL': product_link
        }
