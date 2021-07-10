#!/usr/bin/env python
# test using: python -m running_seconds -v

import unittest
import datetime
from datetime import datetime
import time


def running_seconds(instances, threshold=86400):
    result = []
    for instance in instances:
     if is_threshold(instance['launch_time'], threshold):
      result.append(instance)
    return result


def is_threshold(launch_time, threshold=86400):
    result= False
    launchtime = launch_time
    ltime = launchtime.timestamp()
    currenttime1 = datetime.now()
    curenttime1 = currenttime1.timestamp()
    time = currenttime1.timestamp()
    print(currenttime1)
    uptime = time - ltime
    print(uptime)
    if  uptime > threshold:
        result = True
    return result


class FilterModule(object):

    """ filters for ec2 instances by running_seconds times """

    def filters(self):
        return {
            'running_seconds': running_seconds
        }


class TestRunningSeconds(unittest.TestCase):

    def test_running_seconds1(self):
      l = datetime.strptime('2021-02-02', '%Y-%M-%d')
      self.assertEqual(is_threshold(l), True)

    def test_running_seconds2(self):
      l = datetime.now()
      self.assertEqual(is_threshold(l), False)

if __name__ == '__main__':
    unittest.main()
