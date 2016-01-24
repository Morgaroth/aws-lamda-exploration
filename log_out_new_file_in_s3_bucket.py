import urllib
import boto3

print('Loading function %s...' % __name__)
s3 = boto3.client('s3')


def lambda_handler(event, context):
    # Get the object from the event and show some its informations
    # get bucket name
    bucket = event['Records'][0]['s3']['bucket']['name']
    # get file name
    file_name = urllib.unquote_plus(event['Records'][0]['s3']['object']['key']).decode('utf8')
    # check content type
    response = s3.get_object(Bucket=bucket, Key=file_name)
    content_type = response['ContentType']
    print "Watching bucket %s: new file %s has content type %s." % (bucket, file_name, content_type)
    # return important values from function for future use
    return bucket, file_name, content_type
