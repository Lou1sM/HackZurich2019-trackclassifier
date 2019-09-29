import json
import random

from flask import Flask, jsonify, render_template

DATA_FILENAME = 'data/elements.json'

app = Flask(__name__)


@app.route('/api/track')
def get_track():
    lat, lng = 46.98026536027778, 9.641403229722222
    with open('data/elements.json') as f:
        elements = json.load(f)
    TYPE_DICT = {
        'balise': 'balise',
        'main signal': 'main_signal',
        'distant signal': 'distant_signal',
    }
    elements = [e for e in elements if e['type'] in TYPE_DICT]
    for e in elements:
        # normalize element types
        e['type'] = TYPE_DICT[e['type']]

        # add some lat & long
        e['latitude'], e['longitude'] = lat, lng
        lat += random.uniform(0.001, 0.01)
        lng += random.uniform(0.001, 0.01)

    elements = elements[:50]
    # below this point assume keys id, latitude, longitude, relative

    return jsonify({
        'line': {
            'coords': [(e['longitude'], e['latitude']) for e in elements],
        },
        'elements': [{
            'type': e['type'],
            'id': e['id'],
            'coords': [e['longitude'], e['latitude']],
        } for e in elements],
    })

    # track_coords = [(e['longitude'], e['latitude']) for e in elements]
    # balise_coords = [(e['longitude'], e['latitude']) for e in elements if e['type'] == 'balise']
    # main_signal_coords = [(e['longitude'], e['latitude']) for e in elements if e['type'] == 'main signal']
    # distant_signal_coords = [(e['longitude'], e['latitude']) for e in elements if e['type'] == 'distant signal']
    #
    # track = geojson.FeatureCollection([
    #     geojson.Feature(
    #         id='track',
    #         geometry=geojson.LineString(track_coords),
    #     ),
    #     geojson.Feature(
    #         id='balises',
    #         geometry=geojson.MultiPoint(balise_coords),
    #     ),
    #     geojson.Feature(
    #         id='main_signals',
    #         geometry=geojson.MultiPoint(main_signal_coords),
    #     ),
    #     geojson.Feature(
    #         id='distant_signals',
    #         geometry=geojson.MultiPoint(distant_signal_coords),
    #     ),
    # ])
    # return geojson.dumps(track)


@app.route('/')
def get_index():
    return render_template('index.html')
