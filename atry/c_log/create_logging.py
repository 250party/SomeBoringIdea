# log_utils.py
import logging
import os
from logging.handlers import RotatingFileHandler
import glob

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

class LogManager:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(LogManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if not self._initialized:
            self.log_dir = 'logs'
            os.makedirs(self.log_dir, exist_ok=True)
            self._initialized = True

    def _cleanup_old_logs(self, module_name):
        """清理指定模块的旧日志文件"""
        try:
            # 匹配模块相关的所有日志文件（包括轮转文件）
            pattern = os.path.join(self.log_dir, f'{module_name}*.log*')
            old_logs = glob.glob(pattern)

            for log_file in old_logs:
                try:
                    os.remove(log_file)
                    print(f"已删除旧日志文件: {log_file}")
                except Exception as e:
                    print(f"删除日志文件失败 {log_file}: {e}")
        except Exception as e:
            print(f"清理旧日志时出错: {e}")

    def get_logger(self, module_name, level=logging.INFO,cleanup_old=True):
        """为不同模块获取独立的logger，level是过滤器"""
        logger = logging.getLogger(module_name)

        # 如果logger已经有handler，直接返回（避免重复添加）
        if logger.handlers:
            return logger

        if cleanup_old:
           self._cleanup_old_logs(module_name)

        logger.setLevel(level)

        # 创建模块特定的日志文件
        log_file = os.path.join(self.log_dir, f'{module_name}.log')

        # 文件handler - 按模块分开
        file_handler = RotatingFileHandler(
            log_file,
            maxBytes=10 * 1024 * 1024,  # 5MB
            backupCount=3,
            encoding='utf-8'
        )

        # 控制台handler - 可选，用于开发时查看
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.ERROR)  # 控制台只显示警告及以上

        # 设置日志格式
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - [%(filename)s:%(lineno)d] - %(message)s'
        )
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # 添加handler
        logger.addHandler(file_handler)
        logger.addHandler(console_handler)

        # 防止日志传递给根logger（避免重复）
        logger.propagate = False

        return logger


# 创建全局日志管理器实例
log_manager = LogManager()


# 便捷函数
def get_module_logger(module_name,level):
    """获取模块logger的便捷函数"""
    if level=='DEBUG':
        level=logging.DEBUG
    elif level=='INFO':
        level=logging.INFO
    elif level=='WARNING':
        level=logging.WARNING
    elif level=='ERROR':
        level=logging.ERROR
    elif level=='CRITICAL':
        level=logging.CRITICAL
    else:
        level=logging.DEBUG
    return log_manager.get_logger(module_name,level)

def writeMapDataLog(map,module_name,level='DEBUG'):
    """自动过滤debug级别"""
    logger=get_module_logger(module_name,'INFO')
    from dictionary import mapDictionary
    map1=[]
    for i in range(len(map)):
        row= [str(i) + '\t']
        for j in range(len(map[i])):
            if map[i][j] == mapDictionary.soild:
                if i == 0 or i == len(map) - 1 or j == 0 or j == len(map[i]) - 1:
                    row.append('% ')
                else:
                    row.append('■ ')
            elif map[i][j] == mapDictionary.air:
                row.append('  ')
        map1.append(row)
    map2='\n'.join(''.join(row) for row in map1)
    if level=='DEBUG':
        logger.debug(f'\n {map2}')
    if level=='INFO':
        logger.info(f'\n {map2}')



if __name__ == '__main__':
    logger=get_module_logger(__name__)
    logger.debug('debug')
    logger.info('info')
    logger.warning('warning')
    logger.error('error')