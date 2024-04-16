import scrapy
from scrapy.http import Request
from scrapy_amazon.items import ArticleItem

class AmazonScraperSpider(scrapy.Spider):
    name = 'amazon_scraper'
    allowed_domains = ['www.amazon.in']

    custom_settings = { 
                        "DOWNLOADER_MIDDLEWARES" : 
                        {
                            'scrapy_amazon.middlewares.ProxyMiddleware': 350,
                            'scrapy.downloadermiddlewares.httpproxy.HttpProxyMiddleware': 400, 
                        },
                        "CONCURRENT_REQUESTS" : 2,
                        "DOWNLOAD_DELAY" : .3,
                            
                    }
    
    header = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
        }
    
    def start_requests(self):
        
        url = 'https://www.amazon.in/s?k=headphones+wireless&crid=WAIAFDNL3AWL&sprefix=head%2Caps%2C316&ref=nb_sb_ss_ts-doa-p_2_4'
        request = Request(url, headers=self.header, callback=self.parse)
        yield request

    def parse(self, response):
        articles_list = response.xpath('//*[@class="puisg-row"]//*[@data-cy="title-recipe"]//h2//a//@href').extract()
        print(articles_list,"-----------aaaaaaaaaaaa")
        total_page = response.xpath('//*[@class="s-pagination-item s-pagination-disabled"]//text()').get()
        for i in articles_list:
            url = response.urljoin(i)
            print(url)
            request = Request(url, dont_filter=True, callback=self.parse_article)
            yield request

        for i in range(2, int(total_page)+1):
            url = f'https://www.amazon.in/s?k=headphones+wireless&page={i}&crid=WAIAFDNL3AWL&qid=1713201997&sprefix=head%2Caps%2C316&ref=sr_pg_{i}'
            request = Request(url, headers=self.header, callback=self.pagination)
            yield request

    def pagination(self, response):
        articles_list = response.xpath('//*[@class="puisg-row"]//*[@data-cy="title-recipe"]//h2//a//@href').extract()
        for i in articles_list:
            url = response.urljoin(i)
            print(url,"-------------ppppppppppp")
            request = Request(url, dont_filter=True, callback=self.parse_article)
            yield request

    def normalize(self, text):
        return (text.replace("\t", "").replace("\r", "").replace("\u3000", "").replace("\xa0", "").strip())

    def parse_article(self, response):
        title = self.normalize(response.xpath('//*[@id="productTitle"]//text()').get())

        price_symbol = response.xpath('//*[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-price-symbol"]//text()').get()

        price = response.xpath('//*[@class="a-price aok-align-center reinventPricePriceToPayMargin priceToPay"]//span[@class="a-price-whole"]//text()').get()
        price = f"{price_symbol}{price}"

        description = response.xpath('//*[@id="feature-bullets"]//ul')[0]
        description = "\n".join(description.xpath('.//li//text()').extract())

        image = response.xpath('//*[@id="imgTagWrapperId"]//img//@src').get()

        items=ArticleItem()

        items["product_title"] = title
        items["product_description"] = description
        items["product_image"] = image
        items["product_price"] = price

        yield items

