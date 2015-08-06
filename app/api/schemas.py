from marshmallow import Schema as SchemaOrigin


def fields_to_dict(fields):
    result = {}

    if not fields or len(fields.strip()) == 0:
        return result

    for key in fields.split(','):
        key = key.strip()
        result[key] = {}

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
