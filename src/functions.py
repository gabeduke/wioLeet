import logging
import requests
import datetime
import json
import click_config

from .wio_config import config
from .sensors import sensors
from influxdb import InfluxDBClient


# set log level
logging.basicConfig(level=logging.DEBUG)


class wioLeet:

    def __init__(self):
        # init db connector
        host = config.app.db_host
        port = config.app.db_port
        dbname = config.app.db_name

        self.db = InfluxDBClient(host, port, database=dbname)


    def query_db(self):
        result = self.db.query('select * from soil1;')
        return result


    def log_data(self):
        logging.info("Getting sensor data...")
        d = self.get_data(
            config.node.sensor,
            config.node.param,
            )

        json_body = [
            {
                "measurement": config.node.param,
                "time": str(datetime.datetime.now()),
                "tags": {
                    "fleet": "sensors",
                    "sensor": config.app.sensor_tag,
                },
                "fields": {
                    "Int_value": d,
                }
            }
        ]

        logging.debug("Write points: {}".format(json_body))
        self.db.write_points(json_body)
        return d


    def get_data(self, sensor, param):

        sensor_map = sensors.get(sensor)
        params_map = sensors.get(sensor).get('params')
        logging.debug("Sensor map: {}".format(sensor_map))
        logging.debug("Parameter map: {}".format(params_map))

        url =  "{0}v1/node".format(config.app.base_url)
        url += "/{0}/{1}".format(sensor_map.get('name'), param)
        logging.debug("URL: {}".format(url))

        payload = {
            "access_token": config.node.token
        }

        req = requests.get(url, params=payload)
        logging.debug("Request: {}".format(req))

        resp_dict = json.loads(req.content.decode('utf-8'))
        logging.debug("Response: {}".format(resp_dict))

        sensor_data = resp_dict[params_map.get(param)]
        logging.info("Sensor value: {}".format(sensor_data))

        return sensor_data