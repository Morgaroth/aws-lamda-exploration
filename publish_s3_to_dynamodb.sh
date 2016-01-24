#!/bin/bash

source venv/bin/activate

FILE=publish_s3_to_dynamodb
ROLE_ARN=arn:aws:iam::799951086751:role/lambda-adm

mkdir -p ./zips
zip zips/${FILE}.zip ${FILE}.py

aws lambda get-function \
    --region eu-west-1 \
    --function-name ${FILE}

GET_RES=`echo $?`
echo "Get returned code $GET_RES"

if [ "255" == "$GET_RES" ]; then
    aws lambda create-function \
        --region eu-west-1 \
        --function-name ${FILE} \
        --role ${ROLE_ARN} \
        --zip-file fileb://zips/${FILE}.zip \
        --handler ${FILE}.lambda_handler \
        --runtime python2.7

    CREATE_RES=`echo $?`
    echo "Function was CREATED!"
    echo "Create returned code $CREATE_RES"
else
    aws lambda update-function-code \
        --region eu-west-1 \
        --function-name ${FILE} \
        --zip-file fileb://zips/${FILE}.zip

    RES=`echo $?`
    echo "Function was UPDATED!"
    echo "result code $RES"
fi

#--profile adminuser