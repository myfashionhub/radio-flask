from flask import render_template, redirect, request
import logging
from url_shortener import app
from application import RegexConverter, sanitize_device, valid_url
from database import Database


app.url_map.converters['regex'] = RegexConverter
app.jinja_env.filters['sanitize_device'] = sanitize_device

suffix = ''
if app.config['TEST_MODE']:
    suffix = '_TEST'

db = Database(app.config['DATABASE_URL%s' % suffix ])
base_url = app.config['BASE_URL%s' % suffix]

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/shorten', methods=['POST'])
def shorten():
    target_url  = request.form.get('url')
    key         = request.form.get('key')
    device_type = request.form.get('device_type')
    if not valid_url(target_url):
        return "Invalid target URL"

    if key == None:
        link = db.find_or_create_short_url(target_url)
    else:
        criteria = 'device_type:' + device_type
        link = db.save_short_url(key, target_url, criteria)

    return redirect('/link/'+link.key)

@app.route('/<regex("[a-zA-Z0-9]{6}"):key>/')
def redirect_to_target(key):
    link = db.query_target(key, request.user_agent.platform)
    if link == None:
        return render_template('404.html')
    else:
        db.save_click(link.id, request.referrer)
        return redirect(link.target_url)

@app.route('/links')
def links():
    links = db.all_links()
    return render_template('links.html', links=links, base_url=base_url)

@app.route('/link/<regex("[a-zA-Z0-9]{6}"):key>/')
def show_link(key):
    short_url = base_url + key
    results   = db.get_links_with_clicks(key)

    if len(results) == 0:
        return render_template('404.html')
    else:
        return render_template(
                  'link.html', results=results, short_url=short_url
               )
