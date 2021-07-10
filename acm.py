# -*- coding: utf-8 -*-
# test using: python -m acm -v

import unittest
import datetime
from datetime import date
from datetime import datetime
from dateutil import relativedelta


time_format = '%Y-%m-%dT%H:%M:%S+00:00'

def delta_days(date):
    then = datetime.strptime(date, time_format)
    now = datetime.now()
    return then - now

def arn_with_remaining(certificates, cutoff=30):
    ret = []
    for certificate in certificates:
        remaining = delta_days(certificate['not_after'])
        if remaining.days > 0 and remaining.days < cutoff:
            ret.append(certificate['certificate_arn'] + ', ' + str(remaining.days))
    return ret


class FilterModule(object):

    """ filters for ACM certificate attributes """

    def filters(self):
        return {
            'acm_remaining': arn_with_remaining
        }


class TestAcmFilter(unittest.TestCase):

    def test_with_expiration(self):
        later = datetime.now() + relativedelta.relativedelta(days=15)
        future = later.strftime(time_format)
        l = [
            { 'certificate_arn': 'ARN', 'not_after': future, 'bogus': 'junk'}
        ]
        self.assertEqual(arn_with_remaining(l), ['ARN, ' + str(delta_days(future).days) ])

    def test_with_expiration_expired(self):
        later = datetime.now() + relativedelta.relativedelta(days=-15)
        future = later.strftime(time_format)
        l = [
            { 'certificate_arn': 'ARN', 'not_after': future, 'bogus': 'junk'}
        ]
        self.assertEqual(arn_with_remaining(l), [])

    def test_with_expiration_long_time(self):
        later = datetime.now() + relativedelta.relativedelta(days=91)
        future = later.strftime(time_format)
        l = [
            { 'certificate_arn': 'ARN', 'not_after': future, 'bogus': 'junk'}
        ]
        self.assertEqual(arn_with_remaining(l), [])

    def test_with_expiration_cutoff_include(self):
        later = datetime.now() + relativedelta.relativedelta(days=15)
        future = later.strftime(time_format)
        l = [
            { 'certificate_arn': 'ARN', 'not_after': future, 'bogus': 'junk'}
        ]
        self.assertEqual(arn_with_remaining(l, 16), ['ARN, ' + str(delta_days(future).days) ])

    def test_with_expiration_cutoff_exclude(self):
        later = datetime.now() + relativedelta.relativedelta(days=15)
        future = later.strftime(time_format)
        l = [
            { 'certificate_arn': 'ARN', 'not_after': future, 'bogus': 'junk'}
        ]
        self.assertEqual(arn_with_remaining(l, 14), [])


if __name__ == '__main__':
    unittest.main()
