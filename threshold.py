#!/usr/bin/env python
# test using: python -m threshold -v

import unittest
import datetime
from datetime import datetime
import time


def threshold(instances, threshold=86400):
    result = []
    for instance in instances:
     if is_threshold(instance['launch_time'], threshold):
      result.append(instance)
    return result


def is_threshold(launch_time, threshold=86400):
    result= False
    ltime = datetime.strptime(launch_time[:19], '%Y-%m-%dT%H:%M:%S')
    # print(ltime)
    currenttime = datetime.utcnow()
    print(currenttime)
    uptime = (currenttime - ltime).total_seconds()
    print(uptime)
    if  uptime > threshold:
        result = True
    return result


class FilterModule(object):

    """ filters for ec2 instances by running_seconds times """

    def filters(self):
        return {
            'threshold': threshold
        }


class TestRunningSeconds(unittest.TestCase):

    def test_running_seconds1(self):
      l = '2021-02-09T20:04:52+00:00'
      self.assertEqual(is_threshold(l), True)

    def test_running_seconds2(self):
       l = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S')
       self.assertEqual(is_threshold(l), False)

if __name__ == '__main__':
    unittest.main()
