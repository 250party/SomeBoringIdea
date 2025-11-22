import time
from collections import deque

from c_log import *
from dictionary import mapDictionary
from dictionary import directionDictionary as dd

import random

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='create_corridor'
logger=get_module_logger(module_name,config.create_room_logging_level)

def isPath(map_data,y,x):
    """对下一个路径y,x，是否就是道路"""
    if map_data[y][x]==mapDictionary.path:
        return True
    else:
        return False

def isEdge(y,x,height,width):
    """地图边界"""
    if x==mapDictionary.dwall-1 or x==width-mapDictionary.dwall or y==mapDictionary.hwall-1 or y==height-mapDictionary.hwall:
        #logger.info(f"{y},{x}是边界")
        return True
    else:
        #logger.info(f"{y},{x}不是边界")
        return False

def canNotStartHere(map_data, y, x):
    """能够开始的条件是四周八格都为实心墙"""
    if map_data[y][x]==mapDictionary.soild and map_data[y][x-1]==mapDictionary.soild and map_data[y][x+1]==mapDictionary.soild and map_data[y-1][x]==mapDictionary.soild and map_data[y+1][x]==mapDictionary.soild and map_data[y-1][x-1]==mapDictionary.soild and map_data[y-1][x+1]==mapDictionary.soild and map_data[y+1][x-1]==mapDictionary.soild and map_data[y+1][x+1]==mapDictionary.soild:
        logger.info(f"({y},{x})能作为起点")
        return False
    else:
        logger.info(f"({y},{x})不能作为起点\n")
        return True

def CanBeCorridor(map_data,y,x,height,width):
    """对于下一个(y,x),可以作为路径吗，可以成为的条件是周围都不是房间/air"""
    if isEdge(y,x,height,width):
        logger.info(f"({y},{x})不能作为下一个路径，因为是wall")
        return False
    sum=0
    if map_data[y][x-1]==mapDictionary.air:
        sum+=1
    if map_data[y][x+1]==mapDictionary.air:
        sum += 1
    if map_data[y-1][x]==mapDictionary.air:
        sum += 1
    if map_data[y+1][x]==mapDictionary.air:
        sum += 1
    if map_data[y-1][x-1]==mapDictionary.air:
        sum += 1
    if map_data[y-1][x+1]==mapDictionary.air:
        sum += 1
    if map_data[y+1][x-1]==mapDictionary.air:
        sum += 1
    if map_data[y+1][x+1]==mapDictionary.air:
        sum += 1
    if sum==0:
        logger.info(f"({y},{x})能作为下一个路径/起点？")
        return True
    else:
        logger.info(f"({y},{x})不能作为下一个路径，因为会和已有的房间重叠,sum={sum}")
        return False

def gene_directionSet(number=4)->deque[int]:
    """生成一个directionSet，储存顺序1234"""
    assert(1<=number<=4)
    directionSet = deque()
    start = random.randint(1, 4)
    current = start
    for i in range(number):
        directionSet.append(current)
        current = current % 4 + 1  # 循环到下一个数，4后面是1
    return directionSet

def directionBlocks(map_data,y,x,direction,height,width):
    """对下一个路径y,x，是否有道路在行进方向两侧/周围五格"""
    if direction==dd.right or direction==dd.left:
        #如果两侧有道路阻挡
        if map_data[y+1][x]==mapDictionary.path or map_data[y-1][x]==mapDictionary.path:
            return True
        #如果要和道路连接,或者斜角将有道路
        if direction==dd.right and not isEdge(y,x,height,width) and (map_data[y][x+1]==mapDictionary.path or map_data[y-1][x+1]==mapDictionary.path or map_data[y+1][x+1]==mapDictionary.path):
            return True
        elif direction==dd.left and not isEdge(y,x,height,width) and (map_data[y][x-1]==mapDictionary.path or map_data[y-1][x-1]==mapDictionary.path or map_data[y+1][x-1]==mapDictionary.path):
            return True

    elif direction==dd.down or direction==dd.up:
        # 如果两侧有道路阻挡
        if map_data[y][x+1]==mapDictionary.path or map_data[y][x-1]==mapDictionary.path:
            return True
        # 如果要和道路连接
        if direction==dd.down and not isEdge(y,x,height,width) and (map_data[y+1][x]==mapDictionary.path or map_data[y+1][x-1]==mapDictionary.path or map_data[y+1][x+1]==mapDictionary.path):
            return True
        elif direction==dd.up and not isEdge(y,x,height,width) and (map_data[y-1][x]==mapDictionary.path or map_data[y-1][x-1]==mapDictionary.path or map_data[y-1][x+1]==mapDictionary.path):
            return True
    return False

def goNext(map_data,y,x,height,width):
    """终止条件是：不可以成为走廊。否则成为走廊"""
    if not CanBeCorridor(map_data,y,x,height,width) :
        return False
    else:
        map_data[y][x]=mapDictionary.path
        logger.info(f"({y},{x})成为路径")

        directionSet=gene_directionSet(number=config.try_directionLimit)

        while directionSet:
            direction=directionSet.popleft()

            if direction==dd.right:                            #右
                logger.info(f"({y},{x})向右走")
                if not isPath(map_data,y,x+1) and not directionBlocks(map_data,y,x+1,direction,height,width):
                    goNext(map_data,y,x+1,height,width)
                else:
                    logger.info(f"不能向右走，因为前方已经是路")

            elif direction==dd.down:                          #下
                logger.info(f"({y},{x})向下走")
                if not isPath(map_data,y+1,x) and not directionBlocks(map_data,y+1,x,direction,height,width):
                    goNext(map_data,y+1,x,height,width)
                else:
                    logger.info(f"不能向下走，因为前方已经是路")

            elif direction==dd.left:                          #左
                logger.info(f"({y},{x})向左走")
                if not isPath(map_data,y,x-1) and not directionBlocks(map_data,y,x-1,direction,height,width):
                    goNext(map_data,y,x-1,height,width)
                else:
                    logger.info(f"不能向左走，因为前方已经是路")

            elif direction==dd.up:                          #上
                logger.info(f"({y},{x})向上走")
                if not isPath(map_data,y-1,x) and not directionBlocks(map_data,y-1,x,direction,height,width):
                    goNext(map_data,y-1,x,height,width)
                else:
                    logger.info(f"不能向上走，因为前方已经是路")

        return True


def create_corridor(map_data):
    start_time = time.time()

    logger.info(f"正在生成道路")
    height=len(map_data)
    width=len(map_data[0])

    for y in range(mapDictionary.hwall,height-mapDictionary.hwall):
        for x in range(mapDictionary.dwall,width-mapDictionary.dwall):
            if canNotStartHere(map_data,y,x):
                pass
            else:
                map_data[y][x] = mapDictionary.path
                logger.info(f"({y},{x})成为路径")
                #深度遍历，但是随机方向
                goNext(map_data,y,x,height,width)
                logger.info(f"\n")
    print(f"create_corridor total_time:{time.time() - start_time}")
    write_main_important_data(f"create_corridor total_time:{time.time() - start_time}\n")



if __name__=='__main__':
    pass