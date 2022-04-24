import pandas as pd
from record_run import records_per_run
import datetime
import json
import random 
import os


def s3_file_name(key):
    file_name = key.replace('.','/').split('.')[-2]
    return file_name

def process_data(data):
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
    # bucket = event['detail']['bucket']['name']
    # key = event['detail']['object']['key']
    # s3_buc = "s3://" + bucket + "/" + key
    key = 'customer-orders+0+0000000000.json'
    file_name = s3_file_name(key)
    output_name = 'customer_file' + str(random.randint(1111,9999)) + '.csv'
    data = [json.loads(line) for line in open(key, 'r')]
    data_length, order_df = process_data(data)
    records_per_run(file_name=file_name, data_length=data_length, output_name=output_name)
    order_df.to_csv(output_name, index=False)
    print("Done")

process_orders(None, None)