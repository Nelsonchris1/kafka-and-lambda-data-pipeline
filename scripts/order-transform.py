import pandas as pd
from record_run import records_per_run
import datetime
import json
import random 
import os
import awswrangler as wr
import boto3

#Next add bucket path for s3_upload

def s3_file_name(key):
    # Exract file name from bucket key
 
    file_name = key.replace('.','/').split('.')[-2]
    return file_name

def clean_data(data):
    """
    Normalize table and extract datetime features,
    drop unneccesary column and fix column names
    """

    order_df = pd.json_normalize(data)
    columns = ['itemid', 'orderid', 'orderunits', 
                'ordertime', 'zipcode', 'city', 'state']
    order_df.columns = columns
    order_df['ordertime'] = pd.to_datetime(order_df['ordertime'], unit="ms")
    order_df['hour'] = order_df['ordertime'].dt.hour
    order_df['date'] = order_df['ordertime'].dt.date
    data_length = len(order_df)
    order_df.drop('ordertime', axis=1, inplace=True)
    return data_length, order_df





def process_orders(event, context):
    #Extract bucket name and key from payload

    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    s3_buc = "s3://" + bucket + "/" + key  
    
    # Call filenamefunction to extract file name  
    filename = s3_file_name(key)
    outputname = 'orders_' + str(random.randint(1111,9999)) + '.csv'

    #Extract the json datausing json loads
    s3_client = boto3.client('s3')
    result = s3_client.get_object(Bucket=bucket, Key=key)
    data = [json.loads(line) for line in result['Body'].read().splitlines()]

    #Call clean data function to extract data lenght and 
    data_length, order_df = clean_data(data)

    #Log record runs
    records_per_run(file_name=filename,
                    data_length=data_length, 
                    output_name=outputname)

    # Save cleaned csv data
    output_path = 's3://confluent-customer-orders/landing/' + outputname + '.csv'
    wr.s3.to_csv(order_df, output_path)
    print("Done")
