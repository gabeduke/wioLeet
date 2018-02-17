import os

class config(object):
    class user(object):
        token = os.getenv('USER_TOKEN')

    class node(object):
        sensor =  os.getenv('NODE_SENSOR', 'analog')
        param = os.getenv('NODE_PARAM')
        token =  os.getenv('NODE_TOKEN')

    class app(object):
        base_url = os.getenv('BASE_URL', 'https://us.wio.seeed.io/')
        schedule = os.getenv('NODE_SCHEDULE', 30)
        db_name = os.getenv('DB_NAME', 'leetbase')
        db_host = os.getenv('DB_HOST', 'influxdb-influxdb')
        db_port = os.getenv('DB_PORT', 8086)
        sensor_tag = os.getenv('SENSOR_TAG', 'default')
