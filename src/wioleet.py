import requests
import json
import click
import click_config
import datetime
import schedule
import time

from influxdb import InfluxDBClient
from .sensors import sensors
from .wio_config import config
from flask import Flask

# init flask
app = Flask(__name__)

# init db connector
host = config.user.db_host
port = config.user.db_port
dbname = config.user.db_name

db = InfluxDBClient(host, port, database=dbname)

@click.group()
@click_config.wrap(module=config)
def cli():
    pass


@cli.command()
def wioLeet(name):
    print(name)


@cli.command()
def daemon():
    s = config.node.schedule
    schedule.every(int(s)).minutes.do(log)

    while True:
        schedule.run_pending()
        time.sleep(1)


@cli.command()
def serve():
    app.run(host='0.0.0.0', port=8080)


def mean(numbers):
    return float(sum(numbers)) / max(len(numbers), 1)


@cli.command()
@app.route('/log')
def log():
    d = get_data(
        config.node.sensor,
        config.node.param,
        )

    json_body = [
        {
            "measurement": "soil1",
            "time": str(datetime.datetime.now()),
            "fields": {
                "Int_value": d,
            }
        }
    ]

    print("write points: {0}".format(json_body))
    db.write_points(json_body)


def get_data(sensor, param):

    sensor_map = sensors.get(sensor)
    params_map = sensors.get(sensor).get('params')

    url =  "{0}v1/node".format(config.user.base_url)
    url += "/{0}/{1}".format(sensor_map.get('name'), params_map.get(param))

    payload = {
        "access_token": config.node.token
    }

    req = requests.get(url, params=payload)
    resp_dict = json.loads(req.content.decode('utf-8'))
    sensor_data = resp_dict['analog']

    return sensor_data
