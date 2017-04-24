from scrapy.spiders import Spider
from scrapy.conf import settings
from scrapy import Request
from zhihulive.items import ZhihuliveItem
import json


class ZhihuLivesSpider(Spider):
    name = 'zhihulives'
    start_url = 'https://api.zhihu.com/lives/homefeed?includes=live'
    cookie = settings['COOKIE']
    lives_page = 1

    def start_requests(self):
        yield Request(url=self.start_url, cookies=self.cookie)

    def parse(self, response):
        response_body = json.loads(response.body)
        filename = str(self.lives_page) + ".json"
        print(type(filename))
        with open(filename, "w") as file:
            json.dump(response_body, file, ensure_ascii=False)

        # model
        item = ZhihuliveItem()

        for data in response_body['data']:
            if data['object_type'] == 'live':
                item['live_subject'] = data['live']['subject']
                item['live_description'] = data['live']['speaker']['description']
                item['live_tag'] = data['live']['tags'][0]['short_name']
                item['review_count'] = data['live']['review']['count']
                item['seats_taken'] = data['live']['seats']['taken']
                item['review_score'] = data['live']['review']['score']
                item['speaker_name'] = data['live']['speaker']['member']['name']
                item['speaker_headline'] = data['live']['speaker']['bio']
                item['speaker_gender'] = data['live']['speaker']['member']['gender']

                yield item

        is_end = response_body['paging']['is_end']
        if not is_end:
            self.lives_page = self.lives_page + 1
            next_url = response_body['paging']['next']
            yield Request(next_url)
