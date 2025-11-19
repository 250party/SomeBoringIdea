import json
from typing import Any, Dict

class GlobalConfig:
    _instance = None
    _config_data: Dict[str, Any] = {}

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def load_from_file(self, filepath: str):
        """从JSON文件加载配置"""
        with open(filepath, 'r', encoding='utf-8') as f:
            self._config_data = json.load(f)

    def update(self, new_config: Dict[str, Any]):
        """更新配置"""
        self._config_data.update(new_config)

    def get(self, key: str, default: Any = None) -> Any:
        """获取配置值"""
        keys = key.split('.')
        value = self._config_data

        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        return value

    def __getattr__(self, name: str) -> Any:
        if name in self._config_data:
            return self._config_data[name]
        raise AttributeError(f"配置 '{name}' 不存在")

    def to_dict(self) -> Dict[str, Any]:
        """返回配置字典的副本"""
        return self._config_data.copy()


# 创建全局配置实例
config = GlobalConfig()

# 初始化时加载配置
#config.load_from_file('config.json')

if __name__=='__main__':

    # 初始化配置
    config.load_from_file('config.json')
    #print(type(config))    <class '__main__.GlobalConfig'>
    # 方式1: 属性访问 (通过 __getattr__)
    print(config.app_name)  # "MyApp"
    print(config.debug)  # True

    # 方式2: 字典访问 (通过 __getitem__)
    #print(config['app_name'])  # "MyApp"   x

    # 方式3: get方法访问嵌套配置
    db_host = config.get('database.host')  # "localhost"
    db_user = config.get('database.credentials.username')  # "admin"

    # 方式4: 混合访问
    db_config = config.database
    #print(type(db_config))     <class 'dict'>
    print(db_config['host'])  # "localhost"
    #print(db_config.port)  # 5432

    # 带默认值的访问
    timeout = config.get('timeout', 30)  # 返回30，因为timeout不存在

    # 获取整个配置字典
    full_config = config.to_dict()