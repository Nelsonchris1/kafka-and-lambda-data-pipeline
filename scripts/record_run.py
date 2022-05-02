import datetime
import pandas as pd
import awswrangler as wr

def records_per_run(file_name, data_length, output_name):
    path = 's3://confluent-customer-orders/run_logs/record_run.csv'
    recrd_data = wr.s3.read_csv('s3://confluent-customer-orders/run_logs/record_run.csv')
    data_run = {'input_file_name': file_name,
                     'Data_length': data_length, 
                     'timestamp': datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y"),
                     'output_file_name': output_name}
    df = recrd_data.append(data_run, ignore_index=True)
    wr.s3.to_csv(df, 's3://confluent-customer-orders/run_logs/record_run.csv', index=False)
