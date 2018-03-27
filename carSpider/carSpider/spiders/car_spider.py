# -*- coding: utf-8 -*-
import scrapy
from carSpider.items import CarspiderItem
from carSpider.SpidercarSubTypesItem import SpidercarSubTypesItem
from scrapy.http import Request


class DmozSpider(scrapy.Spider):
    name = "carSpider"
    allowed_domains = ["tzczm.com"]
    start_urls = [
        "http://www.tzczm.com"
    ]

    def parse(self, response):
        cars = response.xpath('//div[@class="listLIlogo"]')
        for index, car in enumerate(cars):
            # 抓取首页的车辆分类数据
            item = CarspiderItem()
            title = car.xpath(
                './/div[@class="listLIlogoT"]/a/text()').extract()[0]
            item['title'] = title
            href = car.xpath(
                './/div[@class="listLIlogoT"]/a/@href').extract()[0]
            item['href'] = href
            image = car.xpath(
                './/div[@class="listLIlogoImg"]/a/img/@src').extract()[0]
            item['image'] = image
            # yield item
            # print title
            # print href
            # print image
            # print "++++++++++++++++++++++++++++++++++++++++++"
            yield item

            subUrl = response.url + href
            # print '开始请求', subUrl
            yield Request(subUrl, callback=TypeSpider().parse_Type)


class TypeSpider(scrapy.Spider):
    name = "subType"
    allowed_domains = ["type"]

    def parse_Type(self, response):
        self.name = "subType"
        # print '收到请求返回' + response.url
        subCarTypes = response.xpath('//div[@class="prd_llt"]/li')
        for index, car in enumerate(subCarTypes):
            subItem = SpidercarSubTypesItem()
            href = car.xpath('.//a/@href').extract()[0]
            subItem['href'] = href
            print subItem['href']
            title = car.xpath('.//a/text()').extract()[0]
            subItem['title'] = title
            print subItem['title']
            image = car.xpath('.//a/img/@src').extract()[0]
            subItem['image'] = image
            print subItem['image']
            subItem['father'] = response.url.split('/')[-2]
            print subItem['father']

            yield subItem
