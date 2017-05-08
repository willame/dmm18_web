# dmm18_web 需要完成的任务，有不清楚的可以讨论
09.05.2017
A.买域名，直接上线

A.（爬虫可以参考makerspider）爬取制片商，发行商，导演名字，制作3张新表。
  制片商信息 http://www.dmm.co.jp/mono/dvd/-/maker/
  格式 |id|name|link| id为主键
  
   
A.制作新爬虫，发行商和导演没有具体网站需要替换url中<id>爬取名字，<id>可以从dmm18_all.dvds和dmm18-database（Github）中的videos表提取
    http://www.dmm.co.jp/mono/dvd/-/list/=/article=director/id=<id>/
    http://www.dmm.co.jp/mono/dvd/-/list/=/article=label/id=<id>/
    格式 |id|name|link| id为主键
    
A.制作新爬虫，爬取dmm18影片分类，制作1张新表
  http://www.dmm.co.jp/mono/dvd/-/genre/
  格式  |id|name|link| id为主键
  
A.制作新爬虫，爬取dmm18影片系列，制作1张新表
  http://www.dmm.co.jp/mono/dvd/-/series/=/sort=ruby/
  格式 |id|name|link| id为主键
  
A.（爬虫可以参考dvdspider）爬取-1，0，+1，+2 月发行的影片(0 代表当月)，
  建立一张新表，格式参考 dmm18_all.dvds，这张表作为辅助表用来补充数据库，
  因为尚未发行的影片在网页布局，日期格式上有可能有问题
  
  http://www.dmm.co.jp/mono/dvd/-/calendar/=/day=1-/
 

A.爬取dmm8 动画上的影片信息，大约25万部，制作一张新表，表的格式参照dmm18.dvds
  （已经有现成爬虫，不用重新编程）

A.分类演员（根据什么分类？），制作花名册

A.推荐系统

A.加入用户系统

A.建论坛
