# -*- coding: utf-8 -*-

"""support for webargs"""

from webargs import Arg


def _string_to_boolean(value):
    mappings = {
        'true': True,
        'false': False,
        '1': True,
        '0': False
    }

    return mappings.get(value.lower(), True)

# false or 0 => False; others => True
BoolArg = Arg(bool, use=_string_to_boolean)
