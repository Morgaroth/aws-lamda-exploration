#!/usr/bin/env bash

FILE=log_out_new_file_in_s3_bucket

mkdir -p ./zips
zip zips/${FILE}.zip ${FILE}.py

aws lambda create-function \
--region eu-west-1 \
--function-name ${FILE} \
--zip-file fileb://zips/${FILE}.zip \
--handler ${FILE}.lambda_handler \
--runtime python3.5 ;

#--role role-arn \
#--profile adminuser