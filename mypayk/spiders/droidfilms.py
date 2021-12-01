import scrapy
from datetime import datetime
import re
from mypayk.spiders.modelsmy import myconnmy
from scrapy.loader.processors import MapCompose
from urllib.parse import urljoin

res = 1


class DroidsSpider(scrapy.Spider):
    name = 'rutor'
    allowed_domains = ['droidfilms.org']
    start_urls = ['https://droidfilms.org/']
    pages_count = 2
    def start_requests(self):
        for page in range(0, 1 + self.pages_count):
            url = f'https://droidfilms.org/?page{page}'
            yield scrapy.Request(url, callback=self.parse_pages)

    def parse_pages(self, response, **kwargs):
        for href in response.xpath('//*[@class="item-box"]//a[1]/@href').extract():
            print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",href)
            url = response.urljoin(href)
            print("urrrrrrrrrrrrrrrrrr",url)
            yield scrapy.Request(url, callback=self.parse)

    def parse(self,response,**kwargs):
        conn =   myconnmy()
        cur = conn.cursor()
        paterrn = r'(magnet:\?xt=urn:btih):([a-zA-Z0-9]+)'
        global res

        url= response.request.url
        # size = response.xpath('//tr[@class="gai"]//td[3]/text()').extract()
        # razdayt = response.xpath('//td[@align="center"]//span[1]/text()').extract()
        # kachayt = response.xpath('//td[@align="center"]//span[2]/text()').extract()
        # title = response.xpath('//*[@id="index"]//a[3]/text()').extract()
        # magnet = response.xpath('//*[@id="index"]//a[2]/@href').extract()
        # created = datetime.now().strftime("%Y-%m-%d")
        # #info_hash = re.search(paterrn,response.xpath('//*[@id="index"]//a[2]/@href').extract())
        # for zurl,zsize,ztitle,zmagnet,zrazdayt,zkachayt in zip(url,size,title,magnet,razdayt,kachayt):
        #     item = {
        #         'url': response.url,
        #         'magnet': zmagnet,
        #         'title': ztitle,
        #         #'image': response.xpath('//*[@id="details"]//img/@src').extract_first(),
        #         #'descrypt': response.xpath('//*[@id="details"]/tbody/tr[1]/td[2]/text()[8]').extract_first(),
        #         'created':datetime.now().strftime("%Y-%m-%d"),
        #         'razdayt': zrazdayt,
        #         'kachayt': zkachayt,
        #         'info_hash': re.search(paterrn,zmagnet).group(2),
        #         'size':zsize


        #     }
        file_url = response.xpath('//*[@class="dowmn_l"]//a[1]/@href').get()
        file_url = response.urljoin(file_url)

        item = {
           'url':response.url,
           'file_url':file_url
        }


            ####################created#####################
            #cur.execute('''INSERT INTO droidfilms(title,url,seeds,peers,magnet,created,updated,info_hash,size) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],item['created'],item['created'],item['info_hash'],item['size']))
            #conn.commit()
            ####################updated#####################

            #cur.execute('''UPDATE  rutor SET title=%s,url=%s,seeds=%s,peers=%s,magnet=%s,updated=%s,info_hash=%s,size=%s WHERE id = %s''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],item['created'],item['info_hash'],item['size'],res))
            #conn.commit()
            ####################################################
        res +=1
        yield item
