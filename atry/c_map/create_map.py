import time

from c_bmp import create_bmp
from c_log import *
from dictionary import mapDictionary

from c_map.create_room import create_room
from c_map.create_corridor import create_corridor
from c_map.create_corridor1 import create_corridor1
from c_map.create_connect_point import create_connect_point
from c_map.back_corridor_end import back_corridor_end

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='create_map'
logger=get_module_logger(module_name,config.create_map_logging_level)

def init_map(height,width):
    logger.info(f"初始化地图\t地图有{height - 2}格高，{width - 2}格宽\n")
    write_main_important_data(f"初始化地图\t地图有{height - 2}格高，{width - 2}格宽\n")
    map_data = []
    for i in range(height):
        row = []
        for j in range(width):
            row.append(mapDictionary.soild)
        map_data.append(row)
    return map_data

def init_map1(height,width):
    logger.info(f"初始化地图\t地图有{height - 2}格高，{width - 2}格宽\n")
    write_main_important_data(f"初始化地图\t地图有{height - 2}格高，{width - 2}格宽\n")
    map_data = [[mapDictionary.soild for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            if i%2==1 and j%2==1 and 0<=i<=height-2 and 0<=j<=width-2:
                map_data[i][j]=mapDictionary.ban
    return map_data

def create_map(height,width):
    start_time = time.time()

    if not config.create_corridor1_condition:
        map_data = init_map(height,width)
    else:
        map_data = init_map1(height,width)
    create_bmp(f"init.bmp", map_data)

    logger.info(f'初始化的地图如下\n')
    writeMapDataLog(map_data,module_name,'INFO')


    map_data,roomSet=create_room(map_data)
    create_bmp(f"create_room.bmp", map_data)

    if map_data is None:
        return None
    if config.test_show_RoomSet:
        logger.info(f"房间集合为")
        for room in roomSet:
            logger.info(f"({room.upleft[0],room.upleft[1]})-({room.upleft[0]+room.height-1},{room.upleft[1]+room.width-1})\t\th: {room.height}  w: {room.width}")

    logger.info(f'生成的房间如下\n')
    writeMapDataLog(map_data,module_name,'INFO')
    logger.info(f'生成房间完毕\n')

    all=0
    allair=0
    for i in range(mapDictionary.hwall,len(map_data)-mapDictionary.hwall):
        for j in range(mapDictionary.dwall,len(map_data[0])-mapDictionary.dwall):
            all+=1
            if map_data[i][j]==mapDictionary.air:   #这是房间
                allair+=1
    logger.info(f"生成了{len(roomSet)}个房间，总共{all}个方格,覆盖了{allair}个方格，剩余{all-allair}个方格，房间覆盖率为{allair/all}")

    write_main_important_data(f"create_room,生成了{len(roomSet)}个房间，总共{all}个方格,覆盖了{allair}个方格，剩余{all-allair}个方格，房间覆盖率为{allair/ all}\n\n")


    if not config.create_corridor1_condition:
        create_corridor(map_data)
    else:
        PATHs=create_corridor1(map_data)
        logger.info("道路")
        path_no=0
        for PATH in PATHs:
            logger.info(f"{path_no}:{PATH}\n")
            path_no += 1
    create_bmp(f"create_corridor.bmp", map_data)


    allpath = 0
    for i in range(mapDictionary.hwall, len(map_data) - mapDictionary.hwall):
        for j in range(mapDictionary.dwall, len(map_data[0]) - mapDictionary.dwall):
            if map_data[i][j] == mapDictionary.path:
                allpath += 1
    logger.info(f"生成道路，总共{len(PATHs)}条路，总共{all}个方格,覆盖了{allpath}个方格，剩余{all-allair-allpath}个方格，路径覆盖率为{allpath / all},总覆盖率{(allair+allpath)/all}\n\n")
    write_main_important_data(f"create_corridor，总共{all}个方格,覆盖了{allpath}个方格，剩余{all-allair-allpath}个方格，路径覆盖率为{allpath / all},总覆盖率{(allair+allpath)/all}\n\n")


    if config.create_corridor1_condition:
        CPs=create_connect_point(map_data,roomSet,PATHs)
        create_bmp(f"create_connect_point.bmp", map_data)


        back_corridor_end(map_data, CPs)
        create_bmp(f"back_corridor_end.bmp", map_data)

        allsoild = 0
        for i in range(mapDictionary.hwall, len(map_data) - mapDictionary.hwall):
            for j in range(mapDictionary.dwall, len(map_data[0]) - mapDictionary.dwall):
                if map_data[i][j] == mapDictionary.soild:
                    allsoild += 1

        write_main_important_data(f"反雕刻，总共{all}个方格,剩余{allsoild}个soild方格，总覆盖率{(all-allsoild)/all}\n\n")

    print(f"create_map total_time:{time.time() - start_time}")
    write_main_important_data(f"create_map total_time:{time.time() - start_time}\n\n")


    return map_data


if __name__=='__main__':
    create_map(config.mapHeight+mapDictionary.hwall+mapDictionary.hwall,config.mapWidth+mapDictionary.dwall+mapDictionary.dwall)