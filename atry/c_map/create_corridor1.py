import time

from c_log import *
from dictionary import mapDictionary
from c_bmp import create_bmp

import random

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='create_corridor1'
logger=get_module_logger(module_name,config.create_corridor_logging_level)

def isVisited(visited,y,x):
    return visited[y][x]

def isVaild(y,x,height,width,visited,map_data):
    if mapDictionary.dwall<=x<=width-mapDictionary.dwall-1 and mapDictionary.hwall<=y<=height-mapDictionary.hwall-1:
        if not isVisited(visited,y,x) and map_data[y][x]!=mapDictionary.air:
            map_data[y][x]=mapDictionary.path
            return True
    return False

def dfs(map_data,y,x,visited,PATH):
    height=len(map_data)
    width=len(map_data[0])

    map_data[y][x]=mapDictionary.path
    PATH.add((y,x))
    stack=[(y,x)]
    dir=[0,1,0,-1,0]

    visited[y][x]=True
    while stack:
        logger.info(f"{stack}")
        (y,x)=stack[-1]     #如果是x,y会有环，和各种独立布局,如果这么改了，要修改path
        havepush=False
        for i in range(4):
            j=random.randint(0,3)
            nx=x+dir[j]*2
            ny=y+dir[j+1]*2
            if isVaild(ny,nx,height,width,visited,map_data):
                havepush=True
                visited[ny][nx]=True
                map_data[y+dir[j+1]][x+dir[j]]=mapDictionary.path
                PATH.add((ny,nx))
                PATH.add((y+dir[j+1],x+dir[j]))
                logger.info(f"({y},{x})-({ny},{nx}):({y+dir[j+1]},{x+dir[j]})打通")
                stack.append((ny,nx))
                break
        if not havepush:
            stack.pop()
    return visited



def create_corridor1(map_data):
    start_time = time.time()

    logger.info(f"正在生成道路")
    height=len(map_data)
    width=len(map_data[0])

    visited = [[False for _ in range(width)] for _ in range(height)]
    PATHs=[]
    for i in range(height):
        for j in range(width):
            if map_data[i][j]==mapDictionary.ban :
                PATH=set()
                visited=dfs(map_data, i, j,visited,PATH)
                PATHs.append(PATH)

    print(f"create_corridor total_time:{time.time() - start_time}")
    write_main_important_data(f"create_corridor1 total_time:{time.time() - start_time}\n\n")

    return PATHs

if __name__ == "__main__":
    height=52
    width=52
    map_data=[[1 for _ in range(width)] for _ in range(height)]
    for i in range(height):
        for j in range(width):
            if i%2==1 and j%2==1 and 0<=i<=height-2 and 0<=j<=width-2:
                map_data[i][j]=0
    #print(map_data)
    create_bmp("init.bmp", map_data)
    create_corridor1(map_data)
    create_bmp("corridor1.bmp", map_data)