import json
import os

mongo = {
    'url': os.getenv('HINBO_DB_URL', 'mongodb://localhost/hinbo')
}

cos = {
    'resource_credentials': {
        'endpoint_url': os.getenv('HINBO_S3_ENDPOINT_URL', 'http://localhost:9000'),
        'aws_access_key_id': os.getenv('HINBO_S3_ACCESS_KEY_ID', 'ACCESS'),
        'aws_secret_access_key': os.getenv('HINBO_S3_SECRET_ACCESS_KEY', 'SuperS3cret'),
    },
    'bucket': {
        'bucket_name': os.getenv('HINBO_S3_BUCKET', 'hinbo'),
    },
    'data_breach_uploads': {
        'key_prefix': 'data_breach_uploads',
        'expiration_days': 30,
    },
}

amqp = {
    "url": os.getenv('HINBO_BROKER_URL', 'amqp://localhost:5672')
}

redis = {
    "url": os.getenv('HINBO_RESULT_BACKEND', 'redis://localhost:6379/0')
}


def _read_config():
    config_file_location = os.getenv('HINBO_CONFIG_FILE', 'config.json')

    with open(config_file_location, 'r') as config_file_reader:
        config = json.load(config_file_reader)

    mongo.update(config['mongo'])
    cos.update(config['cos'])
    amqp.update(config['amqp'])
    redis.update(config['redis'])


_read_config()
