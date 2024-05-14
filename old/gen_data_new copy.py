import argparse
import random
import string
from datetime import datetime, timedelta
import bisect
import os

use_case = None
base_dir = './data'


def create_directory(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)
        print(f"Directory '{directory}' created successfully.")
    else:
        print(f"Directory '{directory}' already exists.")
        
def save_logs(base_dir,filename, logs):
    create_directory(base_dir)
    filename = os.path.join(base_dir,filename)
    base_name, extension = os.path.splitext(filename)
    counter = 1
    new_filename = filename
    
    while os.path.exists(new_filename):
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    # Now, new_filename is a unique filename
    with open(new_filename, 'w') as f:
        # Write content to the new file if needed
        for log in logs:
            f.write(log[1])
    
    print(f"File '{new_filename}' created successfully.")


def generate_random_data_sources(num_data_sources):
    data_sources = []
    for _ in range(num_data_sources):
        source_name = "testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        data_sources.append(source_name)
    return data_sources

def generate_random_users(num_users):
    users = []
    for _ in range(num_users):
        source_name = "testuser_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10))
        users.append(source_name)
    return users


def user_inputs():
    # global use_case
    
    # generic inputs
    if use_case == 'use_case4':
        num_data_sources = 1
        num_users = 3
        anomalous_text = 1
        # num_users = int(input("Enter the number of users : "))
        # anomalous_text = "Enter number of anomalous users: "
    else:
        num_data_sources = int(input("Enter the number of data sources: "))
        anomalous_text = "Enter number of anomalous data sources: "

    # create_segment = input("Create log segments? (True/False): ").lower() == "true"
    
    # num_data_sources = 4
    create_segment = True
    
    
    
    # segment_config = {
    #     'start_date': input("Enter start date for the segment (YYYY-MM-DD HH:MM:SS): "),
    #     'end_date': input("Enter end date for the segment (YYYY-MM-DD HH:MM:SS): "),
    #     'record_rate_per_hr': int(input("Enter record rate per hour per 'normal' users: ")),
    #     'num_anomalous': int(input(anomalous_text)),
    #     'num_of_anomalies': int(input("Enter number of anomalies: ")),
    #     'anomaly_start_date': input("Enter start date for anomalies (YYYY-MM-DD HH:MM:SS): "),
    #     'anomaly_end_date': input("Enter end date for anomalies (YYYY-MM-DD HH:MM:SS): ")
    # } 
    
    segment_config = {
        'start_date': '2021-01-01',
        'end_date': '2021-01-03',
        'record_rate_per_hr': 1,
        'num_anomalous': 3,
        'num_of_anomalies': 4,
        'anomaly_start_date': '2021-01-02',
        'anomaly_end_date': '2021-01-02'
    }       
    
    if use_case == 'use_case4':
        # num_users = 7
        return num_data_sources, create_segment, segment_config, num_users
    
    return num_data_sources, create_segment, segment_config, 1
    
    

def validate_inputs(num_data_sources, create_segment, segment_config, num_users=None):
    if not create_segment:
        print("Segment creation is disabled. No logs will be generated.")
        return False
    
    if use_case == 'use_case4':
        if num_users < 1:
            print("Error: Number of users must be greater than 0")
            return False
        if segment_config['num_anomalous'] > num_users:
            print("Error: Number of anomalous users cannot exceed total number of users.")
            return False
        if segment_config['num_of_anomalies'] < segment_config['num_anomalous']:
            print("Error: Number of anomalies must be greater than or equal to the number of users.")
            return False
    
    if use_case == 'use_case3':
        if segment_config['num_anomalous'] > num_data_sources:
            print("Error: Number of anomalous data sources cannot exceed total data sources.")
            return False
        if segment_config['num_of_anomalies'] < segment_config['num_anomalous']:
            print("Error: Number of anomalies must be greater than or equal to the number of anomalous data sources.")
            return False
 
    return True
        

def extract_segment_config(segment_config):
    start_date = datetime.strptime(segment_config['start_date'], '%Y-%m-%d')
    end_date = datetime.strptime(segment_config['end_date'], '%Y-%m-%d')
    record_rate_per_hr = segment_config['record_rate_per_hr']
    num_anomalous = segment_config['num_anomalous']
    num_of_anomalies = segment_config['num_of_anomalies']
    anomaly_start_date = datetime.strptime(segment_config['anomaly_start_date'], '%Y-%m-%d')
    anomaly_end_date = datetime.strptime(segment_config['anomaly_end_date'], '%Y-%m-%d')
    
    return start_date, end_date, record_rate_per_hr, num_anomalous, num_of_anomalies, anomaly_start_date, anomaly_end_date


