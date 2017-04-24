from scrapy.spiders import Spider
from scrapy import Request
from imooc.items import ImoocItem
import copy
class ImoocCourseSpider(Spider):
    name = 'imooc_course'
    start_urls = ['http://www.imooc.com/course/list']
    base_url = 'http://www.imooc.com'
    def parse(self, response):
        """解析全部课程方向地址"""
        item = ImoocItem()
        all_path = response.xpath('//div[@class="course-nav-row clearfix"][1]//a')
        for path in all_path[1:]:
            # TODO: 保存课程方向名称
            item['path'] = path.xpath('.//text()').extract_first()
            path_url = self.base_url + path.xpath('.//@href').extract_first()    # 课程方向地址
            print(path_url)
            yield Request(path_url, meta={'path': copy.deepcopy(item)},callback=self.parse_type)

    def parse_type(self, response):
        """解析各方向下全部课程分类地址"""
        print("方向页：" + response.url)
        item = response.meta['path']
        all_type = response.xpath('//div[@class="course-nav-row clearfix"][2]//a')
        for type in all_type[1:]:
            # TODO: 保存分类名称
            item['type'] = type.xpath('.//text()').extract_first()
            type_url = self.base_url + type.xpath('.//@href').extract_first()    # 课程分类地址
            print(type_url)
            yield Request(type_url, meta={'type':copy.deepcopy(item)} ,callback=self.parse_course)

    def parse_course(self,response):
        """提取课程信息"""
        print("分类页: " + response.url)
        item = response.meta['type']
        all_course = response.xpath('//div[contains(@class, "index-card-container")]')
        for course in all_course:
            course_info = course.xpath('.//div[@class="course-card-info"]/text()')
            item['name'] = course.xpath('.//h3/text()').extract_first()
            item['difficulty'] = course_info.re(r'\w+')[0]
            item['person_number'] = course_info.re(r'\d+')[0]
            yield item
            # 如果有分页
            if response.xpath('//div[@class="page"]'):
                is_end = bool(response.xpath('//div[@class="page"]/span[@class="disabled_page"]/text()').extract()[0] == '下一页')
                if not is_end:
                    next_url = self.base_url + response.xpath('//div[@class="page"]/a/@href').extract()[-1]
                    Request(next_url, callback=self.parse_course)






