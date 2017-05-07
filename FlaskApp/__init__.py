# coding=utf-8
from flask import Flask,redirect,request,url_for
import MySQLdb
import re
import math
from bs4 import BeautifulSoup

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('FlaskApp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)

itemsPerPage=25

def find_img_src( src):
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

def split_lst(lst,n):
    return [ lst[i::n] for i in xrange(n) ]

def returnError(msg):
    template = env.get_template("error.html")
    html = template.render(msg=msg)
    return html
#
# VALID_TAGS = ['strong', 'em', 'p', 'ul', 'li', 'br','/','*','%']
#
# def sanitize_html(value):
#
#     soup = BeautifulSoup(value)
#
#     for tag in soup.findAll(True):
#         if tag.name not in VALID_TAGS:
#             tag.extract()
#
#     return soup.renderContents()

def connectDB():
    # connect to database
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="666666",  # your password
                         db="dmm18_all",  # name of the data base
                         charset='utf8')  #
    return db

app = Flask(__name__,static_url_path='/static')

app.debug = True
@app.route('/')
def index():
    # return app.send_static_file('index.html')
    template = env.get_template("index.html")
    html = template.render()
    #
    return html

@app.route("/table")
def table():
    # connect to database
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="666666",  # your password
                         db="dmm18_all",  # name of the data base
                         charset='utf8')  #
    cur = db.cursor()
    query2 = "SELECT table_name as 'name',TABLE_ROWS AS 'rows',round(((data_length + index_length) / 1024 / 1024), 2) as `Size in MB` from information_schema.TABLES where table_schema ='dmm18_all'"
    cur.execute(query2)
    counts = cur.fetchall()
    db.close()
    template = env.get_template("db_info.html")
    html = template.render(rows = counts)
    #
    return html

@app.route('/video/cid=<cid>')
def dvd(cid):
    # connect to database
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="666666",  # your password
                         db="dmm18_all",  # name of the data base
                         charset='utf8')  #
    cur = db.cursor(MySQLdb.cursors.DictCursor)

    # query = "SELECT * FROM dvds WHERE cid =\'%s\'"%cid
    cur.execute("SELECT * FROM dvds WHERE cid =\'%s\'"%cid)
    result = cur.fetchall()

    if len(result)==1:
        template = env.get_template("dvd.html")
        cur.execute("SELECT * FROM sample_video_links WHERE cid =\'%s\'"%cid)
        sample_videos = cur.fetchall()
        cur.execute("SELECT * FROM sample_img_links WHERE cid =\'%s\'" % cid)
        sample_imgs = cur.fetchall()

        dvd_js = url_for('static', filename='js/dvd_info.js')
        html = template.render(info=result[0],sample_videos = sample_videos,
                               sample_imgs=sample_imgs,dvd_js = dvd_js,post_img = find_img_src(result[0]['img']))
        db.close()
        return html
    elif len(result)>1:
        db.close()
        template = env.get_template("error.html")
        html = template.render(msg="duplicate cid")
        return html

    else:
        db.close()
        # template = env.get_template("error.html")
        # html = template.render(msg="no dvd "+cid)
        return returnError("no dvd "+cid)


@app.route('/search/key=<key>')
@app.route('/search/key=<key>/page=<page>')
def search(key,page=None):


    if re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key) and len(key)>=5:
        letters = re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key).group(1)
        numbers = re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key).group(2)
        # msg=u"关键字 %s"%key
        # if len(letters)+len(numbers)<5:
        #     msg = u"关键字过短 %s"%key
        if page == None or not page.isdigit():
            return redirect('/search/key=%s/page=1' % key, code=302)
        else:
            # connect to database
            db = connectDB()
            cur = db.cursor(MySQLdb.cursors.DictCursor)
            cur.execute("SELECT * FROM dvds WHERE identifier REGEXP '.*(%s).*(%s).*' LIMIT 500"%(letters,numbers))
            results = cur.fetchall()
            maxPage = int(math.ceil(1. * len(results) / itemsPerPage))
            if len(results) == 0:
                msg = u"没有结果"
            else:
                msg =''
            template = env.get_template("search_result.html")
            offset = itemsPerPage * min([int(page) - 1, maxPage - 1])
            html = template.render(results= results[offset:offset+itemsPerPage-1], msg=msg,page_num = maxPage)
            db.close()
            return html

    else:
        return returnError(u"番号格式不正确")


