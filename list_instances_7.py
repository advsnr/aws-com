import boto3
import csv
import datetime
from datetime import date
import subprocess


regions = ['us-west-2', 'us-west-1', 'us-east-1', 'us-east-1', 'us-east-2','ap-south-1', 'ap-southeast-1', 'ca-central-1', 'eu-west-1', 'eu-west-3']

today = date.today()
file_name = 'ec2_instance_report_'+today.strftime("%m-%d-%y")+'.csv'
s3_bucket = "srahman-test"
file_location = '/tmp/'+file_name

with open(file_location,'w') as file:
    header = ['Instancename', 'Id', 'State',
              'Platform', 'InstanceType', 'Launchedtime', 'Region', 'Uptime']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()


    for region in regions:
        session = boto3.session.Session(region_name=region)
        ec2 = session.resource('ec2')
        cloudtrail = boto3.client('cloudtrail')
        res = cloudtrail.lookup_events()
        for i in ec2.instances.all():
            Id = i.id
            State = i.state['Name']
            Launchtime = i.launch_time
            InstanceType = i.instance_type
            Platform = str(i.platform)
            currenttime = datetime.datetime.now(Launchtime.tzinfo)
            time_diff = currenttime - Launchtime
            uptime = str(time_diff)
            if i.state['Name'] == 'stopped':
                uptime = ' '
            if i.platform == None:
                Platform = 'Unix/Linux'

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
s3 = boto3.client('s3')
s3.upload_file(file_location, s3_bucket, file_name)
