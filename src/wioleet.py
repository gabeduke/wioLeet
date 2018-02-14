import requests
import json
import click
import click_config
import schedule
import time

from .wio_config import config
from flask import Flask


app = Flask(__name__)

analog = {
    'name': 'GenericAInA0',
    'params': {
        'analog': 'analog',
        'voltage': 'volt',
    }
}

@click.group()
@click_config.wrap(module=config)
def cli():
    pass


@cli.command()
def test():
    click.echo(config.user.token)
    click.echo(config.user.base_url)
    click.echo(config.node.sensor)
    click.echo(config.node.token)


@cli.command()
def wioLeet(name):
    print(name)


@cli.command()
def daemon():
    schedule.every(1).minutes.do(log)

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
    d = get_data()

    url = "http://influxdb-influxdb:8086/write?db=leetbase"
    payload = ("--data-binary 'soil1,wionode=wio1 value=%s'" % d)
    req = requests.post(url, data=payload)
    resp_dict = json.loads(req.content.decode('utf-8'))

    return str(resp_dict)


@app.route('/sensor')
def get_data():

    url = config.user.base_url + "v1/node"
    url += "/" + str(analog['name'])                # sensor name
    url += "/" + str(analog['params']['analog'])    # sensor param

    payload = {
        "access_token": config.node.token
    }

    req = requests.get(url, params=payload)
    resp_dict = json.loads(req.content.decode('utf-8'))
    sensor_data = resp_dict['analog']

    return str(sensor_data)
