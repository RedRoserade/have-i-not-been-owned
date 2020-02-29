import os

db_url = os.getenv('HINBO_DB_URL', 'mongodb://localhost/hinbo')

s3 = {
    'resource_credentials': {
        'endpoint_url': os.getenv('HINBO_S3_ENDPOINT_URL', 'http://localhost:9000'),
        'aws_access_key_id': os.getenv('HINBO_S3_ACCESS_KEY_ID', 'ACCESS'),
        'aws_secret_access_key': os.getenv('HINBO_S3_SECRET_ACCESS_KEY', 'SuperS3cret'),
    },
    'bucket': {
        'bucket_name': os.getenv('HINBO_S3_BUCKET', 'hinbo'),
    },
}
