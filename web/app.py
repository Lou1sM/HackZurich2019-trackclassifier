import json
import random

from flask import Flask, jsonify, render_template

LINE_DATA = 'data/line.json'
ELEMENTS_DATA = 'data/elements_03.json'

app = Flask(__name__)


@app.route('/api/track')
def get_track():
    with open(ELEMENTS_DATA) as f:
        elements = json.load(f)

    # normalize element types
    TYPE_DICT = {
        'balise': 'balise',
        'main signal': 'main_signal',
        'distant signal': 'distant_signal',
    }
    for e in elements:
        e['type'] = TYPE_DICT[e['type']]
        e['coords'] = [e['longitude'], e['latitude']]
    elements = elements[:40]

    with open(LINE_DATA) as f:
        points = json.load(f)
        # points = points[:len(points) // 2 - 90]
        points = points[:1000]

    # elements = elements[:200]
    return jsonify({
        'line': {
            'coords': [[p['coordinates'][1], p['coordinates'][0]] for p in points],
        },
        'elements': elements,
    })


@app.route('/')
def get_index():
    return render_template('index.html')
