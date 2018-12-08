# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanItem


# 创建项目：scrapy genspider douban_spider movie.douban.com
# 路径： /d/pythoncharm/pachong/douban/douban/spiders
class DoubanSpiderSpider(scrapy.Spider):
    # 爬虫名称，不能和项目名称相同
    name = 'douban_spider'
    # 只会抓取当前域名内
    allowed_domains = ['movie.douban.com']
    # 入口url
    start_urls = ['https://movie.douban.com/top250']

    # 默认解析方法
    def parse(self, response):
        movie_list = response.xpath("//div[@class='article']//ol[@class='grid_view']/li")
        for i_item in movie_list:
            douban_item = DoubanItem()
            douban_item['serial_number'] = i_item.xpath(".//div[@class='item']//em//text()").extract_first()
            douban_item['movie_name'] = i_item.xpath(".//div[@class='info']/div[@class='hd']/a/span[1]/text()").extract_first()

            # 处理数据
            content = i_item.xpath(".//div[@class='info']/div[@class='bd']/p[1]/text()").extract()
            for i_content in content:
                contents = "".join(i_content.split())
                douban_item['introduce'] = contents
                print(douban_item)

            douban_item['star'] = i_item.xpath(".//span[@class='rating_num']/text()").extract_first()
            douban_item['invaluate'] = i_item.xpath(".//div[@class='star']/span[4]/text()").extract_first()
            douban_item['describe'] = i_item.xpath(".//p[@class='quote']/span[1]/text()").extract_first()

            # 提交管道pipline
            yield douban_item

        # 下一页数据
        next_link = response.xpath(".//span[@class='next']/link/@href").extract()
        if next_link:
            next_link = next_link[0]
            yield scrapy.Request("https://movie.douban.com/top250"+next_link,callback=self.parse)

