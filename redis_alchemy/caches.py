from __future__ import unicode_literals, absolute_import, print_function

__author__ = 'danishabdullah'

from redis import StrictRedis


KEY = [
    "DEL",
    "DUMP",
    "EXISTS",
    "EXPIRE",
    "EXPIREAT",
    "MIGRATE",
    "MOVE",
    "PERSIST",
    "PEXPIRE",
    "PEXPIREAT",
    "PTTL",
    "RENAME",
    "RENAMENX",
    "RESTORE",
    "SORT",
    "TTL",
    "TYPE"
]

HASHMAP = [
    "HDEL",
    "HEXISTS",
    "HGET",
    "HGETALL",
    "HINCRBY",
    "HINCRBYFLOAT",
    "HKEYS",
    "HLEN",
    "HMGET",
    "HMSET",
    "HSET",
    "HSETNX",
    "HSTRLEN",
    "HVALS",
    "HSCAN"
]

LIST = [
    "BLPOP",
    "BRPOP",
    "BRPOPLPUSH",
    "LINDEX",
    "LINSERT",
    "LLEN",
    "LPOP",
    "LPUSH",
    "LPUSHX",
    "LRANGE",
    "LREM",
    "LSET",
    "LTRIM",
    "RPOP",
    "RPOPLPUSH",
    "RPUSH",
    "RPUSHX"
]

SET = [
    "SADD",
    "SCARD",
    "SDIFF",
    "SDIFFSTORE",
    "SINTER",
    "SINTERSTORE",
    "SISMEMBER",
    "SMEMBERS",
    "SMOVE",
    "SPOP",
    "SRANDMEMBER",
    "SREM",
    "SUNION",
    "SUNIONSTORE",
    "SSCAN"
]

NAMESPACED_COMMANDS = KEY + HASHMAP + LIST + SET


class NameSpacedRedis(StrictRedis):
    def __init__(self, namespace, host='127.0.0.1', port=6379, password=None,
                 delimiter='.', **kwargs):
        self.namespace = namespace
        self.host = host
        self.port = port
        self._password = password
        self.namespace = namespace
        self.delimiter = delimiter

        super(NameSpacedRedis, self).__init__(host=host,
                                              port=port,
                                              password=password,
                                              **kwargs)



