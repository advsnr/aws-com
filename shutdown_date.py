#!/usr/bin/env python
# test using: python -m shutdown_date -v

import unittest
import datetime

today = datetime.date.today()

def is_shutdowndate(instance):
    result = False
    print (instance)
    if instance['tags']:
      if 'shutdown_date' in instance['tags'].keys():
        shutdown_date = instance['tags']['shutdown_date']
        print(shutdown_date)
        try:
            if today > datetime.datetime.strptime(shutdown_date, "%Y-%m-%d").date():
                result = True
        except:
            print(today)
      else:
          result = True
    return result

def is_shutdowndates(instances):
   result = []
   for instance in instances:
     if is_shutdowndate(instance):
      result.append(instance)
   return result

class FilterModule(object):

    """ filters for ec2 instances by shutdown_date tags """

    def filters(self):
        return {
            'is_shutdown_date': is_shutdowndate ,
            'is_shutdown_dates': is_shutdowndates
        }



class TestShutdownDate(unittest.TestCase):

    def test_with_no_tags(self):
      l = { 'tags': {}}
      self.assertEqual(is_shutdowndate(l), False)

    def test_with_tag_key(self):
      l = { 'tags': {'foo': 'bar'}}
      self.assertEqual(is_shutdowndate(l), True)

    def test_with_tag_date(self):
      l = { 'tags': {'shutdown_date': '2021-02-02'}}
      self.assertEqual(is_shutdowndate(l), True)

    def test_with_tag_date_bogus(self):
      l = { 'tags': {'shutdown_date': '21-02-04'}}
      self.assertEqual(is_shutdowndate(l), False)

    def test_with_tag_date_today(self):
      l = { 'tags': {'shutdown_date': today}}
      self.assertEqual(is_shutdowndate(l), False)

    def test_with_tag_dates_today(self):
      l = [{ 'tags': {'shutdown_date': today}}]
      self.assertEqual(is_shutdowndates(l), [])

    def test_with_tag_dates(self):
      l = [{ 'tags': {'shutdown_date': '2021-02-05' }}]
      self.assertEqual(is_shutdowndates(l), l)


if __name__ == '__main__':
    unittest.main()
