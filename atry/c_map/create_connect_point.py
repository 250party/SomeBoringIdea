import time

from c_bmp import create_bmp
from c_log import *
from dictionary import mapDictionary

import random

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='create_connect_point'
logger=get_module_logger(module_name,config.create_room_logging_level)

def isEdge(y,x,height,width):
    if x==mapDictionary.dwall-1 or x==width-mapDictionary.dwall or y==mapDictionary.hwall-1 or y==height-mapDictionary.hwall:
        #logger.info(f"{y},{x}是边界")
        return True
    else:
        #logger.info(f"{y},{x}不是边界")
        return False

def isAroundRoom(room,y,x):
    """y,x紧贴着room吗"""
    if y == room.upleft[0] - 1 or y == room.upleft[0] + room.height or x == room.upleft[1] - 1 or x == room.upleft[1] + room.width:
        return True
    else:
        return False

def canBeConnectPoint(map_data,y,x):
    """可以是连接点的条件是，有y,x的横轴或者纵轴存在一侧是房间，另一侧是房间或者走廊"""
    #纵轴
    if map_data[y-1][x]==mapDictionary.air and map_data[y+1][x]==mapDictionary.air:
        return True
    elif map_data[y-1][x]==mapDictionary.air and map_data[y+1][x]==mapDictionary.path:
        return True
    elif map_data[y-1][x]==mapDictionary.path and map_data[y+1][x]==mapDictionary.air:
        return True
    #横轴
    elif map_data[y][x-1]==mapDictionary.air and map_data[y][x+1]==mapDictionary.air:
        return True
    elif map_data[y][x-1]==mapDictionary.air and map_data[y][x+1]==mapDictionary.path:
        return True
    elif map_data[y][x-1]==mapDictionary.path and map_data[y][x+1]==mapDictionary.air:
        return True
    return False

def find_connect_point(map_data,roomSet,height,width):
    """找到所有连接点"""
    logger.info(f"找到所有连接点\n")
    CPs=[]
    for room in roomSet:
        CP=[]
        for i in range(room.upleft[0]-1,room.upleft[0]+room.height+1):
            for j in range(room.upleft[1]-1,room.upleft[1]+room.width+1):
                if isAroundRoom(room,i,j) and not isEdge(i,j,height,width) and canBeConnectPoint(map_data,i,j):
                    if map_data[i][j]==mapDictionary.soild:
                        map_data[i][j]=mapDictionary.connect_point
                        CP.append( (i,j) )
                    elif map_data[i][j]==mapDictionary.connect_point:
                        CP.append( (i,j) )
                    else:
                        pass
        CPs.append(CP)
    return CPs


def existsConnectPoint(CPs):
    """如果连接点集中还存在连接点"""
    for CP in CPs:
        if CP:
            return True
    return False

def removeConnectPointBetween(randomRoom,i,CPs,map_data):
    """移除两个区域的连接点,不保留randomConnectPoint"""
    i=i
    set_i = set(tuple(point) for point in CPs[i])
    set_j = set(tuple(point) for point in CPs[randomRoom])

    # 计算交集
    intersection = set_i & set_j

    # 从两个点集中移除交集点
    CPs[i] = [point for point in CPs[i] if tuple(point) not in intersection]
    CPs[randomRoom] = [point for point in CPs[randomRoom] if tuple(point) not in intersection]
    logger.info(f"\n移除了{intersection}\n剩下{randomRoom}:{CPs[randomRoom]}\n{i}:{CPs[i]}")
    # 在map_data上将交集点设为0
    for point in intersection:
        y, x = point
        map_data[y][x] = mapDictionary.soild

def removeRemainConnectPoint(map_data, roomSet, CPs):
    logger.info(f"去除多余连接点")
    realCPs=[[]for _ in range(len(roomSet))]
    temp = [i for i in range(len(roomSet))]
    f1=1
    while existsConnectPoint(CPs):
        if f1%10==0:create_bmp(f"create_corridor_{f1}.bmp", map_data)
        f1+=1
        logger.info(f"还存在连接点")
        #int
        logger.info(f"\n可选择房间集合{temp}")
        randomRoom = random.choice(temp)
        logger.info(f"\n选择房间{randomRoom}:({roomSet[randomRoom].upleft[0]},{roomSet[randomRoom].upleft[1]})-({roomSet[randomRoom].upleft[0]+roomSet[randomRoom].height-1},{roomSet[randomRoom].upleft[1]+roomSet[randomRoom].width-1})\n\t{CPs[randomRoom]}")
        #元组 in list
        randomConnectPoint = random.choice(CPs[randomRoom])
        logger.info(f"选择点{randomConnectPoint}")

        findi=False
        for i in range(len(roomSet)):
            if randomConnectPoint in CPs[i] and i!=randomRoom:
                logger.info(f"\n找到对应room{i}:({roomSet[i].upleft[0]},{roomSet[i].upleft[1]})-({roomSet[i].upleft[0]+roomSet[i].height-1},{roomSet[i].upleft[1]+roomSet[i].width-1})\n\t{CPs[i]}")
                realCPs[i].append(randomConnectPoint)
                realCPs[randomRoom].append(randomConnectPoint)

                removeConnectPointBetween(randomRoom,i,CPs,map_data)

                if not CPs[i]:temp.remove(i)
                if not CPs[randomRoom]: temp.remove(randomRoom)
                findi=True

        if not findi:
            logger.info(f"找到对应path")
            realCPs[randomRoom].append(randomConnectPoint)
            CPs[randomRoom].remove(randomConnectPoint)
            if not CPs[randomRoom]: temp.remove(randomRoom)

    return realCPs




def create_connect_point(map_data,roomSet):
    start_time=time.time()

    logger.info(f"正在生成打通房间和道路\n")
    height = len(map_data)
    width = len(map_data[0])
    #找到所有连接点

    CPs=find_connect_point(map_data,roomSet,height,width)
    for i in range(len(roomSet)):
        logger.info(f"\nroom{i}:({roomSet[i].upleft[0]},{roomSet[i].upleft[1]})-({roomSet[i].upleft[0]+roomSet[i].height-1},{roomSet[i].upleft[1]+roomSet[i].width-1})\n\t{CPs[i]}")

    #去除多余连接点

    CPs=removeRemainConnectPoint(map_data,roomSet,CPs)
    for i in range(len(roomSet)):
        logger.info(f"\nroom{i}:({roomSet[i].upleft[0]},{roomSet[i].upleft[1]})-({roomSet[i].upleft[0]+roomSet[i].height-1},{roomSet[i].upleft[1]+roomSet[i].width-1})\n\t{CPs[i]}")


    print(f"create_connect_point total_time:{time.time() - start_time}")
    write_main_important_data(f"create_connect_point total_time:{time.time() - start_time}\n")