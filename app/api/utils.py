import re

from ..utils import extract_dict, parse_number


SUPPORTED_OPS = frozenset(['eq', 'ne', 'lt', 'le', 'gt', 'ge', 'lk', 'nl', 'in', 'ni', 'ct', 'mc'])

# sql alchemy ops mapper
SA_OPS_MAPPER = {
    'eq': 'eq',
    'ne': 'ne',
    'lt': 'lt',
    'le': 'le',
    'gt': 'gt',
    'ge': 'ge',
    'lk': 'like',
    'nl': 'notlike',
    'in': 'in_',
    'ni': 'notin_',
    'ct': 'contains',
    'mc': 'match'
}

FILTER_KEY_RE = re.compile(r'^(?P<key>\w*[a-zA-Z0-9])+__(?P<op>%s)$' % '|'.join(SUPPORTED_OPS))


def extract_filters(args):
    """Extracts filters then return filters and new args without filter keys"""
    filters = []
    # parse filters ?field__op=value => convert to [{key: field, op: op, value:value}, ]
    filter_dict = extract_dict(args, func=lambda k, v: FILTER_KEY_RE.match(k))

    for key, value in filter_dict.iteritems():
        matcher = FILTER_KEY_RE.match(key)
        key = matcher.group('key')
        operator = matcher.group('op')
        value = parse_number(value)

        if operator == 'in' or operator == 'ni':
            value = map(parse_number, value.split(','))

        filters.append({
            'key': key,
            'op': SA_OPS_MAPPER.get(operator),
            'value': value
        })

    args = extract_dict(args, ignored_keys=filter_dict.keys())

    return filters, args
