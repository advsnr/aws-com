#!/usr/bin/env python
# test using: python -m asg_instances -v
import boto3
import unittest
import datetime


def is_asg(instances):
    result = []
    for instance in instances:
        asg = get_asg(instance)
        if asg:
            result.append(asg)
    return result

def is_not_asg(instances):
    result = []
    for instance in instances:
        asg = get_asg(instance)
        if not asg:
            result.append(instance)
    return result

def get_asg(instance):
    result = None
    client =  boto3.client('autoscaling', instance['placement']['availability_zone'][:-1] )
    response = client.describe_auto_scaling_instances(InstanceIds=[instance['instance_id']])
    print(response)
    if len(response['AutoScalingInstances']) == 1:
        result = response['AutoScalingInstances'][0]
    return result

class FilterModule(object):

    """ filters for ec2 instances member of autoscaling group """

    def filters(self):
        return {
            'is_asg': is_asg,
            'is_not_asg': is_not_asg
        }


class TestAsgInstances(unittest.TestCase):

    def test_get_asg(self):
       l = { 'instance_id': 'i-031ad43844d51146a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}
       self.assertNotEqual(get_asg(l), None)

    def test_get_not_asg(self):
       l = { 'instance_id': 'i-00d020c6c46f1da9a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}
       self.assertEqual(get_asg(l), None)

    def test_is_asg_ok(self):
      l = [{ 'instance_id': 'i-031ad43844d51146a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}]
      self.assertNotEqual(is_asg(l), [])

    def test_is_asg_empty(self):
      l = [{ 'instance_id': 'i-00d020c6c46f1da9a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}]
      self.assertEqual(is_asg(l), [])

    def test_is_not_asg_empty(self):
      l = [{ 'instance_id': 'i-031ad43844d51146a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}]
      self.assertEqual(is_not_asg(l), [])

    def test_is_not_asg(self):
      l = [{ 'instance_id': 'i-00d020c6c46f1da9a', 'placement': {'availability_zone': 'ap-southeast-1a'  }}]
      self.assertNotEqual(is_not_asg(l), [])

if __name__ == '__main__':
    unittest.main()
