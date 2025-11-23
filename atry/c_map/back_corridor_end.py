import time

from c_log import *
from dictionary import mapDictionary
from c_bmp import create_bmp

import random

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='back_corridor_end'
logger=get_module_logger(module_name,config.create_corridor_logging_level)


def isVisited(visited, y, x):
    return visited[y][x]


def isVaild(y, x, height, width, visited, map_data):
    if (mapDictionary.dwall <= x <= width - mapDictionary.dwall - 1 and
            mapDictionary.hwall <= y <= height - mapDictionary.hwall - 1):
        if not isVisited(visited, y, x) and map_data[y][x] == mapDictionary.path:
            return True
    return False

def neighborIsCP(map_data,dot):
    y,x=dot
    if map_data[y-1][x] == mapDictionary.connect_point or map_data[y][x+1] == mapDictionary.connect_point or map_data[y+1][x] == mapDictionary.connect_point or map_data[y][x-1] == mapDictionary.connect_point:
        return True
    return False

def isDotAlive(dot,alive):
    y,x=dot
    dir=[0,1,0,-1,0]
    for i in range(4):
        if (y+dir[i+1],x+dir[i]) in alive:
            return True
    return False

def dfs(map_data,y,x,visited,DEAD_PATHs):
    height=len(map_data)
    width=len(map_data[0])
    logger.info(f"dfs从({y},{x})开始")
    dead = []
    stack=[(y,x)]
    dir=[0,1,0,-1,0]

    alive=[(y,x)]

    visited[y][x]=True
    while stack:
        #logger.info(f"{stack}")
        (y,x)=stack[-1]     #如果是x,y会有环，和各种独立布局,如果这么改了，要修改path
        logger.info(f"现在是({y},{x})")
        havepush=False
        for i in range(4):  #下，右，上，左
            j=i
            nx=x+dir[j]
            ny=y+dir[j+1]
            if isVaild(ny,nx,height,width,visited,map_data):
                havepush=True
                visited[ny][nx]=True
                if False:
                    logger.info(f"neighborIsCP:点{(ny,nx)}是活的")
                    alive.append((ny,nx))
                stack.append((ny,nx))
                break
        if not havepush:
            dot=stack.pop()
            if neighborIsCP(map_data,dot) or isDotAlive(dot,alive):
                logger.info(f"isDotAlive:点{dot}是活的")
                alive.append(dot)
                if dead:
                    DEAD_PATHs.append(dead)
                    dead=[]
            else:
                logger.info(f"isDotAlive:发现死路上的点{dot}")
                dead.append(dot)

    return visited,DEAD_PATHs


def back_corridor_end(map_data,CPs):
    start_time = time.time()

    logger.info(f"正在去除死路")
    height = len(map_data)
    width = len(map_data[0])

    visited = [[False for _ in range(width)] for _ in range(height)]
    DEAD_PATHs=[]
    for CP in CPs:
        for cp in CP:
            y,x=cp
            visited,DEAD_PATHs = dfs(map_data, y,x,visited,DEAD_PATHs)

    for i in range(len(DEAD_PATHs)):
        logger.info(f"\n{i}:{DEAD_PATHs[i]}")

    for dead in DEAD_PATHs:
        for dot in dead:
            y,x=dot
            map_data[y][x] = mapDictionary.soild



    print(f"back_corridor_end total_time:{time.time() - start_time}")
    write_main_important_data(f"back_corridor_end total_time:{time.time() - start_time}\n")