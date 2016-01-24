#!/usr/bin/env bash

source venv/bin/activate

FILE=microservice
ROLE_ARN=arn:aws:iam::799951086751:role/lambda-adm

mkdir -p ./zips
zip zips/${FILE}.zip ${FILE}.py

aws lambda get-function \
    --region eu-west-1 \
    --function-name ${FILE}

GET_RES=`echo $?`
echo "Get function $FILE returned code $GET_RES"

if [ "255" == "$GET_RES" ]; then
    aws lambda create-function \
        --region eu-west-1 \
        --function-name ${FILE} \
        --role ${ROLE_ARN} \
        --zip-file fileb://zips/${FILE}.zip \
        --handler ${FILE}.lambda_handler \
        --runtime python2.7

    CREATE_RES=`echo $?`
    echo "Function $FILE was CREATED with code $CREATE_RES!"
else
    aws lambda update-function-code \
        --region eu-west-1 \
        --function-name ${FILE} \
        --zip-file fileb://zips/${FILE}.zip

    RES=`echo $?`
    echo "Function $FILE was UPDATED with code $RES"
fi