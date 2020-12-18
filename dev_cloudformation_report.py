#!/usr/bin/env python

import boto3
import csv
import datetime
from datetime import date
import subprocess
from collections import defaultdict

regions = ['us-west-2', 'us-west-1', 'us-east-1',
           'us-east-2', 'ap-south-1', 'ap-southeast-1', 'ca-central-1', 'eu-west-1', 'eu-west-3']

ev_names = ["Clarify", "Harmony", "Inf"]
StackName = defaultdict(list)

file_name = 'cloudformation_stack_report.csv'
file_location = '/tmp/'+file_name

with open(file_location, 'w') as file:
    header = ['StackName', 'Status', 'Createdtime', 'Region']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()


    for region in regions:
        session = boto3.session.Session(region_name=region)
        cf_client = session.resource('cloudformation')
        for i in cf_client.stacks.all():
            StackStatus = i.stack_status
            Createdtime = i.creation_time
            StackName1 = i.stack_name


            for ev_name in ev_names:
                if ('-' + ev_name) in StackName1:

                    output = {'StackName': StackName1,
                               'Createdtime': Createdtime,
                                'Status': StackStatus,
                                'Region': region
                                }


                    writer.writerow(output)
