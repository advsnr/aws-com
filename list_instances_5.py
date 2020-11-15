import boto3
import csv
import datetime
ec2 = boto3.resource('ec2')
ec21 = boto3.client('ec2')
response1 = ec21.describe_instances().get('Reservation')

with open('/Users/srahman/Documents/Shamim_works/gitrepo/ev/ansible/playbooks/devaws/ec2_list_1.csv', 'a', newline='') as file:
    header = ['Instancename', 'Id', 'State',
              'Platform', 'InstanceType', 'Launched', 'RegionNames']
    writer = csv.DictWriter(file, fieldnames=header)
    writer.writeheader()
    for i in ec2.instances.all():
        Id = i.id
        State = i.state['Name']
        Launched = i.launch_time
        InstanceType = i.instance_type
        Platform = i.platform
        RegionNames= i.region

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
                            'Launched': str(Launched),
                            'RegionNames': str(RegionNames)
                            }
                    writer.writerow(output)
