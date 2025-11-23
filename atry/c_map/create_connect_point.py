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
logger=get_module_logger(module_name,config.create_connect_point_logging_level)

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

def removeConnectPointBetweenRoomANDRoom(randomRoom,i,CPs,map_data):
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
    return list(intersection)

def whereISPathPoint(map_data,connectPoint):
    """由于生成的地图特性，只需检查CP的周围4个格子"""
    y,x=connectPoint
    if map_data[y][x-1]==mapDictionary.path:
        return(y,x-1)
    elif map_data[y][x+1]==mapDictionary.path:
        return(y,x+1)
    elif map_data[y-1][x]==mapDictionary.path:
        return(y-1,x)
    elif map_data[y+1][x]==mapDictionary.path:
        return(y+1,x)
    else:
        assert(1/0)


def removeConnectPointBetweenRoomANDPath(randomRoom, PATHs, randomConnectPoint, CPs, map_data):
    # 扩展道路集合，包含连接点周围的路径点
    y, x = randomConnectPoint
    neighbors = [(y - 1, x), (y + 1, x), (y, x - 1), (y, x + 1)]
    for PATH in PATHs:
        # 检查连接点周围的四个方向是否在道路中
        # 如果任意邻居在道路中，说明这个连接点连接该道路
        path_neighbors = PATH & set(neighbors)
        if path_neighbors:
            logger.info(f"找到与room相连的path，通过邻居点 {path_neighbors}")

            # 移除该房间与这条道路的所有连接点
            path_room_connections = set()

            # 找到所有连接这条道路的连接点
            for room_point in CPs[randomRoom]:
                ry, rx = room_point
                room_neighbors = [(ry - 1, rx), (ry + 1, rx), (ry, rx - 1), (ry, rx + 1)]
                if PATH & set(room_neighbors):
                    path_room_connections.add(tuple(room_point))

            # 移除这些连接点
            CPs[randomRoom] = [point for point in CPs[randomRoom]
                               if tuple(point) not in path_room_connections]

            logger.info(f"移除了{path_room_connections}，剩下{randomRoom}:{CPs[randomRoom]}")

            # 在地图上填充这些点
            for point in path_room_connections:
                y, x = point
                map_data[y][x] = mapDictionary.soild

            return list(path_room_connections)

    logger.error("未找到连接的道路")
    return []

def smallChanceOpen(rCP,first=None,second=None,chance=config.smallChanceOpen,except_point=None):
    assert first is not None
    if len(rCP)==1 and except_point:
        return None
    elif len(rCP)==0:
        return None
    time=0
    while random.randint(1,chance)==chance and rCP:
        if time==0 and except_point is not None:
            rCP.remove(except_point)
        rcp=random.choice(rCP)
        first.append(rcp)
        if second is not None:
            second.append(rcp)
        #print(f"{time}:以1/{chance}的概率加入了{rcp}")
        logger.info(f"{time}:以1/{chance}的概率加入了{rcp}")
        rCP.remove(rcp)
        time+=1
    return 1

def removeRemainConnectPoint(map_data, roomSet, CPs,PATHs):
    logger.info(f"去除多余连接点")
    realCPs=[[]for _ in range(len(roomSet))]
    temp = [i for i in range(len(roomSet))]
    #f1=1
    while existsConnectPoint(CPs):
        #if f1%10==0:create_bmp(f"create_corridor_{f1}.bmp", map_data)
        #f1+=1
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

                rCPbrar=removeConnectPointBetweenRoomANDRoom(randomRoom,i,CPs,map_data)
                logger.info(f"cCPbrar{rCPbrar}")
                smallChanceOpen(rCPbrar,first=realCPs[randomRoom],second=realCPs[i],except_point=randomConnectPoint)

                if not CPs[i]:temp.remove(i)
                if not CPs[randomRoom]: temp.remove(randomRoom)
                findi=True

        if not findi:
            logger.info(f"找到对应path")
            realCPs[randomRoom].append(randomConnectPoint)

            rCPbrap=removeConnectPointBetweenRoomANDPath(randomRoom,PATHs,randomConnectPoint,CPs,map_data)
            logger.info(f"cCPbrap{rCPbrap}")
            smallChanceOpen(rCPbrap,first=realCPs[randomRoom], except_point=randomConnectPoint)

            if not CPs[randomRoom]: temp.remove(randomRoom)

    return realCPs




def create_connect_point(map_data,roomSet,PATHs):
    start_time=time.time()

    logger.info(f"正在生成打通房间和道路\n")
    height = len(map_data)
    width = len(map_data[0])
    #找到所有连接点

    CPs=find_connect_point(map_data,roomSet,height,width)
    for i in range(len(roomSet)):
        logger.info(f"\nroom{i}:({roomSet[i].upleft[0]},{roomSet[i].upleft[1]})-({roomSet[i].upleft[0]+roomSet[i].height-1},{roomSet[i].upleft[1]+roomSet[i].width-1})\n\t{CPs[i]}")

    #去除多余连接点

    CPs=removeRemainConnectPoint(map_data,roomSet,CPs,PATHs)
    for i in range(len(roomSet)):
        logger.info(f"\nroom{i}:({roomSet[i].upleft[0]},{roomSet[i].upleft[1]})-({roomSet[i].upleft[0]+roomSet[i].height-1},{roomSet[i].upleft[1]+roomSet[i].width-1})\n\t{CPs[i]}")
    for CP in CPs:
        for cp in CP:
            y,x = cp
            map_data[y][x] = mapDictionary.connect_point

    print(f"create_connect_point total_time:{time.time() - start_time}")
    write_main_important_data(f"create_connect_point total_time:{time.time() - start_time}\n\n")

    return CPs