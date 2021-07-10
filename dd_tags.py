# filter to convert from [key:value] dict to ['key:value'] list for use in datadog configs
from __future__ import (absolute_import, division, print_function)
__metaclass__ = type


import collections
import itertools
import math

from ansible import errors
from ansible.module_utils import basic


def to_dd_tags(tag_dict):
    # (dict) -> list
    if not isinstance(tag_dict, dict):
        raise errors.AnsibleFilterError(
            "|to_dd_tags expects a dictionary, got " + repr(tag_dict))
    tag_dict_keys = tag_dict.keys()
    tag_dict_values = tag_dict.values()
    tag_dict_items = tag_dict.items()
    error_l = []

    # Tag rules: https://docs.datadoghq.com/tagging/
    for illegal in (k for k in tag_dict_keys if not k[0].isalpha()):
        errstr = 'DD tags must start with a letter, got key "{}"'.format(illegal)
        error_l.append(errstr)
    for pair in (pair for pair in tag_dict_items if sum(len(i) for i in pair) > 199):
        errstr = 'Maximum tag length is 200, got "{}:{}"'.format(*pair)
        error_l.append(errstr)
    for illegal in (k for k in tag_dict_keys if ':' in k):
        errstr = 'Keys cannot contain ":", got "{}"'.format(k)
        error_l.append(errstr)
    for illegal in (v for v in tag_dict_values if v[-1] == ':'):
        errstr = 'Values cannot end with ":", got "{}"'.format(v)
        error_l.append(errstr)

    if error_l:
        raise errors.AnsibleFilterError(
            "|to_dd_tags failed; reasons: {}\nInput:\n{}".format('\n'.join(error_l), tag_dict)
        )

    # Sorting makes the output deterministic, and avoids needless changes downstream
    dd_tags = sorted('{}:{}'.format(*kv) for kv in tag_dict_items)
    return dd_tags


def from_dd_tags(tag_list):
    # (list) -> dict
    if not isinstance(tag_list, list):
        raise errors.AnsibleFilterError(
            "|from_dd_tags expects a list, got " + repr(tag_list))
    broken_entries = [item for item in tag_list if not isinstance(item, str)]
    if broken_entries:
        raise errors.AnsibleFilterError(
            r"|from_aws_tags arguments must be strings, found entries " + ', '.join(
                repr(broken_entries))
        )
    as_tuples = (_split_keyvalue(item) for item in tag_list)
    as_dict = {key: value for key, value in as_tuples}
    return as_dict


def _split_keyvalue(entry):
    # (list) -> tuple
    pieces = str(entry).split(':', 1)
    if len(pieces) == 1:
        return (pieces[0], None)
    return pieces


def _testme():
    # () -> None
    # Just some basic tests
    input_1 = {
        'purpose': 'elasticsearch',
        'instance_id': 'i-03253542532506',
        'monitor': 'true'
    }
    e_output_1 = ['purpose:elasticsearch',
                  'instance_id:i-03253542532506',
                  'monitor:true']
    a_output_1 = to_dd_tags(input_1)
    # Broken into two commands for more visibility
    print('test 1:')
    print('expected: ' + repr(sorted(e_output_1)))
    print('actual:   ' + repr(sorted(a_output_1)))
    assert not set(e_output_1).symmetric_difference(a_output_1)

    e_input_2 = list(e_output_1)
    e_output_2 = dict(input_1)
    a_output_2 = from_dd_tags(e_input_2)
    print()
    print('test 2:')
    print('expected: ' + repr(e_output_2))
    print('actual:   ' + repr(a_output_2))
    assert e_output_2 == a_output_2


class FilterModule(object):
    ''' Ansible aws tag filter '''

    def filters(self):
        filters = {
            'to_dd_tags': to_dd_tags,
            'from_dd_tags': from_dd_tags
        }

        return filters
