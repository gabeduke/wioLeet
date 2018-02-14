import os

class config(object):
    class user(object):
        token = os.getenv('USER_TOKEN')
        base_url = os.getenv('BASE_URL', 'https://us.wio.seeed.io/')
        db_name = os.getenv('DB_NAME', 'leetbase')
        db_host = os.getenv('DB_HOST', 'influxdb-influxdb')
        db_port = os.getenv('DB_PORT', 8086)

    class node(object):
        sensor =  os.getenv('NODE_SENSOR', 'analog')
        param = os.getenv('NODE_PARAM')
        token =  os.getenv('NODE_TOKEN')
        schedule = os.getenv('NODE_SCHEDULE')