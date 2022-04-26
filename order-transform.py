import pandas as pd
from record_run import records_per_run
import datetime
import json
import random 
import os
import awswrangler as wr

#Next add bucket path for s3_upload

def s3_file_name(key):
    #file_name = key.replace('.','/').split('.')[-2]
    file_name = key.split('.')[0]
    return file_name

def clean_data(data):
    order_df = pd.json_normalize(data)
    columns = ['itemid', 'orderid', 'orderunits', 'ordertime', 'zipcode', 'city', 'state']
    order_df.columns = columns
    order_df['ordertime'] = pd.to_datetime(order_df['ordertime'], unit="ms")
    order_df['hour'] = order_df['ordertime'].dt.hour
    order_df['date'] = order_df['ordertime'].dt.date
    data_length = len(order_df)
    order_df.drop('ordertime', axis=1, inplace=True)
    return data_length, order_df





def process_orders(event, context):
    bucket = event['detail']['bucket']['name']
    key = event['detail']['object']['key']
    s3_buc = "s3://" + bucket + "/" + key
    # key = 'customer-orders+0+0000000000.json'
    file_name = s3_file_name(key)
    output_name = 'orders_' + str(random.randint(1111,9999)) + '.csv'
    data = [json.loads(line) for line in open(s3_buc, 'r')]
    data_length, order_df = clean_data(data)
    records_per_run(file_name=file_name, data_length=data_length, output_name=output_name)
    output_path = 's3://confluent-customer-orders/landing/' + output_name + '.csv'
    # order_df.to_csv(output_path, index=False)
    wr.s3.to_csv(df=order_df, path=output_path)
    print("Done")

process_orders(None, None)