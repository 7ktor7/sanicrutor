import scrapy
from datetime import datetime
import re
from mypayk.spiders.modelsmy import myconnmy
from scrapy.linkextractors.lxmlhtml import LxmlLinkExtractor
from scrapy.spiders import Rule
from itertools import zip_longest

res = 1


class RutorSpider(scrapy.Spider):
    name = 'rutor'
    allowed_domains = ['rutor.info']
    start_urls = ['http://rutor.info/search/0/0/000/0/%D0%9A%D0%9F%D0%9A']
    # rules = (
    #             Rule(LxmlLinkExtractor(allow=('/search/.*', )), callback='parse_pages', follow=True),
                
    #     )
    pages_count = 18
    def start_requests(self):
        for page in range(0, 1 + self.pages_count):
            url = f'http://rutor.info/search/{page}/0/000/0/%D0%9A%D0%9F%D0%9A'
            yield scrapy.Request(url, callback=self.parse_pages)

    # def parse_pages(self, response, **kwargs):
    #     for href in response.xpath('//*[@id="index"]//a[3]/@href').extract():
    #         print("hhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhhh",href)
    #         url = response.urljoin(href)
    #         print("urrrrrrrrrrrrrrrrrr",url)
    #         yield scrapy.Request(url, callback=self.parse)

    def parse_pages(self,response,**kwargs):
        conn =   myconnmy()
        cur = conn.cursor()
        paterrn = r'(magnet:\?xt=urn:btih):([a-zA-Z0-9]+)'
        global res
        item = {}
        url= response.request.url
        print("uuuuuuuuuuuuuuuuu",url)
        size = response.xpath('//tr[@class="gai"]//td[3]/text()').extract()
        razdayt = response.xpath('//td[@align="center"]//span[1]/text()').extract()
        kachayt = response.xpath('//td[@align="center"]//span[2]/text()').extract()
        gai = response.xpath('//*[@class="gai"]//a/text()').extract()
        tum = response.xpath('//*[@class="tum"]//a/text()').extract()
        magai = response.xpath('//*[@class="gai"]//a[2]/@href').extract()
        matum = response.xpath('//*[@class="tum"]//a[2]/@href').extract()
        title = [y for x in zip_longest(gai, tum) for y in x if y is not None]
        magnet = [y for x in zip_longest(magai, matum) for y in x if y is not None]
        
        created = datetime.now().strftime("%d-%m-%Y")
        print(magnet,"MMMMMMMMMMMMMM")
        for zurl,zsize,ztitle,zmagnet,zrazdayt,zkachayt in zip(url,size,title,magnet,razdayt,kachayt):
            print("zzzzzzzzzzz",zmagnet)
            item = {
                'url': response.url,
                'magnet': zmagnet,
                'title': ztitle,
                #'image': response.xpath('//*[@id="details"]//img/@src').extract_first(),
                #'descrypt': response.xpath('//*[@id="details"]/tbody/tr[1]/td[2]/text()[8]').extract_first(),
                'created':datetime.now().strftime("%d-%m-%Y"),
                'razdayt': zrazdayt,
                'kachayt': zkachayt,
                'info_hash': re.search(paterrn,zmagnet).group(2),
                'size':zsize


            }



            ####################created#####################
            #cur.execute('''INSERT INTO rutor(title,url,seeds,peers,magnet,created,updated,info_hash,size) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s)''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],item['created'],item['created'],item['info_hash'],item['size']))
            #conn.commit()
            ####################updated#####################

            cur.execute('''UPDATE  rutor SET title=%s,url=%s,seeds=%s,peers=%s,magnet=%s,updated=%s,info_hash=%s,size=%s WHERE id = %s''',(item['title'],item['url'],item['razdayt'],item['kachayt'],item['magnet'],created,item['info_hash'],item['size'],res))
            conn.commit()
            ####################################################
            res+=1
        yield item
