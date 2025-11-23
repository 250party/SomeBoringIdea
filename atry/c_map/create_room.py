import time

from c_log import *
from dictionary import mapDictionary

import random

from c_json import GlobalConfig
config=GlobalConfig()
config.load_from_file('config.json')
print(f"当前模块: {__name__}, config id: {id(config)}, config.name: {config.name}")

module_name='create_room'
logger=get_module_logger(module_name,config.create_room_logging_level)

class Room():
    def __init__(self,upleft,height,width):
        self.upleft = upleft
        self.height = height
        self.width = width

def edgeCollision(height,width,room):
    #检查生成的房间是否与地图边界相撞
    if not config.test_edgeCollision:
        if room.upleft[0] <= 0 or room.upleft[0] >= height - 1 or room.upleft[1] <= 0 or room.upleft[1] >= width - 1 or room.upleft[0] + room.height - 1 >= height - 1 or room.upleft[1] + room.width - 1 >= width - 1:
            return True
        else:
            return False
    else:
        if room.upleft[0]<=0 or room.upleft[0]>=height-1:
            logger.info(f"edgeCollision:房间的上沿不能是顶端或是底端\n")
            return True
        elif room.upleft[1]<=0 or room.upleft[1]>=width-1:
            logger.info(f"edgeCollision:房间的左沿不能是左端或是右端\n")
            return True
        elif room.upleft[0]+room.height-1>=height-1:
            logger.info(f"edgeCollision:房间的下沿越界\n")
            return True
        elif room.upleft[1]+room.width-1>=width-1:
            logger.info(f"edgeCollision:房间的右沿越界\n")
            return True
        else:
            return False

def roomCollision(roomSet, room):
    """检查生成的房间是否与已存在的房间相撞"""
    if roomSet==[]:
        return False
    if not config.test_roomCollision:
        for i in roomSet:
            #如果room的四边远离i的四边，那么就检测下一个
            if (room.upleft[0]>i.upleft[0]+i.height-1 +1) or (room.upleft[0]+room.height-1<i.upleft[0] -1) or (room.upleft[1]>i.upleft[1]+i.width-1 +1) or (room.upleft[1]+room.width-1<i.upleft[1] -1):
                pass
            #否则认为相撞
            else:
                return True
        return False
    else:
        for i in roomSet:
            #如果room的四边远离i的四边，那么就检测下一个
            if (room.upleft[0]>i.upleft[0]+i.height-1 +1) or (room.upleft[0]+room.height-1<i.upleft[0] -1) or (room.upleft[1]>i.upleft[1]+i.width-1 +1) or (room.upleft[1]+room.width-1<i.upleft[1] -1):
                logger.info(f"roomCollision:i=({i.upleft[0]},{i.upleft[1]}),{i.height},{i.width} room的上边{room.upleft[0]}?{i.upleft[0]+i.height-1 +1}\t下边{room.upleft[0]+room.height-1}?{i.upleft[0] -1}\t左边{room.upleft[1]}?{i.upleft[1]+i.width-1 +1}\t右边{room.upleft[1]+room.width-1}?{i.upleft[1] -1}\n")
                pass
            #否则认为相撞
            else:
                return True
        return False

def cal_tryLimit(height,width):
    """计算生成房间时的最大尝试次数。如果指定的config.tryLimit<=0,则对tryLimit进行计算"""
    if config.tryLimit<=0:
        tryLimit=height*width
        if tryLimit>1000:
            tryLimit=1000
        return tryLimit
    else:
        if config.tryLimit>1000:
            logger.warning(f"tryLimit过大,有{config.tryLimit}\n")
        return config.tryLimit

def cal_roomLimit(height,width):
    """计算生成房间时的最大房间数量。如果指定的config.roomLimit<=0,则对roomLimit进行计算"""
    if config.roomLimit<=0:
        return height*width
    else:
        if config.roomLimit>1000:
            logger.warning(f"roomLimit过大,有{config.roomLimit}\n")
        return config.roomLimit

