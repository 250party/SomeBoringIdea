import json


class Config:
    _instance = None

    def __new__(cls, config_path='config.json'):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.load(config_path)
        return cls._instance

    def load(self, config_path):
        with open(config_path, 'r', encoding='utf-8') as f:
            self._data = json.load(f)

    def get(self, key, default=None):
        return self._data.get(key, default)

    def __getattr__(self, name):
        if name in self._data:
            return self._data[name]
        raise AttributeError(f"配置项 '{name}' 不存在")

    def __getitem__(self, key):
        return self._data[key]


# 创建全局配置实例
config = Config()

if __name__=='__main__':
    config.load('config.json')
    print(config.app_name)
    print(config.database.host)