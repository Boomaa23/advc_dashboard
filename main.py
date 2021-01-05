import flask
import json
import matplotlib.pyplot as plt
import os
import pandas
import threading
import time

http = flask.Flask(__name__)
stats = pandas.read_csv('stats.csv')


@http.route('/')
@http.route('/index.html')
def index():
    data = json.load(open('data.json', 'r'))
    # threading.Thread(target=generate_graphs, args=(data,)).start()
    generate_graphs(data)
    return flask.render_template('index.html', data=data)


@http.after_request
def force_no_cache(req):
    req.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    req.headers["Pragma"] = "no-cache"
    req.headers["Expires"] = "0"
    req.headers['Cache-Control'] = 'public, max-age=0'
    return req


def generate_graphs(data):
    base_filepath = 'static/img/'
    for planet, businesses in data.items():
        planet_path = base_filepath + planet
        if not os.path.isdir(planet_path):
            os.makedirs(planet_path, exist_ok=True)
        for bus_name, points in businesses.items():
            plt.plot(points)
            plt.savefig(planet_path + '/' + bus_name, bbox_inches='tight')
            plt.clf()


def update_data_json(data):
    # TODO update data in json
    pass


def create_data_json():
    name_list = pandas.Series.to_list(stats.iloc[:, 0])
    out_dict = {}
    planet = str()
    for i, name in enumerate(name_list):
        if i < 10:
            planet = 'Earth'
        elif i < 20:
            planet = 'Moon'
        elif i < 30:
            planet = 'Mars'
        if i % 10 == 0:
            out_dict[planet] = {}
        out_dict[planet][name] = [0]

    with open('data.json', 'w') as file:
        json.dump(out_dict, file, indent=2)


def init_update():
    try:
        if os.stat('data.json').st_size < 400:
            create_data_json()
    except FileNotFoundError:
        create_data_json()
    periodic_update()


def periodic_update():
    # TODO do update here
    time.sleep(1)
    periodic_update()


update_thread = threading.Thread(target=init_update)
update_thread.start()
