import boto3
from botocore.exceptions import ClientError

from have_i_not_been_owned.common.config import s3


def get_s3_resource():
    return boto3.resource(
        's3',
        **s3['resource_credentials']
    )


# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-example-creating-buckets.html#create-an-amazon-s3-bucket
def create_bucket(resource=None):
    if resource is None:
        resource = get_s3_resource()

    client = resource.meta.client

    # Create bucket
    try:
        client.create_bucket(Bucket=s3['bucket']['bucket_name'])
        return True
    except ClientError:
        return False


# See https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-presigned-urls.html
def create_presigned_url(object_name, expiration=3600, s3_resource=None, bucket_name=None) -> str:

    if bucket_name is None:
        bucket_name = s3['bucket']['bucket_name']

    if s3_resource is None:
        s3_resource = get_s3_resource()

    s3_client = s3_resource.meta.client

    response = s3_client.generate_presigned_url(
        ClientMethod='get_object',
        Params={'Bucket': bucket_name, 'Key': object_name},
        ExpiresIn=expiration
    )

    return response


def create_presigned_post(object_name, expiration=3600, s3_resource=None, bucket_name=None) -> dict:

    if bucket_name is None:
        bucket_name = s3['bucket']['bucket_name']

    if s3_resource is None:
        s3_resource = get_s3_resource()

    # Generate a presigned URL for the S3 object
    s3_client = s3_resource.meta.client

    response = s3_client.generate_presigned_post(
        bucket_name,
        object_name,
        ExpiresIn=expiration
    )

    # The response contains the presigned URL
    return response
