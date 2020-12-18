#!/usr/bin/env python

import boto3
import csv
import datetime
from datetime import date
import subprocess


regions = ['us-west-2', 'us-west-1', 'us-east-1', 'us-east-2', 'ap-south-1', 'ap-southeast-1', 'ca-central-1', 'eu-west-1', 'eu-west-3' ]

file_name = 'rds_report.csv'
file_location = '/tmp/'+file_name

with open(file_location,'w') as file:
    header = ['DB_identifier', 'Size', 'Status', 'Region',
              'Multi-AZ', 'StorageType', 'Storage(GiB)']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()


    for region in regions:
        session = boto3.session.Session(region_name=region)
        rds_client = session.client('rds')
        rds_instance = rds_client.describe_db_instances()
        for i in rds_instance['DBInstances']:
            dbInstanceName = i['DBInstanceIdentifier']
            dbInstanceEngine =i['DBInstanceClass']
            dbInstanceStatus = i['DBInstanceStatus']
            db_storage = i['AllocatedStorage']
            db_storagetype = i['StorageType']
            MultiAZ= i['MultiAZ']
            output = {
                'DB_identifier': dbInstanceName,
                'Size': dbInstanceEngine,
                'Status': dbInstanceStatus,
                'Region': region,
                'Storage(GiB)': db_storage,
                'StorageType': db_storagetype,
                'Multi-AZ': MultiAZ,
            }
            writer.writerow(output)
        print(output)
