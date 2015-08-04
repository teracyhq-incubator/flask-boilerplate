# -*- coding: utf-8 -*-

"""utils module"""

import os
import collections


INSTANCE_FOLDER_PATH = os.path.join('/tmp', 'instance')


# thanks to https://github.com/jpadilla/pyjwt/blob/master/jwt/utils.py#L25
def merge_dict(original, updates):
    """Merge 2 dicts into one
    :param original the original dict
    :param updates the updates dict to be merged
    :return the merged dict
    """
    if not updates:
        return original

    try:
        merged_options = original.copy()
        merged_options.update(updates)
    except (AttributeError, ValueError) as ex:
        raise TypeError('original and updates must be a dictionary: %s' % ex)

    return merged_options


def extract_dict(origin_dict, extracted_keys=None, ignored_keys=None, ignored_values=(None, ''),
                 func=None):
    """Extract specified keys with a filter from a dictionary

    :param origin_dict the origin dictionary
    :param extracted_keys the optional sequence of keys to be extracted, if None, all keys are
                          extracted
    :param ignored_keys  the optional sequence of keys to be ignored, if None, no keys are ignored
    :param ignored_values the optional filter, by default will ignore None and empty string values
    :param func  the optional filter function taking key and value and return True or False to
                 indicate item acceptance. If None func, accept all items.

    :return the extracted dictionary
    """

    if not isinstance(origin_dict, dict):
        raise ValueError('origin_dict must be a dict')

    if extracted_keys is None:
        extracted_keys = origin_dict.keys()

    if ignored_keys is None:
        ignored_keys = ()

    if func is None:
        func = lambda key, value: True

    if not isinstance(extracted_keys, collections.Sequence):
        raise ValueError('extracted_keys must be a sequence')

    if not isinstance(ignored_keys, collections.Sequence):
        raise ValueError('ignored_keys must be a sequence')

    if not isinstance(ignored_values, collections.Sequence):
        raise ValueError('ignored_values must be a sequence')

    if not callable(func):
        raise ValueError('func must be a function')

    return dict((k, v) for k, v in
                origin_dict.iteritems() if
                k in extracted_keys and k not in ignored_keys and
                v not in ignored_values and func(k, v))


def add_filters(query, op_sequence, accepted_keys):
    """Add more filters to an existing query.

    It's assumed that query is created from model_class.query

    :param query existing query
    :param op_sequence sequence of op_item with the following format:
                       op_item = {"key": <fieldname>, "op": <operator>, "value": <value>}

                        Some common supported operators:
                        eq, ne
                        lt, le
                        gt, ge
    :param accepted_keys the sequence of accepted keys

    :return the updated query with added filters
    """

    if query is None:
        raise ValueError('query must not be None')

    if not isinstance(op_sequence, collections.Sequence):
        raise ValueError('op_list must be a sequence')

    if accepted_keys is None or len(accepted_keys) == 0:
        return query

    model_class = query.column_descriptions[0]['type']  # assuming

    for op_item in op_sequence:
        key = op_item.get('key')
        operator = op_item.get('op')
        value = op_item.get('value')

        if key not in accepted_keys:
            continue

        # TODO(hoatle): validate key, op, value for security reason?

        column = getattr(model_class, key)

        if not column:
            raise ValueError('Invalid filter column: {}'.format(key))

        lst = filter(lambda e: hasattr(column, e % operator), ['%s', '%s_', '__%s__'])
        if len(lst) > 0:
            attr = lst[0] % operator
        else:
            raise ValueError('Invalid filter operator: {}'.format(operator))

        query = query.filter(getattr(column, attr)(value))
    return query