def cal_roomAtLeast(height,width):
    """计算生成房间时尽可能要生成的房间数量。如果指定的config.roomAtLeast<=0,则对roomAtLeast进行计算"""
    if config.roomAtLeast<=0:
        return 1
    else:
        if config.roomAtLeast>50:
            logger.warning(f"roomAtLeast过大,有{config.roomAtLeast}\n")
        return config.roomAtLeast

def cal_roomMaxHeight(height):
    """计算生成房间时的房间最大高度，至少为2。如果指定的config.roomMaxHeight<=0或者>=地图高度的一半,则对roomMaxHeigh进行计算。"""
    if config.roomMaxHeight<=0 or config.roomMaxHeight>=height//2:
        roomMaxHeight=height//10
        if roomMaxHeight <2:
            roomMaxHeight=2
        return roomMaxHeight
    else:
        return config.roomMaxHeight

def cal_roomMaxWidth(width):
    """计算生成房间时的房间最大宽度，至少为2。如果指定的config.roomMaxWidth<=0或者>=地图宽度的一半,则对roomMaxWidth进行计算。"""
    if config.roomMaxWidth<=0 or config.roomMaxWidth>=width//2:
        roomMaxWidth = width // 10
        if roomMaxWidth < 2:
            roomMaxWidth = 2
        return roomMaxWidth
    else:
        return config.roomMaxWidth

def cal_roomMinHeight(height,roomMaxHeight):
    """计算房间的最小高度，至少为2。如果config.roomMinHeight<=0或者大于最大值，则计算roomMinHeight"""
    if config.roomMinHeight <= 0 or config.roomMinHeight >= roomMaxHeight:
        return 2
    else:
        return config.roomMinHeight

def cal_roomMinWidth(width,roomMaxWidth):
    """计算房间的最小宽度，至少为2。如果config.roomMinWidth<=0或者大于最大值，则计算roomMinWidth"""
    if config.roomMinWidth <= 0 or config.roomMinWidth >= roomMaxWidth:
        return 2
    else:
        return config.roomMinWidth

