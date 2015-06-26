from __future__ import unicode_literals, absolute_import, print_function

__author__ = 'danishabdullah'

from .utils import prepend_prefix
import ujson
from collections import MutableSet, MutableMapping
from datetime import datetime

try:
    string_types = basestring
except NameError:  # Python 3 compat
    string_types = str


class RedisSetContainer(MutableSet):
    def __init__(self, redis, key, values):
        """
        :param redis: NameSpacedRedis
        :param key: unicode
        :param namespace: unicode
        :param delimiter: unicode
        :param cooloff: int
        :return:
        """
        self.redis = redis
        self.store = values if values else set()
        self.key = key
        self._dirty = False
        self._last_load_time = None

    def load_remote(self):
        self.store = self.redis.smembers(self.key)
        self._dirty = False
        return datetime.now()

    def __iter__(self):
        return iter(self.store)

    def __contains__(self, item):
        return item in self.store

    def __len__(self):
        return len(self.store)

    def add(self, array):
        if not type(array) == list:
            array = [array]
        res = self.redis.sadd(self.key, *array)
        map(self.store.add, array)
        self._dirty = True
        return res

    def discard(self, array):
        if not type(array) == list:
            array = [array]
        self.redis.spop(self.key, *array)
        map(self.store.discard, array)

    def __str__(self):
        return self.store.__str__()

    def __unicode__(self):
        return unicode(self.__str__())

    def __repr__(self):
        return self.__str__()


class RedisHashContainer(MutableMapping):
    def __init__(self, redis, key, values, serialize=False, serializer='json'):
        """
        :param redis: NameSpacedRedis
        :param key: unicode
        :param namespace: unicode
        :param delimiter: unicode
        :param cooloff: int
        :return:
        """
        assert serializer in ('json', None)
        self.redis = redis
        self.store = values if values else dict()
        self.key = key
        self.serialize = serialize
        self.serializer = serializer
        self._last_load_time = None
        self._dirty = False

    def load_remote(self):
        res = self.redis.hgetall(self.key)
        if self.serialize and self.serializer:
            for k, v in res.iteritems():
                res[k] = ujson.loads(v)
        self.store = res
        self._dirty = False
        return datetime.now()

    def __getitem__(self, item):
        return self.store[item]

    def __setitem__(self, field, value):
        if value:
            if self.serialize and self.serializer:
                value = ujson.dumps(value)
        res = self.redis.hset(self.key, field, value)
        self.store[field] = value
        self._dirty = True
        return res

    def __delitem__(self, fields):
        if not isinstance(fields, list):
            fields = [fields]
        res = self.redis.hdel(self.key, *fields)
        [self.store.pop(item, None) for item in fields]
        self._dirty = True
        return res

    def __iter__(self):
        return iter(self.store)

    def __contains__(self, item):
        return item in self.store

    def __len__(self):
        return len(self.store)

    def __str__(self):
        return self.store.__str__()

    def __unicode__(self):
        return unicode(self.__str__())

    def __repr__(self):
        return self.__str__()


class RSet(object):
    def __init__(self, redis, key, namespace=None, delimiter='.',
                 cooloff=30 * 1000):
        """
        :param redis: NameSpacedRedis
        :param key: unicode
        :param namespace: unicode
        :param delimiter: unicode
        :param cooloff: int
        :return:
        """
        self.redis = redis
        self._last_load_time = None
        self.cooloff = cooloff
        self.key = prepend_prefix(key, namespace or redis.namespace,
                                  delimiter or redis.delimiter)
        self.store = RedisSetContainer(self.redis, self.key, None)

    def load_remote(self):
        self._last_load_time = self.store.load_remote()

    def __get__(self, instance, owner):
        if (not self._last_load_time
            or (datetime.now() - self._last_load_time).microseconds / 1000 > self.cooloff
            or self.store._dirty):
            self.load_remote()
        return self.store

    def __set__(self, instance, array):
        assert isinstance(array, list)
        self.__del__()
        res = self.redis.sadd(self.key, *array)
        self.load_remote()
        return res

    def __del__(self):
        res = self.redis.delete(self.key)
        self.store.store = None
        self.store._dirty = True
        return res


class RString(object):
    def __init__(self, redis, key, namespace=None, delimiter='.'):
        """
        :param redis: NameSpacedRedis
        :param key: unicode
        :param namespace: unicode
        :param delimiter: unicode
        :return:
        """
        self.redis = redis
        self.key = prepend_prefix(key, namespace or redis.namespace,
                                  delimiter or redis.delimiter)

    def __get__(self, instance, owner):
        return self.redis.get(self.key)

    def __set__(self, instance, string):
        assert isinstance(string, string_types)
        self.__del__()
        return self.redis.set(self.key, string)

    def __del__(self):
        self.redis.delete(self.key)


class RHash(object):
    def __init__(self, redis, key, namespace=None, delimiter='.',
                 serializer=None, serialize=False, cooloff=30 * 1000):
        """
        :param redis: NameSpacedRedis
        :param key: unicode
        :param namespace: unicode
        :param delimiter: unicode
        :param serializer: unicode
        :param serialize: bool
        :return:
        """
        assert serializer in (None, 'json')
        self.redis = redis
        self.serializer = serializer
        self.serialize = serialize
        self._last_load_time = None
        self.key = prepend_prefix(key, namespace or redis.namespace,
                                  delimiter or redis.delimiter)
        self.cooloff = cooloff
        self.store = RedisHashContainer(self.redis, self.key, None,
                                        serialize=serialize,
                                        serializer=serializer)

    def load_remote(self):
        self._last_load_time = self.store.load_remote()

    def __get__(self, instance, owner):
        if (not self._last_load_time
            or (datetime.now() - self._last_load_time).microseconds / 1000 > self.cooloff
            or self.store._dirty):
            self.load_remote()
        return self.store

    def __set__(self, instance, hash):
        assert isinstance(hash, dict)
        self.__del__()
        if self.serializer and self.serialize:
            for k, v in hash.iteritems():
                hash[k] = ujson.dumps(v, ensure_ascii=False)
        res = self.redis.hmset(self.key, hash)
        self.store._dirty = True
        return res

    def __del__(self):
        res = self.redis.delete(self.key)
        self.store.store = None
        self.store._dirty = True
        return res

