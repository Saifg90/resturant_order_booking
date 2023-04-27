import os
import redis
import json


class RedisStorage:
    _obj = None

    def __init__(self):
        self.url = os.environ.get('REDIS_HOST', '127.0.0.1')
        self.port = os.environ.get('REDIS_PORT', '6379')
        self.db = os.environ.get('REDIS_DB', '1')
        self.expire = os.environ.get('REDIS_EXPIRE', '43200')
        self.connection = None

    @classmethod
    def factory(cls):
        if not cls._obj:
            cls._obj = cls()
            cls._obj.connect()
        return cls._obj
    
    def connect(self):
        self.connection = redis.Redis(
            host=self.url, port=self.port, db=self.db)

    def set_key(self, key, value):
        value = str(value)
        self.connection.lpush(key, value)
        self.connection.expire(key, self.expire)

    def get_key(self, key):
        json_data = self.connection.lrange(key, 0, -1)
        prompt = []
        for data in json_data:
            try:
                json_data = json.loads(data.decode("utf-8"))
                prompt.append(json_data)
            except (json.JSONDecodeError, TypeError):
                print(f"Invalid JSON string: {data.decode('utf-8')}")
        return prompt

    def get_key_callsid(self, key):
        json_data = self.connection.lrange(key, 0, -1)
        # print(json_data[0].decode('utf-8')[2:-1])
        # print(json_data[0].decode('utf-8')[:])
        return str(json_data[0].decode('utf-8')[:])
    
    def remove_key(self, key):
        self.connection.delete(key)