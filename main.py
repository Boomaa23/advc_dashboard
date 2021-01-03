import flask
import json
import os
import pandas
import matplotlib
import threading

http = flask.Flask(__name__, template_folder=os.path.abspath('.'))
stats = pandas.read_csv('stats.csv')


@http.route('/')
@http.route('/index.html')
def index():
    if os.stat('data.json').st_size < 400:
        create_data_json()
    data = json.load(open('data.json', 'r'))
    return flask.render_template('index.html', data=data, stats=stats)


def create_data_json():
    name_list = pandas.Series.to_list(stats.iloc[:, 0])
    out_dict = {}
    for name in name_list:
        out_dict[name] = 0

    with open('data.json', 'w') as file:
        json.dump(out_dict, file, indent=2)


def periodic_update():
    pass


update_thread = threading.Thread(target=periodic_update)
update_thread.start()
