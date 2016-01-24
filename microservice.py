import json
from uuid import uuid4

import boto3
from botocore.exceptions import ClientError

print('Loading function %s...' % __name__)

dynamo = boto3.client('dynamodb')
table_name = 'MicroServiceDB'


def ensure_table_exists():
    try:
        dynamo.describe_table(TableName=table_name)
        return boto3.resource('dynamodb').Table(table_name)
    except ClientError as e:
        if e.message.startswith(
                'An error occurred (ResourceNotFoundException) when calling the DescribeTable operation: Requested resource not found: Table'):
            print "Creating table %s in DynamoDB" % table_name
            dynamo.create_table(
                    AttributeDefinitions=[{'AttributeName': 'id', 'AttributeType': 'S',}, ],
                    TableName=table_name,
                    KeySchema=[{'AttributeName': 'id', 'KeyType': 'HASH',}],
                    ProvisionedThroughput={'ReadCapacityUnits': 123, 'WriteCapacityUnits': 123,},
            )
            return boto3.resource('dynamodb').Table(table_name)
        else:
            raise


def insert_item(data):
    table = ensure_table_exists()
    table.put_item(Item={
        'id': str(uuid4()),
        'data': data
    })
    return 'OK'


def list_items(data):
    table = ensure_table_exists()
    result = table.scan()['Items']
    return result


def lambda_handler(event, context):
    print "Event: %s" % json.dumps(event)
    try:
        operation = globals()[event['method']]
        result = operation(event['params'])
        return {'jsonrpc': '2.0', 'result': result, 'id': event.get('id', '-1')}
    except KeyError:
        return {'jsonrpc': '2.0', 'error': 'method %s not found' % event['method'], 'id': event.get('id', '-1')}
