from flask import Blueprint

from www.util import render_with_header

blueprint = Blueprint('standalone', __name__, template_folder='templates')

@blueprint.route('/')
def index():
    return render_with_header('index.html',
        server_detail = {
            'creative': {
                'address': 'c.nerd.nu',
                'tagline': 'flying enabled, infinite blocks',
                'links': [
                    ('live map', 'http://nerd.nu/maps/creative/live')]},
            'pve': {
                'address': 'p.nerd.nu',
                'tagline': 'survival mode, pvp disabled',
                'links': [
                    ('live map', 'http://nerd.nu/maps/pve/live')
                ]},
            'survival': {
                'address': 's.nerd.nu',
                'tagline': 'survival mode, pvp enabled',
                'links': []
            }
        }
    )

@blueprint.route('/appeal')
def appeal():
    return None #TODO

@blueprint.route('/staff')
def staff():
    return None #TODO