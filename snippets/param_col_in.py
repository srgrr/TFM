# Parameter conversion dictionary.
_param_conversion_dict_ = {
    'IN': {},
    'OUT': {
        'p_direction': DIRECTION.OUT
    },
    'INOUT': {
        'p_direction': DIRECTION.INOUT
    },
    ...
}

def get_new_parameter(key):
    """
    Returns a brand new parameter (no copies!)
    :param key: A string that is a key of a valid Parameter template
    """
    return Parameter(**_param_conversion_dict_[key])
...
# Aliases for objects (just direction)
IN = _param_('IN')
OUT = _param_('OUT')
INOUT = _param_('INOUT')