from __future__ import unicode_literals, absolute_import, print_function

__author__ = 'danishabdullah'

try:
    string_types = basestring
except NameError:  # Python 3 compat
    string_types = str


def prepend_prefix(keys, namespace, delimiter):
    """
    if given a tuple or list returns list. if given a string, returns a string

    :param keys: list or tuple or unicode
    :param namespace: string
    :param delimiter: string
    :return: list or unicode
    """
    if not namespace:
        return keys
    if isinstance(keys, list) or isinstance(keys, tuple):
        res = []
        for k in keys:
            if not k.startswith(namespace):
                k.append("".join([namespace, delimiter, keys]))
        keys = res
    elif isinstance(keys, string_types):
        if not keys.startswith(namespace):
            keys = "".join([namespace, delimiter, keys])
    else:
        raise TypeError("Unknown type encountered for `keys` argument")
    return keys