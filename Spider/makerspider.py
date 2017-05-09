# coding=utf-8
import scrapy
import MySQLdb
import re
import time
from random import randint

class makerSpider(scrapy.Spider):
    name = "makerspider"
    scheme = 'dmm18_all'
    count = 0

    user_agent_list = [ \
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",
        "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 "
        "(KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 "
        "(KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 "
        "(KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 "
        "(KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",
        "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 "
        "(KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",
        "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 "
        "(KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
    ]

    def start_requests(self):
        # urls = self.retrieve_links("SELECT link from %s.maker_links"%self.scheme)# 255334/274552
        # makers_dvd = self.retrieve_links("SELECT id from %s.maker_links"%self.scheme)
        # makers = self.retrieve_links("SELECT distinct(maker) from %s.videos"%'dmm18')
        # all_makers = set(makers+makers_dvd) # 266676/274552   258111/264763
        # labels = self.retrieve_links("SELECT distinct(label) from %s.videos"%'dmm18')
        # self.log(len(all_makers))

        # urls = [('http://www.dmm.co.jp/mono/dvd/-/maker/=/keyword=a/','maker_links')]
        # urls = [('http://www.dmm.co.jp/digital/videoa/-/list/=/limit=120/sort=date/','video_links'),
        #         ('http://www.dmm.co.jp/mono/dvd/-/list/=/limit=120/list_type=release/sort=date/','dvd_links'),
        #         ('http://www.dmm.co.jp/digital/videoc/-/list/=/limit=120/sort=date/','amateur_links')]
        # self.log(len(makers))
        # self.log(len(labels))
        # makers_url = ['http://www.dmm.co.jp/digital/videoa/-/list/=/article=maker/id=%s/limit=120/'
        #               %maker for maker in makers if maker!=""]
        # labels_url = ['http://www.dmm.co.jp/digital/videoa/-/list/=/article=label/id=%s/limit=120/'
        #               %label for label in labels if label!=""]
        # all_makers_url = ['http://www.dmm.co.jp/mono/dvd/-/list/=/article=maker/id=%s/limit=120/'
        #               %maker for maker in all_makers if maker!=""]
        # self.log(len(all_makers_url))
        # self.log(len(makers_url))
        # self.log(len(labels_url))
        # self.log(makers_url[0])
        # self.log(labels_url[0])
        # dvd_test = ['http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=13dsvr00004/',
        #             'http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=miae00011/',
        #             'http://www.dmm.co.jp/digital/videoa/-/detail/=/cid=snis00872/?i3_ref=list&i3_ord=19',
        #             'http://www.dmm.co.jp/mono/dvd/-/detail/=/cid=h_491love349/']

        # maker_test = ['http://www.dmm.co.jp/mono/dvd/-/list/=/article=maker/id=2661/limit=120/',
        #               'http://www.dmm.co.jp/mono/dvd/-/list/=/article=maker/id=46346/limit=120/']
        calendar = list()
        for year in range(1990,2020,1):
            for month in range(1,13,1):
                calendar.append('http://www.dmm.co.jp/mono/dvd/-/calendar/=/month=%d/year=%d/day=1-/'%(month,year))
        calendar_test = ['http://www.dmm.co.jp/mono/dvd/-/calendar/=/month=5/year=2016/day=1-/']
        for url in calendar:
            request = scrapy.Request(url=url,

                                     callback=self.countCalendar)
            request.meta['table'] = 'dvd_links'
            yield request
            time.sleep(2)


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
            except (MySQLdb.Error, MySQLdb.Warning) as e:
                db.rollback()
                self.log('[INSERT FAIL] %s' % log_list[i])
                self.log(e)

        db.close()

    def parse_video_info(self, response):
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
            extract_first()
        performers = response.xpath(u'//*[contains(text(),"出演者：")]/following-sibling::td/span[@id="performer"]/a/@href'). \
            extract()
        director = response.xpath(u'//*[contains(text(),"監督：")]/following-sibling::td/a/@href'). \
            extract_first()
        series = response.xpath(u'//*[contains(text(),"シリーズ：")]/following-sibling::td/a/@href'). \
            extract_first()
        maker = response.xpath(u'//*[contains(text(),"メーカー：")]/following-sibling::td/a/@href'). \
            extract_first()
        label = response.xpath(u'//*[contains(text(),"レーベル：")]/following-sibling::td/a/@href'). \
            extract_first()
        genre = response.xpath(u'//*[contains(text(),"ジャンル：")]/following-sibling::td/a/@href'). \
            extract()
        vr = response.xpath(u'//*[contains(text(),"コンテンツタイプ：")]/following-sibling::td/text()'). \
            extract_first()
        identifier = response.xpath(u'//*[contains(text(),"品番：")]/following-sibling::td/text()'). \
            extract_first()
        img = response.css('div#sample-video img::attr(src)').extract_first()
        onclick = response.css('a.d-btn ::attr(onclick)').extract_first()
        sample_img = response.css('div#sample-image-block img ::attr(src)').extract()
        sample_img_l = [self.find_img_src(img) for img in sample_img]
        # info = (title,favorite,type,delivery_date,release_date,duration,performers,
        #         director,series,maker,label,genre,vr,identifier,img,onclick,sample_img,sample_img_l)
        # for e in info:
        #     print e

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
        onclick = response.css('a.d-btn ::attr(onclick)').extract_first()
        # self.log(onclick)
        link = re.search(r'\(\'(.+)\'\)', onclick).group(1)
        # self.log(link)
        if link != None:
            yield scrapy.Request(url='http://www.dmm.co.jp' + link, callback=self.find_video_src)

    def find_video_src(self, response):
        iframe_src = response.css('*')[2].css('::attr(src)').extract_first()
        if iframe_src != None:
            yield scrapy.Request(url=iframe_src, callback=self.parse_video_src)

    def parse_video_src(self, response):
        js = response.css('*')[0].css('script ::text').extract_first()
        if js != None:
            param = max(js.split('\n'), key=len)
            param = param.replace('\\', '')
            videos = re.findall(r'bitrate\"\:(\d+),\"src\":\"(http:\/\/[a-zA-Z0-9\.\/_]+)', param)
            for video in videos:
                self.log('[SampleV] %s %s' % (video[0], video[1]))