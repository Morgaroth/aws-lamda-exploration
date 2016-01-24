import json
import urllib
from uuid import uuid4

import boto3

print 'Loading function %s...' % __name__

s3 = boto3.client('s3')
dynamo = boto3.client('dynamodb')


def lambda_handler(event, context):
    # Get the object from the event and get some its informations
    print "Received event: " + json.dumps(event, indent=3)
    bucket = event['Records'][0]['s3']['bucket']['name']
    file_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    response = s3.get_object(Bucket=bucket, Key=file_name)
    content_type = response['ContentType']

    # create table UploadedFiles in dynamodb if not exists
    table_name = 'UploadedFiles'
    try:
        dynamo.describe_table(TableName=table_name)
    except Exception as e:
        dynamo.create_table(
                AttributeDefinitions=[{'AttributeName': 'UUID', 'AttributeType': 'S',}, ],
                TableName=table_name,
                KeySchema=[{'AttributeName': 'UUID', 'KeyType': 'HASH',}],
                ProvisionedThroughput={'ReadCapacityUnits': 123, 'WriteCapacityUnits': 123,},
        )

    # save data to dynamodb
    boto3.resource('dynamodb').Table(table_name).put_item(Item={
        'UUID': str(uuid4()),
        'bucket': bucket,
        'name': file_name,
        'content': content_type,
        'event': event,
        'context': str(context),
    })


