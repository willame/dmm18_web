# coding=utf-8
import scrapy
import MySQLdb
import re
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import logging
import time
from random import randint

class makerSpider(scrapy.Spider):
    name = "dvdspider"
    scheme = 'dmm18_all'
    countFailure = 0

    # user_agent_list = [ \
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
    #     "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
    #     "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
    #     "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
    #     "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
    #     "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
    #     "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
    #     "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
    #     "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
    #     "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    #     "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
    #     "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
    #     "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
    #     "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
    #     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
    #     "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
    #     "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    # ]

    def start_requests(self):
        # urls = self.retrieve_links("SELECT link from %s.dvd_links"%self.scheme)# 255334/274552
        # len(urls)
        dvd_test = ['http://www.dmm.co.jp/mono/dvd/-/detail/=/cid=104fsmd30/'
                    ]
        for url in dvd_test:
            request = scrapy.Request(url=url,callback=self.parse_video_info)
            request.meta['table'] = 'dvd_info'
            yield request
            # time.sleep(2)


    def parse_maker_page(self, response):
        # extract alphabet links
        alphabet_links = response.css('table.menu_aiueo td a::attr(href)').extract()
        # make new requests
        # self.log(len(alphabet_links))
        for url in alphabet_links:
            if not re.match(r'http:\/\/www\.dmm\.co\.jp', url):
                url = 'http://www.dmm.co.jp' + url
            # self.log("[PAL] " + url)
            request = scrapy.Request(url=url, callback=self.parse_maker_link)
            request.meta['table'] = response.meta['table']
            yield request

    def parse_maker_link(self, response):
        maker_links = response.css(u'table[summary="おすすめメーカー"] div.maker-text a::attr(href)').extract()
        maker_links += response.css(u'table[summary="メーカー一覧リスト"] a::attr(href)').extract()
        query_list = list()
        log_list = list()
        for maker_link in maker_links:
            if not re.match(r'http:\/\/www\.dmm\.co\.jp',maker_link):
                maker_link = 'http://www.dmm.co.jp'+maker_link
                if re.search(r'\/id=(.+)\/', maker_link):
                    id = re.search(r'\/id=(.+)\/', maker_link).group(1)
                    # self.log(id)
                    query = "INSERT INTO %s.%s(id,link) VALUES(\'%s\',\'%s\')"%(self.scheme, response.meta['table'],
                                                                                id, maker_link)
                    log = "[MAKER] %s"%id
                    query_list.append(query)
                    log_list.append(log)
                    # self.log(query)
        # self.log(len(maker_links))
        self.insert_data(query_list, log_list)

    def parse_video_pages(self, response):
        # parse the first page
        self.parse_video_links(response)
        # extract page number
        pages = response.css('div.list-boxcaptside.list-boxpagenation li a::attr(href)')
        # find last page
        if len(pages) > 0:
            last_page = max([int(page.re(r'page=(\d+)')[0]) for page in pages])
        else:
            last_page = 1
        # send new requests
        for page in range(1, last_page + 1, 1):
            if page != 1:
                url = response.url + 'page=%d/' % page
                # self.log("[PVP] " + url)
                request = scrapy.Request(url=url, callback=self.parse_video_links)
                request.meta['table'] = response.meta['table']
                yield request

    def parse_video_links(self, response):
        video_links = response.css('p.tmb a::attr(href)').extract()
        query_list = list()
        log_list = list()
        for video_link in video_links:
            if re.search(r'\/cid=(.+)\/', video_link):
                cid = re.search(r'\/cid=(.+)\/', video_link).group(1)
                query = "INSERT INTO %s.%s(cid,link) VALUES(\'%s\',\'%s\')"\
                        %(self.scheme,response.meta['table'],cid,video_link)
                log = '[LINK] %s'%cid
                query_list.append(query)
                log_list.append(log)
                # self.log(log)

        # self.log(len(query_list))
        self.insert_data(query_list, log_list)

    def countVideos(self, response):
        id = re.search(r'\/id=(.+)\/', response.url).group(1)
        num = response.css('div.list-boxcaptside.list-boxpagenation p:first-child ::text').re(r'^([\d,]+)')
        if num != None:
            num = int(num[0].replace(',',''))
            self.count+=num
            self.log(self.count)

    def countCalendar(self, response):
        self.count += len(response.css('td.title-monocal a[href]'))
        self.log(self.count)
    ###
    def insert_data(self, query_list, log_list):
        # connect to database
        db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                                 user="root",  # your username
                                 passwd="666666",  # your password
                                 db="dmm18_all",  # name of the data base
                                 charset='utf8')  #

        cur = db.cursor()

        for i in range(0, len(query_list), 1):
            try:
                 # self.log(query_list[i])
                cur.execute(query_list[i])
                db.commit()
                self.log('[INSERT SUCCESS] %s' % log_list[i])
                # logging.INFO('[INSERT SUCCESS] %s' % log_list[i])
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                db.rollback()
                # logging.WARNING('[INSERT FAIL] %s' % log_list[i])
                self.log('[INSERT FAIL] %s' % log_list[i])
                self.log(e)

        db.close()

    def parse_video_info(self, response):
        cid = re.search(r'\/cid=(.+)\/',response.url).group(1)
        title = response.css('h1#title ::text').extract_first()
        favorite = response.xpath(u'//*[contains(text(),"お気に入り登録数")]/span/span/text()').\
            extract_first()
        type = response.xpath(u'//*[contains(text(),"種類：")]/following-sibling::td/text()').\
            extract_first()
        delivery_date = response.xpath(u'//*[contains(text(),"配信開始日：")]/following-sibling::td/text()').\
            extract_first()
        release_date = response.xpath(u'//*[contains(text(),"発売日：")]/following-sibling::td/text()').\
            extract_first()
        duration = response.xpath(u'//*[contains(text(),"収録時間：")]/following-sibling::td/text()'). \
            re(r'(\d+)')
        performers = response.xpath(u'//*[contains(text(),"出演者：")]/following-sibling::td/span[@id="performer"]/a/@href'). \
            re(r'\/id=(\d+)\/')
        director = response.xpath(u'//*[contains(text(),"監督：")]/following-sibling::td/a/@href'). \
            re(r'\/id=(\d+)\/')
        series = response.xpath(u'//*[contains(text(),"シリーズ：")]/following-sibling::td/a/@href'). \
            re(r'\/id=(\d+)\/')
        maker = response.xpath(u'//*[contains(text(),"メーカー：")]/following-sibling::td/a/@href'). \
            re(r'\/id=(\d+)\/')
        label = response.xpath(u'//*[contains(text(),"レーベル：")]/following-sibling::td/a/@href'). \
            re(r'\/id=(\d+)\/')
        genre = response.xpath(u'//*[contains(text(),"ジャンル：")]/following-sibling::td/a/@href'). \
            re(r'\/id=(\d+)\/')
        vr = response.xpath(u'//*[contains(text(),"コンテンツタイプ：")]/following-sibling::td/text()'). \
            extract_first()
        identifier = response.xpath(u'//*[contains(text(),"品番：")]/following-sibling::td/text()'). \
            extract_first()
        img = response.css('div#sample-video img::attr(src)').extract_first()
        onclick = response.css('a.d-btn ::attr(onclick)').re(r'\(\'(.+)\'\)')
        sample_imgs = response.css('div#sample-image-block img ::attr(src)').extract()
        sample_imgs_l = [self.find_img_src(img2) for img2 in sample_imgs]
        # parse rate and reviews
        if len(response.css('p.d-review__average strong::text')) > 0:
            rate = response.css('p.d-review__average strong::text').re(r'\d*\.?\d*')[0]
        else:
            rate = 0
        rate_num = response.css('p.d-review__evaluates strong::text').extract_first()
        if len(response.css('p.d-review__evaluates ::text')) > 0:
            reviews = response.css('p.d-review__evaluates ::text').re(r'(\d+)')[1]
        else:
            reviews = 0
        info = (cid,title,favorite,type,delivery_date,release_date,duration,performers,
                director,series,maker,label,genre,vr,identifier,img,onclick,sample_imgs,sample_imgs_l)
        # self.log("%s,%s,%s"%(rate,rate_num,reviews))
        for e in info:
            print e
        if len(onclick)>0:
            link = 'http://www.dmm.co.jp'+onclick[0]
            # self.log(link)
            request = scrapy.Request(url=link, callback=self.find_video_src)
            request.meta["cid"] = cid
            yield request
            #self.find_sample_video_link(response)

        if delivery_date == None:
            delivery_date = "0001-01-01"
        if favorite == None:
            favorite = 0
        if rate_num == None:
            rate_num = 0
        if duration == None:
            duration = 0
        performers = '|'.join(performers)
        genre = '|'.join(genre)
        duration = '|'.join(duration)
        director = '|'.join(director)
        maker = '|'.join(maker)
        label = '|'.join(label)
        series = '|'.join(series)
        query = "INSERT INTO %s.dvds(cid,title,favorite,dvd_type,delivery_date,release_date,duration,performers,\
                director,series,maker,label,genre,vr,identifier,img,reviews,rate,rate_num) \
                VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"\
        %(self.scheme,cid,title,favorite,type,delivery_date,release_date,duration,performers,\
                director,series,maker,label,genre,vr,identifier,img,reviews,rate,rate_num)
        self.insert_data([query],['DVD %s'%cid])
        query_list = list()
        log_list = list()
        for sample_img in sample_imgs:
            query2 = "INSERT INTO %s.sample_img_links(cid,link) VALUES(\'%s\',\'%s\')"%(self.scheme,cid,sample_img)
            # self.insert_data([query2], [''])
            query_list.append(query2)
            log_list.append('[S IMG] %s'%cid)
        # self.insert_data(query_list,log_list)
        # print query2


            # parse reviewers and reviews
        if reviews != 0:
            request = scrapy.FormRequest("http://www.dmm.co.jp/review/-/list/ajax-list/",
                                             callback=self.parse_reviewer, \
                                             formdata={'cid': cid, 'page': str(1), 'limit': reviews,
                                                       'sort': 'yes_desc'})
            request.meta['cid'] = cid
            yield request


    def retrieve_links(self, query):
        # connect to database
        db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                             user="root",  # your username
                             passwd="666666",  # your password
                             db="dmm18",  # name of the data base
                             charset='utf8')  #

        cur = db.cursor()
        cur.execute(query)
        links = [row[0] for row in cur.fetchall()]
        self.log('[RETRIEVE LINKS] %d' % len(links))
        db.close()
        return links

        # find the src url of large picture

    def find_img_src(self, src):
        if re.search(r'(p[a-z]\.)jpg', src):
            return src.replace(re.search(r'(p[a-z]\.)jpg', src).group(1), 'pl.')
        elif re.search(r'/consumer_game/', src):
            return src.replace('js-', '-')
        elif re.search(r'js\-([0-9]+)\.jpg$', src):
            return src.replace('js-', 'jp-')
        elif re.search(r'ts\-([0-9]+)\.jpg$', src):
            return src.replace('ts-', 'tl-')
        elif re.search(r'(\-[0-9]+\.)jpg$', src):
            return src.replace(re.search(r'(\-[0-9]+\.)jpg$', src).group(1),
                               'jp' + re.search(r'(\-[0-9]+\.)jpg$', src).group(1))
        else:
            return src.replace('-', 'jp-')

    def find_sample_video_link(self, response):
        self.log('123123')
        onclick = response.css('a.d-btn ::attr(onclick)').extract_first()
        # self.log(onclick)
        link = re.search(r'\(\'(.+)\'\)', onclick).group(1)
        self.log(link)
        if link != None:
            yield scrapy.Request(url='http://www.dmm.co.jp' + link, callback=self.find_video_src)

    def find_video_src(self, response):
        iframe_src = response.css('*')[2].css('::attr(src)').extract_first()
        if iframe_src != None:
            self.log(iframe_src)
            request = scrapy.Request(url=iframe_src,
                                 callback=self.parse_video_src)
            request.meta["cid"] = response.meta["cid"]
            yield request

    def parse_video_src(self, response):

        js = response.css('*')[0].css('script ::text').extract_first()
        if js != None:
            query_list = list()
            log_list = list()
            param = max(js.split('\n'), key=len)
            param = param.replace('\\', '')
            videos = re.findall(r'bitrate\"\:(\d+),\"src\":\"(http:\/\/[a-zA-Z0-9\.\/_]+)', param)
            for video in videos:

                # self.log(log)
                cid = response.meta["cid"]
                log = '[S VIDEO] %s %s' % (video[0], cid)
                query = "INSERT INTO %s.sample_video_links(cid, link, bitrate) VALUES(\'%s\',\'%s\',\'%s\')"%(self.scheme,cid,video[1],video[0])
                # self.insert_data([query],[''])
                query_list.append(query)
                log_list.append(log)
            # self.insert_data(query_list,log_list)

    # store reviewer id, name and review into database
    def parse_reviewer(self,response):
        cid= response.meta['cid']
        query_list = list()
        log_list = list()
        query_list2 = list()
        log_list2 = list()
        reviews = response.css('div.d-review__with-comment li.d-review__unit')

        for review in reviews:
            reviewer = review.css('span.d-review__unit__reviewer a')
            link = reviewer.css('::attr(href)').extract_first()
            id = reviewer.css('::attr(href) ').re(r'\/id=(\d+)\/')[0]
            name =  reviewer.css('::text').extract_first()
            # self.log('[REVIEWER] %s %s'%(id,name))
            query = "INSERT INTO %s.reviewers(id,name,link) VALUES(\'%s\',\'%s\',\'%s\')"%(self.scheme,id,name,link)
            query_list.append(query)
            log_list.append('[REVIEWER] %s %s'%(id,name))

            title = review.css('span.d-review__unit__title ::text').extract_first()
            content = "|".join(review.css('div.d-review__unit__comment ::text').extract())
            rate = review.css('p:first-child span:first-child ::attr(class)').re(r'(\d)')[0]
            postdate = review.css('span.d-review__unit__postdate ::text').extract_first()[1:]
            service = review.css('span.d-review__unit__service ::text').extract_first()[1:]
            votes = review.css('p.d-review__unit__voted ::text').re(r'(\d+)')[0]
            useful = review.css('p.d-review__unit__voted strong::text').re(r'(\d+)')[0]

            # print title
            # print content
            # print rate
            # print postdate
            # print service
            # print votes
            # print useful

            query2 = "INSERT INTO %s.reviews(cid,id,title,content,rate,postdate,service,votes,useful)"\
                "VALUES(\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\',\'%s\')"%(self.scheme,cid,id,\
                    title,content,rate,postdate,service,votes,useful)

            query_list2.append(query2)
            log_list2.append('[REVIEW CONTENT] %s %s'%(cid,id))

        # # insert reviewer info into data base
        # self.insert_data(query_list, log_list)
        #
        # # insert reviews into database
        # self.insert_data(query_list2, log_list2)






if __name__ == "__main__":
    process = CrawlerProcess(get_project_settings())
    process.crawl('dvdspider')
    process.start()  # the script will block here until the crawling is finished