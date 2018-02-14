sensors = {
    'analog': {
        'name': 'GenericAInA0',
        'params': {
            'analog': 'analog',
            'voltage': 'volt',
        }
    },
    'tempHumd': {
        'name': 'GroveTempHumD1',
        'params': {
            'humidity': 'humidity',
            'temperature': [
                'celsius_degree',
                'fahrenheit_degree',
                ]
        }
    }
}