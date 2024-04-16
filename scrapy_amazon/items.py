# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class ArticleItem(scrapy.Item):
    product_title = scrapy.Field()
    product_description = scrapy.Field()
    product_image = scrapy.Field()
    product_price = scrapy.Field()

    def to_raw_article_json(self):
        return {
            u"product_title": self.get('product_title'),
            u"product_description": self.get('product_description'),
            u"product_image": self.get('product_image'),
            u"product_price": self.get('product_price'),
        }

