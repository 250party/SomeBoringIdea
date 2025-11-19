from c_log import *
from dictionary import mapDictionary
from c_map.create_room import create_room

module_name='create_map'
logger=get_module_logger(module_name)

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

def create_map(height,width):
    logger.info(f"初始化地图\t地图有{height - 2}格高，{width - 2}格宽\n")
    map_data=[]
    for i in range(height):
        row=[]
        for j in range(width):
            row.append(mapDictionary.soild)
        map_data.append(row)

    logger.info(f'初始化的地图如下\n')
    writeMapDataLog(map_data,module_name,'INFO')

    map_data,roomSet=create_room(map_data,tryLimit=1000,roomLimit=1000)
    if map_data is None:
        return None
    if config.test_show_RoomSet:
        logger.info(f"房间集合为")
        for room in roomSet:
            logger.info(f"{room.upleft},({room.upleft[0]+room.height-1},{room.upleft[1]+room.width-1})\t\th: {room.height}  w: {room.width}")
    logger.info(f'生成的房间如下\n')
    writeMapDataLog(map_data,module_name,'INFO')
    logger.info(f'生成房间完毕\n')
    all=0
    allair=0
    for i in range(1,len(map_data)-1):
        for j in range(1,len(map_data[0])-1):
            all+=1
            if map_data[i][j]==mapDictionary.air:
                allair+=1
    logger.info(f"生成了{len(roomSet)}个房间，总共{all}个方格,覆盖了{allair}个方格，覆盖率为{allair/all}")
    return map_data


if __name__=='__main__':
    create_map(100+mapDictionary.hwall+mapDictionary.hwall,100+mapDictionary.dwall+mapDictionary.dwall)