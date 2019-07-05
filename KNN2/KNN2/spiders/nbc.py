# -*- coding: utf-8 -*-
import scrapy


class CnnSpider(scrapy.Spider):
    name = 'nbc'
    allowed_domains = ['www.nbcnews.com']
    start_urls = ['https://www.nbcnews.com/politics', 'https://www.nbcnews.com/us-news',
                  'https://www.nbcnews.com/business', 'https://www.nbcnews.com/world',
                  'https://www.nbcnews.com/tech-media', 'https://www.nbcnews.com/think']

    def parse(self, response):
        types_of_articles = response.url.split('/')[-1]
        # domain = 'https://www.nbcnews.com/'
        articles_raw = response.css('h2.teaseCard__headline a::attr(href)').extract()

        for article in articles_raw:
            # if 'video' in article:
            #     continue
            # urls = article
            yield scrapy.Request(article, callback=self.parse_article, meta={'type': types_of_articles})

    def parse_article(self, response):
        journals = {}
        journals['headline'] = response.css('h1.headline___CuovH::text').extract()
        journals['content'] = response.css('p::text').extract()
        sub = response.css('div.articleDek::text').extract()
        journals['content'].append(sub[0])
        journals['type'] = response.meta['type']
        yield journals