@app.route('/top/page=<page>')
@app.route('/top')
def top(page=None):

    # itemsPerPage=25
    maxPage = int(math.ceil(1.*500/itemsPerPage))

    if page == None or  not page.isdigit():
        return redirect("/top/page=1", code=302)
        # connect to database
        # db = connectDB()
        # cur = db.cursor(MySQLdb.cursors.DictCursor)
        # cur.execute("SELECT * FROM dvds ORDER BY rate*rate_num DESC LIMIT %d OFFSET %d" % (itemsPerPage, 0))
        # results = cur.fetchall()
        # template = env.get_template("search_result.html")
        # html = template.render(results=results, msg="",page_num=maxPage)
        # db.close()
        # return html
    else:
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM dvds ORDER BY rate*rate_num DESC LIMIT %d OFFSET %d" % (itemsPerPage,
                                                                                           itemsPerPage*min([int(page)-1,maxPage-1]) ))
        results = cur.fetchall()
        template = env.get_template("search_result.html")
        html = template.render(results=results, msg="",page_num=maxPage)
        db.close()
        return html
    # else:
    #     # template = env.get_template("search_result.html")
    #     # html = template.render(results=[], msg="超出最大页数")
    #     return redirect("/top/page=%d"%maxPage, code=302)

@app.route('/actor/id=<id>/page=<page>')
@app.route('/actor/id=<id>')
def actor(id=None,page=None):

    if id==None or not id.isdigit() or len(id)<4:
        # template = env.get_template("search_result.html")
        # html = template.render(results=[], msg="错误演员编号")
        return returnError(u"错误演员编号")

    elif page==None or not page.isdigit():
        return redirect('/actor/id=%s/page=1'%id, code=302)
    else:
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        # print "SELECT * FROM dvds WHERE performers REGEXP \'[|]*%s[|]*\' ORDER BY release_date DESC"%id
        # query = "SELECT ROW_NUMBER() OVER(ORDER BY release_date DESC) AS 'index',* FROM dvds WHERE performers REGEXP \'[|]*%s[|]*\'"
        cur.execute("SELECT * FROM dvds WHERE performers REGEXP \'[|]*%s[|]*\' ORDER BY release_date DESC"%id)
        # print "SELECT * FROM dvds WHERE performers REGEXP \'[|]*%s[|]*\' ORDER BY release_date DESC"%id
        results = cur.fetchall()

        if len(results)>0:
            maxPage = int(math.ceil(1.*len(results) / itemsPerPage))
            # if int(page)>maxPage:
            #     db.close()
            #     return redirect("/actor/id=%s/page=%d"%(id,maxPage), code=302)
            # print maxPage
            cur.execute("SELECT name1,name2 FROM stars1 WHERE id=\'%s\'"%id)
            name = cur.fetchall()
            if len(name) == 1:
                msg = u"%s (%s)"%(name[0]["name1"],name[0]["name2"])
            else:
                msg = u"未知"
            template = env.get_template("search_result.html")
            offset = itemsPerPage*min([int(page)-1,maxPage-1])
            # print offset
            html = template.render(results=results[offset:offset+itemsPerPage-1], msg=msg,page_num=maxPage)
            db.close()
            return html
        else:
            db.close()
            return returnError(u"没有 "+id)

@app.route('/actor/page=<page>')
@app.route('/actor')
def namebook(page=None):
    if page == None or  not page.isdigit():
        return redirect("/actor/page=1", code=302)
    else:
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        query = "SELECT TABLE_ROWS AS 'rows' from information_schema.TABLES where table_name='stars1'"
        cur.execute(query)
        maxPage = int(math.ceil(1. * cur.fetchall()[0]['rows'] / itemsPerPage))

        cur.execute("SELECT * FROM stars1 LIMIT %d OFFSET %d" % (itemsPerPage,itemsPerPage*min([int(page)-1,maxPage-1]) ))
        results = cur.fetchall()

        # template = env.get_template("search_result.html")
        # html = template.render(results=results, msg="",page_num=maxPage)
        db.close()
        return returnError(u"花名册开发中")


if __name__ == "__main__":
    app.run()
