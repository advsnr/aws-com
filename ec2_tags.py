# -*- coding: utf-8 -*-
# test using: python -m ec2_tags -v

import unittest


def with_keys(instances, keys):
    ret = []

    if type(keys) is str:
        for instance in instances:
            if keys in instance['tags'].keys():
                ret.append(instance)

    if type(keys) is list:
        for instance in instances:
            for key in keys:
                if key in instance['tags'].keys():
                    ret.append(instance)
                    break
    return ret


def without_keys(instances, keys):
    ret = []

    if type(keys) is str:
        for instance in instances:
            if keys not in instance['tags'].keys():
                ret.append(instance)

    if type(keys) is list:
        for instance in instances:
            for key in keys:
                if key not in instance['tags'].keys():
                    ret.append(instance)
                    break
    return ret


def with_values(instances, values):
    ret = []

    if type(values) is str:
        for instance in instances:
            if values in instance['tags'].values():
                ret.append(instance)

    if type(values) is list:
        for instance in instances:
            for value in values:
                if value in instance['tags'].values():
                    ret.append(instance)
                    break
    return ret

def with_key_value(instances, key, value):
    ret = []

    for instance in instances:
        if key in instance['tags'] and value == instance['tags'][key]:
            ret.append(instance)

    return ret

def without_key_value(instances, key, value):
    ret = []

    for instance in instances:
        if key not in instance['tags'] or value != instance['tags'][key]:
            ret.append(instance)

    return ret

def without_name_like(instances, value):
    ret = []

    for instance in instances:
        if 'Name' not in instance['tags'] or value not in instance['tags']['Name']:
            ret.append(instance)

    return ret

class FilterModule(object):

    """ filters for ec2 instances by tags """

    def filters(self):
        return {
            'ec2_tags_with_keys': with_keys,
            'ec2_tags_with_values': with_values,
            'ec2_tags_with_key_value': with_key_value,
            'ec2_tags_without_key_value': without_key_value,
            'ec2_tags_without_keys': without_keys,
            'ec2_tags_without_name_like': without_name_like
        }


class TestEc2Tags(unittest.TestCase):

    def test_with_keys_single(self):
        l = [
            { 'tags': {'foo': 'bar', 'bar': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'baz', 'oof': 'bar', 'baz': 'quux'}}
        ]
        self.assertEqual(with_keys(l, 'foo'), l)
        self.assertEqual(with_keys(l, 'fob'), [])
        self.assertEqual(with_keys(l, 'oof'), [l[1]])

    def test_with_keys_array(self):
        l = [
            { 'tags': {'foo': 'bar', 'rab': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'baz', 'oof': 'rab', 'baz': 'quux'}}
        ]
        self.assertEqual(with_keys(l, ['foo']), l)
        self.assertEqual(with_keys(l, ['fob']), [])
        self.assertEqual(with_keys(l, ['oof']), [l[1]])
        self.assertEqual(with_keys(l, ['rab', 'oof']), l)

    def test_with_values_single(self):
        l = [
            { 'tags': {'foo': 'bar', 'bar': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'baz', 'oof': 'bar', 'baz': 'quux'}}
        ]
        self.assertEqual(with_values(l, 'bar'), l)
        self.assertEqual(with_values(l, 'fob'), [])
        self.assertEqual(with_values(l, 'baz'), [l[1]])

    def test_with_values_array(self):
        l = [
            { 'tags': {'foo': 'bar', 'rab': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'bar', 'oof': 'rab', 'baz': 'quux'}}
        ]
        self.assertEqual(with_values(l, ['bar']), l)
        self.assertEqual(with_values(l, ['fob']), [])
        self.assertEqual(with_values(l, ['rab']), [l[1]])
        self.assertEqual(with_values(l, ['qux', 'quux']), l)

    def test_without_keys_single(self):
        l = [
            { 'tags': {'foo': 'bar', 'bar': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'baz', 'oof': 'bar', 'baz': 'quux'}}
        ]
        self.assertEqual(without_keys(l, 'fo'), l)
        self.assertEqual(without_keys(l, 'foo'), [])
        self.assertEqual(without_keys(l, 'bar'), [l[1]])

    def test_without_keys_array(self):
        l = [
            { 'tags': {'foo': 'bar', 'rab': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'baz', 'oof': 'rab', 'baz': 'quux'}}
        ]
        self.assertEqual(without_keys(l, ['fo']), l)
        self.assertEqual(without_keys(l, ['foo']), [])
        self.assertEqual(without_keys(l, ['rab']), [l[1]])
        self.assertEqual(without_keys(l, ['rb', 'of']), l)

    def test_with_key_value(self):
        l = [
            { 'tags': {'foo': 'bar', 'rab': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'bar', 'oof': 'rab', 'baz': 'quux'}}
        ]
        self.assertEqual(with_key_value(l, 'foo', 'bar'), l)
        self.assertEqual(with_key_value(l, 'foo', 'foo'), [])
        self.assertEqual(with_key_value(l, 'fo', 'bar'), [])
        self.assertEqual(with_key_value(l, 'oof', 'rab'), [l[1]])
        self.assertEqual(with_key_value(l, 'baz', 'qux'), [l[0]])

    def test_without_key_value(self):
        l = [
            { 'tags': {'foo': 'bar', 'rab': 'oof', 'baz': 'qux'}},
            { 'tags': {'foo': 'bar', 'oof': 'rab', 'baz': 'quux'}}
        ]
        self.assertEqual(without_key_value(l, 'oof', 'bar'), l)
        self.assertEqual(without_key_value(l, 'foo', 'rab'), l)
        self.assertEqual(without_key_value(l, 'foo', 'bar'), [])
        self.assertEqual(without_key_value(l, 'oof', 'rab'), [l[0]])
        self.assertEqual(without_key_value(l, 'baz', 'qux'), [l[1]])

    def test_without_name_like(self):
        l = [
            { 'tags': {'foo': 'bar', 'Name': 'qux'}},
            { 'tags': {'foo': 'bar', 'Name': 'qix'}}
        ]
        self.assertEqual(without_name_like(l, 'a'), l)
        self.assertEqual(without_name_like(l, 'bar'), l)
        self.assertEqual(without_name_like(l, 'x'), [])
        self.assertEqual(without_name_like(l, 'i'), [l[0]])
        self.assertEqual(without_name_like(l, 'u'), [l[1]])

if __name__ == '__main__':
    unittest.main()
