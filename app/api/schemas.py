from marshmallow import Schema as SchemaOrigin
import re

def fields_to_dict(fields):
    """ FIXME:
        https://www.debuggex.com/r/24QPqzm5EsR0e2bt
        https://www.debuggex.com/r/0SjmBL55ySna0kFF
        https://www.debuggex.com/r/Vh9qvHkCV4ZquS14
    """
    result = {}

    if not fields or len(fields.strip()) == 0:
        return result

    look_behind_keys = re.findall('{(\w*?),', fields)
    look_behind_pattern_list = ['(?<!{' + k + ')' for k in look_behind_keys]

    # FIXME: '(?<!{[^,]*),<look_forward_pattern>' will trigger "look-behind requires fixed-width pattern"
    look_behind_pattern = ''.join(look_behind_pattern_list)

    # FIXME: not support nested bracket: field{id,name,description{abc,def}}
    look_forward_pattern = '(?![a-zA-Z0-9,\}:\[\]]*?})'

    # sample pattern: '(?<!{id)(?<!{email),<look_forward_pattern>'
    re_pattern = look_behind_pattern + ',' + look_forward_pattern

    for key in re.split(re_pattern, fields):
        key = key.strip()
        value = {}
        if key.find('{') > -1:
            # get sub fields: field{<sub_fields>} and assign its value
            sub_field = re.findall('{(.*)}', key)
            value = fields_to_dict(sub_field[0])
            # clean key
            key = re.sub('{(.*)}', '', key)

        if key.find('[') > -1:
            # get & set slide range: [a:b]
            value['__slice'] = re.findall('\[(.*)\]', key)[0]
            # clean key
            key = re.sub('\[(.*)\]', '', key)

        result[key] = value

    return result


def filter_dict(origin_dict, fields=None):
    result = {}
    fields_dict = fields_to_dict(fields)

    if len(fields_dict) == 0:
        result = origin_dict.copy()
    else:
        for key, value in fields_dict.iteritems():
            result[key] = origin_dict[key]

    return result


class Schema(SchemaOrigin):

    def dump(self, obj, many=None, update_fields=True, fields=None, **kwargs):
        result = super(Schema, self).dump(obj, many, update_fields, **kwargs)
        return filter_dict(result, fields)
