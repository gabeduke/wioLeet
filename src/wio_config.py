import os

class config(object):
    class user(object):
        token = os.getenv('USER_TOKEN')
        base_url = os.getenv('BASE_URL', 'https://us.wio.seeed.io/')

    class node(object):
        sensor =  os.getenv('NODE_SENSOR', 'analog')
        token =  os.getenv('NODE_TOKEN')