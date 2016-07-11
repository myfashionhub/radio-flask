from flask import render_template, redirect, request
import logging
from url_shortener import app
from application import RegexConverter, sanitize_device
from database import Database


app.url_map.converters['regex'] = RegexConverter
app.jinja_env.filters['sanitize_device'] = sanitize_device
db = Database(app.config['DATABASE_URL'])
domain = app.config['DOMAIN']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    target_url  = request.form.get('url')
    key         = request.form.get('key')
    device_type = request.form.get('device_type')

    if key == None:
        link = db.find_or_create_short_url(target_url)
    else:
        link = db.add_target(key, target_url, device_type)

    return redirect('/link/'+link.key)

@app.route('/<regex("[a-zA-Z0-9]{6}"):key>/')
def redirect_to_target(key):
    link = db.query_target(request.user_agent, key)
    if link == None:
        return render_template('404.html')
    else:
        db.save_click(link.id, request.referrer)
        return redirect(link.target_url)

@app.route('/links')
def links():
    links = db.all_links()
    return render_template('links.html', links=links, domain=domain)

@app.route('/link/<regex("[a-zA-Z0-9]{6}"):key>/')
def show_link(key):
    short_url = domain + key
    results   = db.get_links_with_clicks(key)

    if len(results) == 0:
        return render_template('404.html')
    else:
        return render_template(
                  'link.html', results=results, short_url=short_url
               )
