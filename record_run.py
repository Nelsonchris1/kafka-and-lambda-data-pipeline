import datetime
import pandas as pd

def records_per_run(file_name, data_length, output_name):
    record_run = pd.read_csv('record_run.csv')
    data_run = {'input_file_name': file_name,
                 'Data_length': data_length, 
                 'timestamp': datetime.datetime.utcnow().strftime("%a %b %d %H:%M:%S UTC %Y"),
                 'output_file_name': output_name}
    new_record = record_run.append(data_run, ignore_index=True)
    new_record.to_csv('record_run.csv', index=False)