import random
import time
import configparser
import string
from datetime import datetime, timedelta
import bisect
import os



def create_directory(directory):
    os.makedirs(directory, exist_ok=True)
    print(f"Directory '{directory}' created successfully.")

def save_logs(base_dir, filename, logs):
    create_directory(base_dir)
    filename = os.path.join(base_dir, filename)
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
        

# Function to read config file
def read_config():
    config = configparser.ConfigParser()
    config.read("config.ini")
    return config

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

# Function to generate syslog-like data
def generate_syslog_data(current_date, source, src_user_name):
    return (current_date, "<13>" + current_date.strftime("%b %d %H:%M:%S") + " " + source + " " + current_date.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: "+src_user_name +"\n")

def generate_logs3():
    pass

def generate_logs4(user_inputs):

    #format the user inputs, convert date strings to datetime objects, int strings to integers, etc.
    user_inputs["num_users"] = int(user_inputs["num_users"])
    user_inputs["num_data_sources"] = int(user_inputs["num_data_sources"])
    user_inputs["num_anomalous_users"] = int(user_inputs["num_anomalous_users"])
    user_inputs["start_date"] = datetime.strptime(user_inputs["start_date"].replace(':', ' ', 1), "%Y-%m-%d %H:%M:%S")
    user_inputs["end_date"] = datetime.strptime(user_inputs["end_date"].replace(':', ' ', 1), "%Y-%m-%d %H:%M:%S")
    user_inputs["anomaly_start_date"] = datetime.strptime(user_inputs["anomaly_start_date"].replace(':', ' ', 1), "%Y-%m-%d %H:%M:%S")
    user_inputs["anomaly_end_date"] = datetime.strptime(user_inputs["anomaly_end_date"].replace(':', ' ', 1), "%Y-%m-%d %H:%M:%S")
    user_inputs["normal_frequency"] = int(user_inputs["normal_frequency"])
    user_inputs["anomaly_frequency"] = int(user_inputs["anomaly_frequency"])


    logs = []

    users = generate_random_users(user_inputs["num_users"])
    sources = generate_random_data_sources(user_inputs["num_data_sources"])
    anomalous_uers = random.sample(users, user_inputs["num_anomalous_users"])

    start_timestamp =user_inputs["start_date"]
    end_timestamp = user_inputs["end_date"]

    anomaly_start_timestamp = user_inputs["anomaly_start_date"]
    anomaly_end_timestamp = user_inputs["anomaly_end_date"]


    for user in users:
        current_timestamp = start_timestamp
        #generate normal data
        while current_timestamp < end_timestamp:
            if current_timestamp > anomaly_start_timestamp and current_timestamp < anomaly_end_timestamp and user in anomalous_uers:
                source = random.choice(sources)
                log = (current_timestamp, generate_syslog_data(current_timestamp, source, user))
                bisect.insort(logs, log)
                current_timestamp += timedelta(hours=1/user_inputs["anomaly_frequency"])
            else:
                source = random.choice(sources)
                log = (current_timestamp, generate_syslog_data(current_timestamp, source, user))
                bisect.insort(logs, log)
                current_timestamp += timedelta(hours=1/user_inputs["normal_frequency"])
    
    return logs



# Main function to generate data for different use cases
def main():
    config = read_config()

    use_case = input("Enter use case (usecase1/usecase2/usecase3/usecase4): ")
    if use_case not in config.sections():
        print("Invalid use case.")
        return
    
    user_inputs = dict(config[use_case])

    # messages = config[use_case]["messages"].split(',')

    logs = []
    
    if use_case == "usecase1":
        pass
    elif use_case == "usecase2":
        pass
    elif use_case == "usecase3":
        logs = generate_logs3()
    elif use_case == "usecase4":
        logs = generate_logs4(user_inputs)

    if logs:
        save_logs(config["DEFAULT"]["base_dir"], config[use_case]["filename"], logs)

if __name__ == "__main__":
    main()