def generate_logs(*args):
    print(len(args))
    print()
    print(args)
    
    num_data_sources, start_date, end_date, record_rate_per_hr, num_anomalous, num_of_anomalies, anomaly_start_date, anomaly_end_date, num_users = args
    
    if num_data_sources and num_data_sources > 1:
        data_sources = generate_random_data_sources(num_data_sources)
    else:
        data_sources = ["fixed_datasource_value"]
    
    if num_users:
        users = generate_random_users(num_users)
    else:
        users = ['testSourceUser']
    
    
    #  Generate logs based on the segment configuration
    logs = []
    anomaly_count = 0
    current_date = start_date
    end_date = end_date + timedelta(days=1)

    # generate normal logs
    while current_date <= end_date:
        if current_date.hour > 5 and current_date.hour < 19:
            for src_user_name in users:
                source = random.choice(data_sources)
                log = (current_date, "<13>" + current_date.strftime("%b %d %H:%M:%S") + " " + source + " " + current_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: "+src_user_name +"\n")
                bisect.insort(logs, log)
        current_date += timedelta(hours=1/record_rate_per_hr)
    
    # generate anomalous logs
    current_date = anomaly_start_date
    # get random num_anomalous_data_sources data sources
    anomalous_list = random.sample(users, num_anomalous)
    anomalous_d_req =  False
    # generate num_of_anomalies for anomalous_data_sources on random dates between anomaly_start_date and anomaly_end_date and between 7pm and 5am
    while anomaly_count < num_of_anomalies:
       
        if anomalous_d_req:
            # get a random source from anomalous_data_sources
            # get a random date between anomaly_start_date and anomaly_end_date
            current_date = anomaly_start_date + timedelta(days=random.randint(0, (anomaly_end_date - anomaly_start_date).days))
            # get a random hour between 7pm and 5am
            current_date = current_date.replace(hour=random.randint(19, 23))
            source = random.choice(data_sources)
            src_user_name = random.choice(anomalous_list)
            log = (current_date, "<13>" + current_date.strftime("%b %d %H:%M:%S") + " " + source + " " + current_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: "+src_user_name +"\n")
            bisect.insort(logs, log)
            anomaly_count += 1
        else:
            for src_user_name in anomalous_list:
                 # get a random date between anomaly_start_date and anomaly_end_date
                current_date = anomaly_start_date + timedelta(days=random.randint(0, (anomaly_end_date - anomaly_start_date).days))
                # get a random hour between 7pm and 5am
                current_date = current_date.replace(hour=random.randint(19, 23))
                source = random.choice(data_sources)
                log = (current_date, "<13>" + current_date.strftime("%b %d %H:%M:%S") + " " + source + " " + current_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: "+src_user_name +"\n")
                bisect.insort(logs, log)
                anomaly_count += 1
                anomalous_d_req = True
    
    return logs
    

def use_case3(filename):
    num_data_sources, create_segment, segment_config, num_users = user_inputs()
    # print(num_data_sources, create_segment, segment_config)
    
    #validate inputs
    if not validate_inputs(num_data_sources, create_segment, segment_config):
        return
        
    logs = generate_logs(num_data_sources, *extract_segment_config(segment_config),num_users)    
    save_logs(base_dir=base_dir,filename=filename, logs=logs)
     
    
    
    
    

def use_case4(filename):
    num_data_sources, create_segment, segment_config, num_users = user_inputs()
    print(num_data_sources, create_segment, segment_config, num_users)
    
    #validate inputs
    if not validate_inputs(num_data_sources, create_segment, segment_config, num_users):
        return
    
    logs = generate_logs(num_data_sources, *extract_segment_config(segment_config), num_users)
    save_logs(base_dir=base_dir,filename=filename, logs=logs)
    


def main():
    parser = argparse.ArgumentParser(description='Your script description here.')

    # Add argument for specifying the use case
    parser.add_argument('use_case', choices=['use_case1', 'use_case2','use_case3','use_case4'], help='Specify the use case. Choose from: use_case1, use_case2.')

    # Add optional arguments if needed
     #parser.add_argument('--option', help='Description of the option.')

    # args = parser.parse_args()
    global use_case
    
    use_case = 'use_case4'
    filename = 'usecase4.syslog'
    use_case4(filename)

    # if args.use_case == 'use_case1':
    #     # Run code for use case 1
    #     pass
    
    # elif args.use_case == 'use_case2':
    #     # Run code for use case 2
    #     pass
    
    # elif args.use_case == 'use_case3':
    #     use_case = args.use_case
    #     filename = 'usecase3.syslog'
    #     use_case3(filename)
        
    # elif args.use_case == 'use_case4':
    #     use_case = args.use_case
    #     filename = 'usecase4.syslog'
    #     use_case4(filename)

if __name__ == "__main__":
    main()
