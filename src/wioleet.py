import logging
import time
import click
import click_config

from .wio_config import config
from .functions import wioLeet
from flask import Flask


# init flask
app = Flask(__name__)

# set log level
logging.basicConfig(level=logging.DEBUG)

# set schedule
timer = float(config.app.schedule)
logging.info("Setting daemon schedule to {} seconds".format(timer))

# init class


@click.group()
@click_config.wrap(module=config)
def cli():
    pass


@cli.command()
def serve():
    logging.info("Starting app server...")
    app.run(host='0.0.0.0', port=8080)


@cli.command()
@app.route('/log')
def writeSensorData():
    w = wioLeet()
    w.log_data()


@cli.command()
@click.pass_context
def daemon(ctx):

    starttime=time.time()

    while True:
        logging.debug("starting log_data...")
        ctx.forward(writeSensorData)

        logging.debug("sleeping..")
        time.sleep(timer - ((time.time() - starttime) % timer))