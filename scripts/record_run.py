import datetime
import pandas as pd

def records_per_run(file_name, data_length, output_name):
    path = 's3://confluent-customer-orders/run_logs/record_run.csv'
    record_run = pd.read_csv(path)
    data_run = {'input_file_name': file_name,
                 'Data_length': data_length, 
                 'timestamp': datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y"),
                 'output_file_name': output_name}
    new_record = record_run.append(data_run, ignore_index=True)
    new_record.to_csv(path, index=False)