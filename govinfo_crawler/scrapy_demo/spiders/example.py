# -*- coding: utf-8 -*-
import scrapy
from scrapy import Selector
from scrapy.http import Response


class ExampleSpider(scrapy.Spider):
    name = 'example'
    skip = False
    count = {}

    def start_requests(self):
        for dpt in range(1, 99):
            base_url = 'http://yczs.jxzwfww.gov.cn/jxzw/xzql/bsznurl.do?webId=116&itemcode=360982-0002010{}000-XK-'. \
                format(str(dpt).zfill(2))
            for i in range(1, 100):
                if self.skip:
                    self.skip = False
                    break
                for j in range(1, 8):
                    url = base_url + str(i).zfill(3) + '-' + str(j).zfill(2)
                    print(url)
                    yield scrapy.Request(url=url, callback=self.parse_a)

    def parse_a(self, response):
        dep = response.request.url[-15:-13]
        if dep not in self.count:
            self.count[dep] = 0
        if self.count[dep] > 1000:
            self.skip = True
        sel = Selector(response)
        if sel.response.body:
            print(self.count[dep])
            self.count[dep] = 0
            # print(response, sel.response.body)
            # print(sel.response.body.decode('utf8'))
            yield scrapy.Request(url=sel.response.body.decode('utf8'), callback=self.parse_b)
        else:
            self.count[dep] += 1
            print(self.count[dep], self.skip)

    def parse_b(self, response):
        sell = Selector(response)
        tmp_dict = {'审批事项名称': sell.xpath('/html/body/div[6]/div[1]/div[1]/text()').extract()}
        for row in range(1, 10):
            for column in range(1, 3):
                if str(sell.xpath(self.get_xpath(row, 2 * column - 1)).extract()):
                    tmp_dict[str(sell.xpath(self.get_xpath(row, 2 * column - 1)).extract())] \
                        = sell.xpath(self.get_xpath(row, 2 * column)).extract()
        print('###', tmp_dict['审批事项名称'])
        yield tmp_dict

    def get_xpath(self, r, c):
        result = '//*[@id="con1"]/table/tr[{}]/td[{}]/text()'.format(r, c)
        return str(result)
