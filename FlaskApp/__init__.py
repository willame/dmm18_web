# coding=utf-8
from flask import Flask,redirect,request
import MySQLdb
import re

from jinja2 import Environment, PackageLoader, select_autoescape
env = Environment(
    loader=PackageLoader('FlaskApp', 'templates'),
    autoescape=select_autoescape(['html', 'xml'])
)


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
    return app.send_static_file('index.html')

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

@app.route('/dvd/<cid>')
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
        html = template.render(info=result[0],img_l = find_img_src(result[0]["img"]),sample_videos = sample_videos,
                               sample_imgs=sample_imgs)
        db.close()
        return html
    elif len(result)>1:
        db.close()
        return "duplicate cid"

    else:
        db.close()
        return "no dvd ",cid

@app.route('/dvd/search/key=<key>')
def search(key):

    # connect to database
    db = MySQLdb.connect(host="localhost",  # your host, usually localhost
                         user="root",  # your username
                         passwd="666666",  # your password
                         db="dmm18_all",  # name of the data base
                         charset='utf8')  #
    cur = db.cursor(MySQLdb.cursors.DictCursor)
    if re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key) and len(key)>=5:
        letters = re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key).group(1)
        numbers = re.search(r'([a-zA-z]+)[-:blank:]*(\d+)',key).group(2)
        # msg=u"关键字 %s"%key
        # if len(letters)+len(numbers)<5:
        #     msg = u"关键字过短 %s"%key

        cur.execute("SELECT * FROM dvds WHERE cid REGEXP '.*(%s).*(%s).*' LIMIT 500"%(letters,numbers))
        results = cur.fetchall()
        template = env.get_template("search_result.html")
        html = template.render(results= results, msg="")
        db.close()
        return html

    else:
        db.close()
        return u"番号格式不正确"

@app.route('/top/page=<page>')
@app.route('/top')
def top(page=None):

    itemsPerPage=25
    maxPage = 500/25

    if page == None or  not page.isdigit():
        # connect to database
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM dvds ORDER BY rate*rate_num DESC LIMIT %d OFFSET %d" % (itemsPerPage, 0))
        results = cur.fetchall()
        template = env.get_template("search_result.html")
        html = template.render(results=results, msg="")
        db.close()
        return html
    elif int(page)<=maxPage:
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        cur.execute("SELECT * FROM dvds ORDER BY rate*rate_num DESC LIMIT %d OFFSET %d" % (itemsPerPage,
                                                                                           itemsPerPage*min([int(page)-1,20]) ))
        results = cur.fetchall()
        template = env.get_template("search_result.html")
        html = template.render(results=results, msg="")
        db.close()
        return html
    else:
        # template = env.get_template("search_result.html")
        # html = template.render(results=[], msg="超出最大页数")
        return u"超出最大页数"

@app.route('/actor/id=<id>')
def actor(id=None):

    if id==None:
        # template = env.get_template("search_result.html")
        # html = template.render(results=[], msg="错误演员编号")
        return u"错误演员编号"
    elif not id.isdigit() or len(id)<4:
        return u"错误演员编号"
    else:
        db = connectDB()
        cur = db.cursor(MySQLdb.cursors.DictCursor)
        # print "SELECT * FROM dvds WHERE performers REGEXP \'[|]*%s[|]*\' ORDER BY release_date DESC"%id
        cur.execute("SELECT * FROM dvds WHERE performers REGEXP \'^[|]*%s[|]*$\' ORDER BY release_date DESC"%id)

        results = cur.fetchall()
        if len(results)>0:
            cur.execute("SELECT name1,name2 FROM stars1 WHERE id=\'%s\'"%id)
            name = cur.fetchall()
            if len(name) == 1:
                msg = u"%s (%s)"%(name[0]["name1"],name[0]["name2"])
            else:
                msg = u"未知"
            template = env.get_template("search_result.html")
            html = template.render(results=results, msg=msg)
            db.close()
            return html
        else:
            return u"没有 %s"%id

if __name__ == "__main__":
    app.run()