def create_room(map_data):
    start_time = time.time()

    logger.info(f"正在生成房间\n")
    height=len(map_data)    #包括边墙
    width=len(map_data[0])
    if height<3 or width<3:
        logger.error(f"ERROR:地图太小，有{height-2}格高，{width-2}格宽\n")

    roomSet=[]
    tryTime=0

    tryLimit=cal_tryLimit(height,width)

    roomLimit=cal_roomLimit(height,width)
    roomAtLeast=cal_roomAtLeast(height,width)

    roomMaxHeight=cal_roomMaxHeight(height)
    roomMaxWidth=cal_roomMaxWidth(width)

    roomMinHeight=cal_roomMinHeight(height,roomMaxHeight)
    roomMinWidth=cal_roomMinWidth(width,roomMaxWidth)

    edgeCollisionTime=0
    roomCollisionTime=0
    stop=False

    logger.info(f"生成参数为tryLimit={tryLimit}\troomLimit={roomLimit}\troomAtLimit={roomAtLeast}\n")
    logger.info(f"roomMaxHeight={roomMaxHeight}\troomMaxWidth={roomMaxWidth}\troomMinHeight={roomMinHeight},roomMinWidth={roomMinWidth}\n")
    while True:
        #生成房间，每生成一个就检测是否碰撞，并且赋值
        tryTime+=1

        logger.info(f"第{tryTime}次尝试生成房间\n")
        if config.create_corridor1_condition:
            dup=0
            while dup%2!=1:
                dup=random.randint(mapDictionary.hwall,height-1-mapDictionary.hwall)    #在左下角生成1格高的房间是不允许的
            dleft=0
            while dleft%2!=1:
                dleft=random.randint(mapDictionary.dwall,width-1-mapDictionary.dwall)
            rupleft=(dup,dleft)
            rheight=0
            while rheight%2!=1:
                rheight=random.randint(roomMinHeight,roomMaxHeight)                     #生成1格高的房间是不允许的
            rwidth=0
            while rwidth%2!=1:
                rwidth=random.randint(roomMinWidth,roomMaxWidth)
        else:
            dup = random.randint(mapDictionary.hwall, height - 1 - mapDictionary.hwall)  # 在左下角生成1格高的房间是不允许的
            dleft = random.randint(mapDictionary.dwall, width - 1 - mapDictionary.dwall)
            rupleft = (dup, dleft)
            rheight = random.randint(roomMinHeight, roomMaxHeight)  # 生成1格高的房间是不允许的
            rwidth = random.randint(roomMinWidth, roomMaxWidth)
        logger.info(f"房间的参数为:上左顶点{rupleft[0],rupleft[1]}，高度{rheight}，宽度{rwidth}\n")
        room=Room(rupleft,rheight,rwidth)

        if edgeCollision(height,width,room):
            logger.warning(f"尝试生成失败，因为边缘越界\n")
            edgeCollisionTime+=1
        elif roomCollision(roomSet,room):
            logger.warning(f"尝试生成失败，因为与现有的房间碰撞\n")
            roomCollisionTime+=1
        else:
            roomSet.append(room)
            #赋值，如果有重叠则停止
            if config.test_pop_roomSet and roomSet:
                i=roomSet.pop()
                logger.info(f"房间({i.upleft[0]},{i.upleft[1]}),{i.height},{i.width}\n")
                for k in range(i.upleft[0], i.upleft[0] + i.height):
                    for j in range(i.upleft[1], i.upleft[1] + i.width):
                        if map_data[k][j] == mapDictionary.air:
                            logger.error(f"发生了({k},{j})重叠\n")
                            stop=True
                        map_data[k][j] = mapDictionary.air
                writeMapDataLog(map_data,module_name,config.create_room_show_map_logging_level)
                roomSet.append(i)
                if stop:
                    logger.info(f"生成了{len(roomSet)}个房间，尝试生成{tryTime}次，发生了edgeCollision{edgeCollisionTime}次，roomCollision{roomCollisionTime}次\n")
                    return map_data,roomSet

        if tryTime>=tryLimit:break
        if len(roomSet)>=roomLimit:break

    if len(roomSet)==0:
        logger.error(f"生成了0个房间")
        return None
    elif len(roomSet)<=roomAtLeast:
        logger.warning(f"生成的房间太少，有{len(roomSet)}个\n")

    if not config.test_pop_roomSet:
        for room in roomSet:
           for i in range(room.upleft[0],room.upleft[0]+room.height ):  #如果你想要融合，你可以+1
                for j in range(room.upleft[1],room.upleft[1]+room.width ):
                    map_data[i][j]=mapDictionary.air
    logger.info(f"生成了{len(roomSet)}个房间，尝试生成{tryTime}次，发生了edgeCollision{edgeCollisionTime}次，roomCollision{roomCollisionTime}次\n")

    write_main_important_data(f"生成了{len(roomSet)}个房间，尝试生成{tryTime}次，发生了edgeCollision{edgeCollisionTime}次，roomCollision{roomCollisionTime}次\n")
    write_main_important_data(f"尝试上限为{tryLimit}，房间上限为{roomLimit}，警告的最小房间数为{roomAtLeast}\n")
    write_main_important_data(f"最大房间高度为{roomMaxHeight}，最大房间宽度为{roomMaxHeight}\n")
    write_main_important_data(f"最小房间高度为{roomMinHeight}，最小房间宽度为{roomMinHeight}\n")

    print(f"create_room total_time:{time.time()-start_time}")
    write_main_important_data(f"create_room total_time:{time.time() - start_time}\n\n")
    return map_data,roomSet

if __name__ == '__main__':
    for i in range(7,11):
        print(i)
        print(edgeCollision(102,102,Room((95,1),i,2)))