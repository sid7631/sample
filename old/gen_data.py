import random
import string
from datetime import datetime, timedelta
import bisect

def generate_random_data_sources(num_data_sources):
    data_sources = []
    for _ in range(num_data_sources):
        source_name = "testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data_sources.append(source_name)
    return data_sources

def generate_logs(num_data_sources, create_segment, segment_config):
    if not create_segment:
        print("Segment creation is disabled. No logs will be generated.")
        return
    
    # Extract segment configuration parameters
    start_date = datetime.strptime(segment_config['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(segment_config['end_date'], '%Y-%m-%d')
    record_rate_per_hr = segment_config['record_rate_per_hr']
    num_anomalous_data_sources = segment_config['num_anomalous_data_sources']
    num_of_anomalies = segment_config['num_of_anomalies']
    anomaly_start_date = datetime.strptime(segment_config['anomaly_start_date'], '%Y-%m-%d')
    anomaly_end_date = datetime.strptime(segment_config['anomaly_end_date'], '%Y-%m-%d')

    # Validate parameters
    if num_anomalous_data_sources > num_data_sources:
        print("Error: Number of anomalous data sources cannot exceed total data sources.")
        return
    
    if num_of_anomalies < num_anomalous_data_sources:
        print("Error: Number of anomalies must be greater than or equal to the number of anomalous data sources.")
        return

    # Generate random data source names
    data_sources = generate_random_data_sources(num_data_sources)

    # Generate logs based on the segment configuration
    logs = []
    anomaly_count = 0
    current_date = start_date
    end_date = end_date + timedelta(days=1)

    # generate normal logs
    while current_date <= end_date:
        if current_date.hour > 5 and current_date.hour < 19:
            for source in data_sources:
                log = {
                    'source': source,
                    'timestamp': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'message': "Normal log message"
                }
                log = (current_date, f"{source} Normal log message")
                bisect.insort(logs, log)
        current_date += timedelta(hours=1/record_rate_per_hr)
    
    # generate anomalous logs
    current_date = anomaly_start_date
    # get random num_anomalous_data_sources data sources
    anomalous_data_sources = random.sample(data_sources, num_anomalous_data_sources)
    anomalous_data_sources_req =  False
    # generate num_of_anomalies for anomalous_data_sources on random dates between anomaly_start_date and anomaly_end_date and between 7pm and 5am
    while anomaly_count < num_of_anomalies:
       
        
        if anomalous_data_sources_req:
             # get a random source from anomalous_data_sources
            # get a random date between anomaly_start_date and anomaly_end_date
            current_date = datetime.strptime(segment_config['anomaly_start_date'], '%Y-%m-%d') + timedelta(days=random.randint(0, (anomaly_end_date - anomaly_start_date).days))
            # get a random hour between 7pm and 5am
            current_date = current_date.replace(hour=random.randint(19, 23))
            source = random.choice(anomalous_data_sources)
            log = (current_date, f"{source} Anomalous log message")
            bisect.insort(logs, log)
            anomaly_count += 1
        else:
            for source in anomalous_data_sources:
                 # get a random date between anomaly_start_date and anomaly_end_date
                current_date = datetime.strptime(segment_config['anomaly_start_date'], '%Y-%m-%d') + timedelta(days=random.randint(0, (anomaly_end_date - anomaly_start_date).days))
                # get a random hour between 7pm and 5am
                current_date = current_date.replace(hour=random.randint(19, 23))
                log = {
                    'source': source,
                    'timestamp': current_date.strftime('%Y-%m-%d %H:%M:%S'),
                    'message': "Anomalous log message"
                }
                log = (current_date, f"{source} Anomalous log message")
                bisect.insort(logs, log)
                anomaly_count += 1
                anomalous_data_sources_req = True
    return logs

if __name__ == "__main__":
    # num_data_sources = int(input("Enter the number of data sources: "))
    # create_segment = input("Create log segments? (True/False): ").lower() == "true"
    num_data_sources = 4
    create_segment = True
    
    # segment_config = {
    #     'start_date': input("Enter start date for the segment (YYYY-MM-DD HH:MM:SS): "),
    #     'end_date': input("Enter end date for the segment (YYYY-MM-DD HH:MM:SS): "),
    #     'record_rate_per_hr': int(input("Enter record rate per hour per 'normal' data source: ")),
    #     'num_anomalous_data_sources': int(input("Enter number of anomalous data sources: ")),
    #     'num_of_anomalies': int(input("Enter number of anomalies: ")),
    #     'anomaly_start_date': input("Enter start date for anomalies (YYYY-MM-DD HH:MM:SS): "),
    #     'anomaly_end_date': input("Enter end date for anomalies (YYYY-MM-DD HH:MM:SS): ")
    # }

    segment_config = {
        'start_date': '2021-01-01',
        'end_date': '2021-01-03',
        'record_rate_per_hr': 1,
        'num_anomalous_data_sources': 3,
        'num_of_anomalies': 4,
        'anomaly_start_date': '2021-01-01',
        'anomaly_end_date': '2021-01-02'
    }

    logs = generate_logs(num_data_sources, create_segment, segment_config)
    print('logs:', len(logs))
    # for log in logs:
    #     print('i')
    #     # print(log)
