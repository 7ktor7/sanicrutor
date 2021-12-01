from sanic import Sanic,response
from sanic.response import json, html, text
from models import myconn
from jinja2 import Environment, PackageLoader, select_autoescape
import asyncio
from tmbdapi import get_movie
import re
from datetime import datetime,timedelta
import pdb
from urllib.parse import urlparse, urlunsplit, unquote

env = Environment(loader=PackageLoader('app', 'templates'), autoescape=select_autoescape(['html', 'xml', 'tpl']), enable_async=True)


app = Sanic(__name__)
app.static('/static', './static')




async def template(tpl, **kwargs):

    template = env.get_template(tpl)
    content = await template.render_async(kwargs)
    return html(content)

async def temptext(tpl, **kwargs):

    temptext = env.get_template(tpl)
    content = await temptext.render_async(kwargs)
    return text(content,content_type="application/xml")


@app.route('/search/',methods=['GET','POST'])
async def search(request):
    

    
    q = request.form.get('q')
    if q != None:
        
        conn = await myconn()

        value = await conn.fetch(f"SELECT COUNT(*) FROM rutor WHERE title LIKE '%{q}%'")
        rowsmy = await conn.fetch(f"SELECT * FROM rutor WHERE title  LIKE '%{q}%' ORDER BY id LIMIT 200")
        total = value[0][0]
        await conn.close()
        print("Q",total,rowsmy,"QQQQQQQQQQQQQQQQQQQQQQQQ")
        content = await template('search.html', title='Sanic',total=total, rows=rowsmy)
        return content
    
    
    

@app.route('/',methods=['GET','POST'])
async def index(request):
    
    offset = request.args.get('page')
    if offset:
 
    
        myint = int(offset+'0'+'0')
    else:
        offset = '0'
        myint = int(offset)
    try:          
        conn = await myconn()

        value = await conn.fetch('SELECT COUNT(*) FROM rutor')
        
        rows = await conn.fetch('SELECT * FROM rutor ORDER BY id LIMIT 100 OFFSET $1',myint)
        total = value[0][0]
        await conn.close()
        
        content = await template('index.html', title='Sanic',total=total, rows=rows)
        return content
    except (OSError,ConnectionRefusedError) as e:        
    
        content = await template('index.html', title='Sanic')
        return content    

@app.route('/<slug>')
async def detail (request,slug):
    ret = {}
    pattern = r'([А-Яа-я0-9].+?)([\/?\.?\(\)?\[\]?])'
    conn = await myconn()
    
    row = await conn.fetchrow('SELECT * FROM rutor WHERE info_hash = $1',slug)

   
    
    
    query = re.search(pattern,row['title']).group(1)
    print("query==",query)

    vote_average,original_title,overview,poster_path = await get_movie(query)
    
    ret['nazvanie'] = original_title
    ret['vote'] = vote_average
    ret['opisanie'] = overview
    ret['image'] = poster_path
    content = await template('detail.html',row=row,ret=ret)
    await conn.close()
    return content


###################sitemap dinamic

@app.route('/sitemap.xml', methods=['GET'])
async def sitemap(request):
    conn = await myconn()
    pages = []

   
    posts =  await conn.fetch('SELECT * FROM rutor ORDER BY id LIMIT 10000')
    for post in posts:
        url = 'www.videofilms.cf' + app.url_for('detail', slug=post['info_hash'])
        last_updated = post['updated']
        pages.append([url, last_updated])

    content= await temptext('sitemap.xml',pages=pages)
    
    return content


if __name__ == "__main__":
    app.run(port='8001',debug=True)
