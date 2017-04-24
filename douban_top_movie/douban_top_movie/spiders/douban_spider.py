from scrapy import Request
from scrapy.spiders import Spider
from douban_top_movie.items import DoubanTopMovieItem

class DoubanMovieTop250Spider(Spider):
    name = 'douban_movie_top250'
    start_urls = ['https://movie.douban.com/top250']

    def parse(self, response):
        item = DoubanTopMovieItem()
        movies = response.xpath('//div[@class="item"]')
        for movie in movies:
            item['ranking'] = movie.xpath('.//div[@class="pic"]/em/text()').extract()[0]
            item['movie_name'] = movie.xpath('.//div[@class="hd"]//span[1]/text()').extract()[0]
            item['score'] = movie.xpath('.//div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
            item['score_num'] = movie.xpath('.//div[@class="star"]/span/text()').re(r'(\d+)人评价')[0]
            yield item

        # 下一页
        next_url = response.xpath('//span[@class="next"]/a/@href').extract()
        if next_url:
            next_url = 'https://movie.douban.com/top250' + next_url[0]
            yield Request(next_url)