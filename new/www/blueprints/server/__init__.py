from flask import Blueprint, render_template, request, current_app
from www.models.cache import Cache

import json

def load_json(filename):
    with current_app.open_resource('scraped/'+filename) as json_data:
        d = json.load(json_data)
        json_data.close()
        return d

def load_html(filename):
    with current_app.open_resource('scraped/'+filename) as html_data:
        d = html_data.read()
        html_data.close()
        return d

blueprint = Blueprint('server', __name__, template_folder='templates')

def _index(server):
    server = server.lower()
    if server not in ['creative', 'survival', 'pve']:
        abort(404)
    addr = {'creative': 'c.nerd.nu', 'survival': 's.nerd.nu', 'pve': 'p.nerd.nu'}
    current_rev = int(Cache.query.filter_by(key='CURRENT_REVISION_'+server.upper()).first().value)

    options = {
        'title': server,
        'addr': addr,
        'subreddit': json.loads(Cache.query.filter_by(key='REDDIT_POSTS').first().value),
        #'github': json.loads(Cache.query.filter_by(key='GITHUB_'+server.upper()+'_ISSUES').first().value),
        'current_rev': current_rev,
        'top_players': json.loads(Cache.query.filter_by(key='MC_'+server.upper()+'_TOP_PLAYERS').first().value)
    }

    return render_template('server.html', **options)


@blueprint.route('/creative')
def creative_index():
    return _index('creative')

@blueprint.route('/survival')
def survival_index():
    return _index('survival')

@blueprint.route('/pve')
def pve_index():
    return _index('pve')
