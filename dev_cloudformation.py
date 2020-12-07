#!/usr/bin/env python

import boto3
import csv
import datetime
from datetime import date
import subprocess


regions = ['us-east-1', 'us-west-1', 'us-west-2']

file_name = 'cloudformation_report.csv'
file_location = '/tmp/'+file_name

with open(file_location, 'w') as file:
    header = ['StackName', 'Status', 'CreatedTime']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()

    for region in regions:
        session = boto3.session.Session(region_name=region)
        cf_client = session.resource('cloudformation')
        #cf_response = cf_client.describe_stacks()
        for i in cf_client.stacks.all():
            StackName = i.stack_name
            StackStatus = i.stack_status
            Createdtime = i.creation_time

            output = {
                'StackName': StackName,
                'Status': StackStatus,
                'CreatedTime': Createdtime
            }
            writer.writerow(output)
        #print(output)
