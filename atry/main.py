from c_log import write_main_important_data
from c_map import create_map
import c_log
from c_bmp import create_bmp
from dictionary import mapDictionary
import time

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')    #由于工作路径原因，运行main时，尽管也有如下语句，而且前面的导入模块意味着那些模块里的语句先执行，但是他只会读取项目下的json文件
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='main'
logger=c_log.get_module_logger(module_name,config.create_main_logging_level)

c_log.start_main_important_data()

import sys
sys.setrecursionlimit(5000)  # 将递归深度限制提高到5000

if __name__ == "__main__":
    start_time = time.time()

    map_data=create_map(config.mapHeight+mapDictionary.hwall+mapDictionary.hwall,config.mapWidth+mapDictionary.dwall+mapDictionary.dwall)
    if map_data is None:
        print("create map failed")
    else:
        print("create map success")
        if create_bmp("1.bmp",map_data):
            pass
        else:
            print("create bmp failed")

    end_time = time.time()
    totalTime = end_time - start_time
    print(f"运行{__name__}的总时间是{totalTime}s")
    c_log.write_main_important_data(f"运行{__name__}的总时间是{totalTime}s\n")


