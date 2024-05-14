# Assisted by WCA for GP
# Latest GenAI contribution: granite-20B-code-instruct-v2 model
import random
import string
import os
from datetime import datetime, timedelta
import dateutil.parser


def gather_user_inputs_for_segment():
    config = {}

    # Set the start and end dates for the segment
    # TODO turn this into fine grained timestamps so you can have smaller anomalous periods
    start_date_str = str(input("What is the start date for the segment? "))
    config['start_date'] = dateutil.parser.parse(start_date_str, dayfirst=True)
    end_date_str = str(input("What is the end date for the segment? "))
    config['end_date'] = dateutil.parser.parse(end_date_str, dayfirst=True)

    config['record_rate_per_hr'] = int(input("Approximately how many records do you want per hour per 'normal' data source? "))

    #config.anomaly_mode = str(input("What anomaly mode? (e.g. 'count') ") or "count")
    # Modes: count
    #if anomaly_mode != "count":
    #    print(f'Count is currently the only mode supported')
    #    exit(0)

    config['num_anomalous_data_sources'] = int(input("How many data sources should misbehave in this segment? "))

    if config['num_anomalous_data_sources'] > 0:
        config['anomaly_change_ratio'] = float(input("What ratio should be applied to the rate for the anomalous data? "))
    
    return config

def validate_user_inputs(num_data_sources, config):
    if config['num_anomalous_data_sources'] > num_data_sources:
        print('Number of anomalous data sources (' + str(config['num_anomalous_data_sources']) + ') cannot exceed the number of data sources available (' + str(num_data_sources) + ')')
        exit(0)



def main():
    # Prompt the user for the number of different data source names they want
    num_data_sources = int(input("How many different data source names do you want? "))
    # Generate a list of random data source names
    data_source_names = ["testdatasource_" + "".join(random.choices(string.ascii_uppercase + string.digits, k=10)) for _ in range(num_data_sources)]

    create_segment = bool(input("Do you want to start creating log segments? (yes/no) ") == "yes")

    # Open a file for writing
    filename = "test_dataset.syslog"
    with open(filename, "w") as f:
        while create_segment:

            segment_config = gather_user_inputs_for_segment()
        
            validate_user_inputs(num_data_sources, segment_config)

            # Loop through each day in the specified date range
            current_date = segment_config['start_date']
            while current_date <= segment_config['end_date']:
                # Get the timestamp for the start of the day
                day_start = datetime(current_date.year, current_date.month, current_date.day)

                # Generate log lines for the current day
                for hour_of_day in range(0, 24):
                    # Do anomalous data sources first
                    for data_source_name in data_source_names[:segment_config['num_anomalous_data_sources']]:
                        for record_count in range(0,int(segment_config['record_rate_per_hr'] * segment_config['anomaly_change_ratio'])):
                            # Calculate a random timestamp within the current hour
                            seconds_so_far = hour_of_day * 60 * 60
                            delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far))
                            timestamp = day_start + delta

                            # Write the log line to the file
                            line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: testSourceUser\n"
                            f.write(line)

                    # Now the rest of the data sources
                    for data_source_name in data_source_names[segment_config['num_anomalous_data_sources']:]:
                        for record_count in range(0,segment_config['record_rate_per_hr']):
                            # Calculate a random timestamp within the current hour
                            seconds_so_far = hour_of_day * 60 * 60
                            delta = timedelta(seconds=(random.randint(0, 60 * 60) + seconds_so_far))
                            timestamp = day_start + delta

                            # Write the log line to the file
                            line = "<13>" + timestamp.strftime("%b %d %H:%M:%S") + " " + data_source_name + " " + timestamp.strftime("%b%d%Y %H:%M:%S") + " accept 10.94.82.7 product: FG; src: 10.94.85.141; s_port: 53049; dst: 192.168.151.175; service: 443; proto: udp; rule: ;__policy_id_tag: product=VPN-1 & FireWall-1[db_tag={5FF580E8-1C46-F44B-A8D8-1CDC291BCDE4};mgmt=testMGMT;date=1533313654;policy_name=Standard];has_accounting: 0;i/f_dir: inbound;origin_sic_name: CN=test_origin_sic_name: 9096cbb1;src_user_name: testSourceUser\n"
                            f.write(line)
                    # TODO 'for data_source_name in anomalous_data_source_names[:segment_config.num_anomalous_data_sources]' - also generate the normal data and the abnormal data for the anomalous sources
                    # Need to make sure you are generating the anomaly only in one place, and the rest of the time is fine        

                # Increment the current date by one day
                current_date += timedelta(days=1)

            print(f"Log file written to {filename}")

            create_segment = bool(input("Do you want to create another log segment? (yes/no) ") == "yes")

if __name__ == "__main__":
    main()