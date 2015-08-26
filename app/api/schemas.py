from marshmallow import Schema as SchemaOrigin
from marshmallow.schema import MarshalResult
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

    # look_behind_keys = re.findall('{(\w*?),', fields)
    # look_behind_pattern_list = ['(?<!{' + k + ')' for k in look_behind_keys]

    # # FIXME: '(?<!{[^,]*),<look_forward_pattern>' will trigger "look-behind requires
    # # fixed-width pattern"
    # look_behind_pattern = ''.join(look_behind_pattern_list)

    # # FIXME: not support nested bracket: field{id,name,description{abc,def}}
    # look_forward_pattern = '(?![a-zA-Z0-9,\}:\[\]]*?})'

    # # sample pattern: '(?<!{id)(?<!{email),<look_forward_pattern>'
    # re_pattern = look_behind_pattern + ',' + look_forward_pattern

    splited_fields = []
    word_block = ''
    bracket_counter = 0
    field_len = len(fields)
    for index, word in enumerate(fields):

        if word == '{':
            bracket_counter = bracket_counter + 1

        if word == '}':
            bracket_counter = bracket_counter - 1
        

        # move to new word block
        if word == ',' and bracket_counter == 0:
            splited_fields.append(word_block)
            word_block = ''
        else:
            word_block += word
            
        # add remaining word_block
        if word_block != '' and index==field_len-1:
            splited_fields.append(word_block)

    for key in splited_fields:
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



def filter_dict_recursive(origin_dict, fields_dict):
    result = {}
    for key, value in fields_dict.iteritems():

        if origin_dict.get(key) is None:
            continue

        # exp: roles{id,name} -> key: `roles`, value: `{id,name}`
        if type(value) is dict and len(value) > 0:
            if type(origin_dict[key]) is dict:
                result[key] = filter_dict_recursive(origin_dict[key], value)
            elif type(origin_dict[key]) is list:
                result[key] = [filter_dict_recursive(k, value) for k in origin_dict[key]]
            else:
                result[key] = origin_dict[key]

        else:
            result[key] = origin_dict[key]

        if value.get('__slice') is not None:
            slice_indexes = map(int, value.get('__slice').split(':'))
            result[key] = result[key][slice(*slice_indexes)]
    return result


def filter_dict(origin_dict, fields=None):
    fields_dict = fields_to_dict(fields)

    return origin_dict.copy() if len(fields_dict) == 0 else \
        filter_dict_recursive(origin_dict, fields_dict)


def filter_list(origin_list, fields=None):
    return origin_list if fields is None else \
        [filter_dict(obj, fields) for obj in origin_list]


class Schema(SchemaOrigin):
    def dump(self, obj, many=None, update_fields=True, fields=None, **kwargs):
        result, errors = super(Schema, self).dump(obj, many, update_fields, **kwargs)
        data = filter_list(result, fields) if many is True else filter_dict(result, fields)
        return MarshalResult(data, errors)

    def dumps(self, obj, many=None, update_fields=True, fields=None, *args, **kwargs):
        result, errors = self.dump(obj, many, update_fields, fields)
        data = self.opts.json_module.dumps(result, *args, **kwargs)
        return MarshalResult(data, errors)
