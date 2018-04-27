# carSpider
简单爬虫Python+Scrapy

<p>
基于Python和Scrapy的车辆信息抓取爬虫，抓取完成存入本地数据库
</p>
<pre><code>
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
</code></pre>

<pre><code>
class CarspiderPipeline(object):
    global hostUrl
    hostUrl = 'http://www.tzczm.com'
    
    def open_spider(self, spider):
        print 'spider开始'
        global conn
        conn = MySQLdb.connect(host='localhost', user='root',
                               passwd='密码', db='数据库名', charset='utf8')
        global cur
        cur = conn.cursor()
        pass

    def process_item(self, item, spider):

        if isinstance(item, CarspiderItem):
            print '总分类'
            createSql = "CREATE TABLE IF NOT EXISTS car_types (id INT(11) unsigned NOT NULL AUTO_INCREMENT,title varchar(100) DEFAULT NULL,image varchar(100) DEFAULT NULL,href varchar(50) DEFAULT NULL,PRIMARY KEY(id)) ENGINE = InnoDB AUTO_INCREMENT = 92 DEFAULT CHARSET = utf8"
            cur.execute(createSql)
            insertSql = "INSERT INTO car_types (title, image, href) VALUES ('%s', '%s%s', '%s')" % (
                item['title'], hostUrl, item['image'], item['href'])
            print '执行sql', insertSql
            cur.execute(insertSql)
            conn.commit()

        elif isinstance(item, SpidercarSubTypesItem):
            print '小分类'
            createSubSql = "CREATE TABLE IF NOT EXISTS car_sub_types (id INT(11) unsigned NOT NULL AUTO_INCREMENT,title varchar(100) DEFAULT NULL,image varchar(100) DEFAULT NULL,href varchar(50) DEFAULT NULL,father varchar(50) DEFAULT NULL,PRIMARY KEY(id)) ENGINE = InnoDB AUTO_INCREMENT = 92 DEFAULT CHARSET = utf8"
            cur.execute(createSubSql)

            insertSql = "INSERT INTO car_sub_types (title, image, href, father) VALUES ('%s', '%s%s', '%s', '%s')" % (
                item['title'], hostUrl, item['image'], item['href'], item['father'])
            print '执行sql', insertSql
            cur.execute(insertSql)
            conn.commit()

        return item

    def close_spider(self, spider):
        print 'spoder关闭'
        cur.close()
        conn.close()
        pass
</code></pre> 
