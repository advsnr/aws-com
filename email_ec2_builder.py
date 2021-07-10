#!/usr/bin/env python
# test using: python -m email_ec2_builder -v

import unittest


# Function to read email addresses for ec2_report.csv file. List of emails
def get_contacts(mail_to, filename = '/tmp/ec2_report.csv'):
    emails = []
    with open(filename, mode = 'r') as contacts_file:
        for instancebuilder in contacts_file:
            email = instancebuilder.split(',')[-1].strip()
            if '@' in email:
                if email not in emails:
                  emails.append(email)
                  print(email)
    print (emails)
    return emails


class FilterModule(object):

    """ filters for ec2 instances need to be printed in csv file """

    def filters(self):
        return {
            'get_contacts': get_contacts
        }


class Testemail(unittest.TestCase):

    def test_send_email_with_emailadress(self):
        output = get_contacts('', './test.csv')
        expect = ['srahman@cleo.com']
        self.assertEqual(output, expect)

    def test_send_email_without_emailadress(self):
        output = get_contacts('', './blank.csv')
        expect = []
        self.assertEqual(output, expect)


if __name__ == '__main__':
    unittest.main()
