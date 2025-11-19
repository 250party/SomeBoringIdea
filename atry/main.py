from c_map import create_map
import c_log
from c_bmp import create_bmp
from dictionary import mapDictionary
import time

module_name='main'
logger=c_log.get_module_logger(module_name)

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')    #由于工作路径原因，运行main时，尽管也有如下语句，而且前面的导入模块意味着那些模块里的语句先执行，但是他只会读取项目下的json文件
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")


if __name__ == "__main__":
    start_time = time.time()

    map_data=create_map(50+mapDictionary.hwall+mapDictionary.hwall,50+mapDictionary.dwall+mapDictionary.dwall)
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

