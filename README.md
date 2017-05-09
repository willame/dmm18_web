# dmm18_web 需要完成的任务，有不清楚的可以讨论
开发注意事项：<br />
1.用Flask开发网页，使用jinja2设立template方便以后网页布局的复用。<br />
  http://jinja.pocoo.org/docs/2.9/intro/#basic-api-usage<br />
  目前网站的基本模板是FlaskApp/templates中的base.html 。它包含顶部导航栏，中部左侧导航栏，中部中间内容注入区，中部右侧广告栏，底部导航栏。<br />
  （其他模板不清楚可以问我）<br />
  base.html 中可以注入的区域有<br />
  {% block title %} 浏览器页面标题<br />
  {%block custom_nav %} 额外的导航栏项目<br />
  {% block content %} 中间内容区域<br />
  {% block custom_js %} 额外js<br />
  {% block custom_css %} 额外css<br />
  {% block custom_css_2 %}额外css（这个block可能是多余的）<br />
  开发新页面时只需要新建的模板， 继承{% extends base.html%}，然后定义{%block xxx %}中的内容，然后用Flask输出新建的模板。<br />
  base.html 中已经包含了jquery和bootstrap不需要重新插入<br />
  
  2.爬虫的开发没有特别规定， 如果用scrapy开发可以参考复用dvdspider和maker的中的一些函数，<br />
    插入数据库，爬取解析影片详细信息，爬取日文50音图对应的每个页面的链接，爬取maker的链接<br />
    
09.05.2017


A.添加专栏页面？每周或更短间隔发表长篇AV评论。建立一个AV讨论，欣赏，爱好者社区？

A.制作新爬虫，为最热，最新，最想要影片（影片数量在500+500+500左右）爬取磁力链接，制作新表

格式| cid | link | cid和link为主键

A. 影片编号/品番号到真实番号的转换方法，例如 tktek001 -> tek001 , 9avop012 -> avop012

  转换的规则有很多

A.买域名，直接上线

A.（爬虫可以参考makerspider）爬取制片商，发行商，导演名字，制作3张新表。

  制片商信息 http://www.dmm.co.jp/mono/dvd/-/maker/
  
  格式 | id | name | link | id为主键
  
   
A.制作新爬虫，发行商和导演没有具体网站需要替换url中{id}爬取名字，{id}可以从 dmm18_all.dvds 和 dmm18-database（Github） 中的videos表提取

  http://www.dmm.co.jp/mono/dvd/-/list/=/article=director/id={id}/
    
  http://www.dmm.co.jp/mono/dvd/-/list/=/article=label/id={id}/
    
  格式 | id | name | link | id为主键
    
A.制作新爬虫，爬取dmm18影片分类，制作1张新表

  http://www.dmm.co.jp/mono/dvd/-/genre/
  
  格式  | id | name | link | id为主键
  
A.制作新爬虫，爬取dmm18影片系列，制作1张新表

  http://www.dmm.co.jp/mono/dvd/-/series/=/sort=ruby/
  
  格式 | id | name | link | id为主键
  
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
