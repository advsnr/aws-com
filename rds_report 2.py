#!/usr/bin/env python

import boto3
import csv
import datetime
from datetime import date
import subprocess


regions = ['us-east-1','us-west-1', 'us-west-2']

file_name = 'rds_report.csv'
file_location = '/tmp/'+file_name

with open(file_location,'w') as file:
    header = ['DB_identifier', 'Size', 'Status', 'Region',
              'Multi-AZ', 'StorageType', 'Storage(GiB)', 'IOPS']
    writer = csv.DictWriter(file, fieldnames=header, extrasaction='ignore')
    writer.writeheader()


    for region in regions:
        session = boto3.session.Session(region_name=region)
        rds_client = session.client('rds')
        rds_instance = rds_client.describe_db_instances()
        #paginator = rds_client.get_paginator('describe_db_instances').paginate()
        #paginate = RDS.Client.describe_db_instances()
        #rds_paginator = paginator.paginate
        for i in rds_instance['DBInstances']:
            dbInstanceName = i['DBInstanceIdentifier']
            dbInstanceEngine =i['DBInstanceClass']
            dbInstanceStatus = i['DBInstanceStatus']
            db_storage = i['AllocatedStorage']
            db_storagetype = i['StorageType']
            #iops = i['Iops']
            MultiAZ= i['MultiAZ']
            output = {
                'DB_identifier': dbInstanceName,
                'Size': dbInstanceEngine,
                'Status': dbInstanceStatus,
                'Region': region,
                'Storage(GiB)': db_storage,
                'StorageType': db_storagetype,
                #'IOPS': int(iops),
                'Multi-AZ': MultiAZ,
            }
            writer.writerow(output)
        print(output)


         #   State = i.state['Name']
          #  Launchtime = i.launch_time
         #   InstanceType = i.instance_type
          #  Platform = str(i.platform)
          #  currenttime = datetime.datetime.now(Launchtime.tzinfo)
          #  time_diff = currenttime - Launchtime
          #  uptime = str(time_diff)
          #  if i.state['Name'] == 'stopped':
          #      uptime = ' '
          #  if i.platform == None:
          #      Platform = 'Unix/Linux'

          #  if i.tags:
          #      for idx, tag in enumerate(i.tags, start=1):
          #          if tag['Key'] == 'Name':
          #              Instancename = tag['Value']
          #          if tag['Key'] == 'build_user_id':
          #              Instancebuilder = tag['Value']
          #              output = {
          #                          'Instancename': Instancename,
          #                          'Id': Id,
          #                          'State': State,
          #                          'Platform': str(Platform),
          #                          'InstanceType': InstanceType,
          #                          'Launchedtime': str(Launchtime),
          #                          'Region': region,
          #                          'Uptime': uptime,
          #                          'Instancebuilder': Instancebuilder
          #                          }
          #              writer.writerow(output)
