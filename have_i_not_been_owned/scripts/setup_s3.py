import logging

from botocore.exceptions import ClientError

from have_i_not_been_owned.common.config import cos
from have_i_not_been_owned.common.s3 import get_s3_resource

logger = logging.getLogger(__name__)


def main():
    logger.info("Setting up S3")

    resource = get_s3_resource()

    _create_bucket(resource)
    _setup_lifecycle(resource)


# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html#create-an-amazon-s3-bucket
def _create_bucket(resource):
    client = resource.meta.client
    bucket_name = cos['bucket']['bucket_name']

    try:
        client.create_bucket(Bucket=bucket_name)
        logger.info("Bucket %r created successfully.", bucket_name)
        return True
    except ClientError:
        logger.info("Bucket %r already exists", bucket_name)
        return False


# See https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#bucketlifecycle
def _setup_lifecycle(resource):
    """
    Create a lifecycle policy on the uploaded data breach files so that they expire and get deleted automatically
    :param resource:
    :return:
    """
    bucket_name = cos['bucket']['bucket_name']
    data_breach_uploads = cos['data_breach_uploads']

    logger.info(
        "Setting up an expiration lifecycle policy on the data uploads for %r days on bucket %r",
        data_breach_uploads['expiration_days'],
        bucket_name,
    )

    resource.meta.client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            'Rules': [
                {
                    'Expiration': {
                        'Days': data_breach_uploads['expiration_days']
                    },
                    'ID': 'data-breach-uploads-expiration',
                    'Prefix': f"{data_breach_uploads['key_prefix']}/",
                    'Status': 'Enabled'
                }
            ]
        }
    )


if __name__ == '__main__':
    logging.basicConfig(level=logging.WARNING)
    logger.setLevel(logging.INFO)
    main()
