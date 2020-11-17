import boto3
import csv
import datetime
import boto.ec2
from dateutil.parser import *
import subprocess


regions = ['us-west-2', 'us-west-1', 'us-east-1']


with open('ec2_list_1.csv', 'a', newline='') as file:
    header = ['Instancename', 'Id', 'State',
              'Platform', 'InstanceType', 'Launchedtime', 'Region', 'Uptime']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()

    for region in regions:
        session = boto3.session.Session(region_name=region)
        ec2 = session.resource('ec2')

        for i in ec2.instances.all():
            Id = i.id
            State = i.state['Name']
            Launchtime = i.launch_time
            InstanceType = i.instance_type
            Platform = i.platform
            currenttime = datetime.datetime.now(Launchtime.tzinfo)
            lt_delta = currenttime - Launchtime
            uptime = str(lt_delta)
            if i.tags:
                for idx, tag in enumerate(i.tags, start=1):
                    if tag['Key'] == 'Name':
                        Instancename = tag['Value']
                        output = {
                                    'Instancename': Instancename,
                                    'Id': Id,
                                    'State': State,
                                    'Platform': str(Platform),
                                    'InstanceType': InstanceType,
                                    'Launchedtime': str(Launchtime),
                                    'Region': region,
                                    'Uptime': uptime
                                    }
                        writer.writerow(output)
