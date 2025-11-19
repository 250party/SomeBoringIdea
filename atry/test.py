import random
from typing import List, Tuple, Optional
from test1 import *
# 方向常量
UP = 1
RIGHT = 2
DOWN = 3
LEFT = 4

# 状态常量
YES = 1
NO = 0
TRUE = 1
FALSE = 0
OVERFLOW = -1

MAXSTEP = 10
MINSTEP = 3


class Stack:
    def __init__(self):
        self.stack = []

    def push(self, item):
        self.stack.append(item)

    def pop(self):
        if self.stack:
            return self.stack.pop()
        return None

    def length(self):
        return len(self.stack)

    def __getitem__(self, index):
        return self.stack[index]


def mapWillHitWall(x: int, y: int, map_data: List[List[int]], row: int, col: int, direction: int) -> int:
    if direction == UP:
        return YES if y - 1 <= 0 else NO
    elif direction == RIGHT:
        return YES if x + 1 >= col + 1 else NO
    elif direction == DOWN:
        return YES if y + 1 >= row + 1 else NO
    elif direction == LEFT:
        return YES if x - 1 <= 0 else NO
    return NO


def mapWillHitRoad(x: int, y: int, map_data: List[List[int]], row: int, col: int, direction: int) -> int:
    if direction == UP:
        if (map_data[y - 2][x] == 0 or map_data[y - 1][x - 1] == 0 or map_data[y - 1][x + 1] == 0):
            return YES
    elif direction == RIGHT:
        if (map_data[y][x + 2] == 0 or map_data[y - 1][x + 1] == 0 or map_data[y + 1][x + 1] == 0):
            return YES
    elif direction == DOWN:
        if (map_data[y + 2][x] == 0 or map_data[y + 1][x + 1] == 0 or map_data[y + 1][x - 1] == 0):
            return YES
    elif direction == LEFT:
        if (map_data[y][x - 2] == 0 or map_data[y + 1][x - 1] == 0 or map_data[y - 1][x - 1] == 0):
            return YES
    return NO


def mapCanMove(x: int, y: int, map_data: List[List[int]], row: int, col: int) -> int:
    bup, bright, bdown, bleft = 0, 0, 0, 0

    if y - 1 <= 0 or map_data[y - 1][x] == 0 or map_data[y - 2][x] == 0:
        bup = 1
    if x + 1 >= col + 1 or map_data[y][x + 1] == 0 or map_data[y][x + 2] == 0:
        bright = 1
    if y + 1 >= row + 1 or map_data[y + 1][x] == 0 or map_data[y + 2][x] == 0:
        bdown = 1
    if x - 1 <= 0 or map_data[y][x - 1] == 0 or map_data[y][x - 2] == 0:
        bleft = 1

    if map_data[y - 1][x + 1] == 0:
        bup = bright = 1
    if map_data[y + 1][x + 1] == 0:
        bdown = bright = 1
    if map_data[y + 1][x - 1] == 0:
        bdown = bleft = 1
    if map_data[y - 1][x - 1] == 0:
        bup = bleft = 1

    if bup == 1 and bright == 1 and bdown == 1 and bleft == 1:
        return NO
    else:
        return YES


def mapBannedDirection(x: int, y: int, map_data: List[List[int]], row: int, col: int) -> Tuple[List[int], int]:
    dir_list = [-1] * 5

    if y - 1 <= 0 or map_data[y - 1][x] == 0 or map_data[y - 2][x] == 0:
        dir_list[UP] = 1
    if x + 1 >= col + 1 or map_data[y][x + 1] == 0 or map_data[y][x + 2] == 0:
        dir_list[RIGHT] = 2
    if y + 1 >= row + 1 or map_data[y + 1][x] == 0 or map_data[y + 2][x] == 0:
        dir_list[DOWN] = 3
    if x - 1 <= 0 or map_data[y][x - 1] == 0 or map_data[y][x - 2] == 0:
        dir_list[LEFT] = 4

    if map_data[y - 1][x + 1] == 0:
        dir_list[UP] = 1
        dir_list[RIGHT] = 2
    if map_data[y + 1][x + 1] == 0:
        dir_list[DOWN] = 3
        dir_list[RIGHT] = 2
    if map_data[y + 1][x - 1] == 0:
        dir_list[DOWN] = 3
        dir_list[LEFT] = 4
    if map_data[y - 1][x - 1] == 0:
        dir_list[UP] = 1
        dir_list[LEFT] = 4

    return dir_list, TRUE


def _isin(elem: int, swh: List[int], n: int) -> int:
    for i in range(n):
        if elem == swh[i]:
            return YES
    return NO


def printMap(map_data: List[List[int]], row: int, col: int):
    for i in range(row + 2):
        for j in range(col + 2):
            if map_data[i][j] == 1:
                print("■ ", end="")
            elif map_data[i][j] == 0:
                print("  ", end="")
        print()


#def writeLog(msg: str):
    # 在Python中，你可以选择打印日志或使用logging模块
 #   print(msg)


#def writeLogMap(data, size, desc: str):
 #   print(f"{desc}: {data}")


def rand(min_val: int, max_val: int) -> int:
    return random.randint(min_val, max_val)


def mapCreateA(row: int, col: int) -> Tuple[Optional[List[List[int]]], Stack]:
    # 初始化全部不可通行的地图
    map_data = [[1 for _ in range(col + 2)] for _ in range(row + 2)]

    # 设置起始点，地图的中间
    ix = col // 2
    iy = row // 2
    map_data[iy][ix] = 0

    # 将起始点设为房间
    room = Stack()
    room.push((iy, ix))

    # 拐点集
    S = Stack()
    S.push((iy, ix))
    writeLog(f"({iy},{ix})写入拐点集")

    # 构造通道
    allstep = 1
    retrytime = 0

    while True:
        while S.length() != 0:
            # 获取出发点
            turndot = S.pop()
            if turndot is None:
                break

            y, x = turndot
            iy, ix = y, x
            writeLog(f"({iy},{ix})从拐点集取出")

            direction_ = 0
            direction = 0

            while mapCanMove(x, y, map_data, row, col) == YES:
                if direction_ != 0 and direction != direction_:
                    room.push((y, x))
                    writeLog(f"({y},{x})写入拐点集")

                direction_ = direction

                retrydir = 0
                bdir, _ = mapBannedDirection(x, y, map_data, row, col)
                writeLogMap(bdir, 5, "禁止")

                writeLog(f"direction的重选结果为：{direction} ")
                while _isin(direction, bdir, 5) == YES or direction == 0:
                    direction = rand(1, 4)
                    writeLog(f"{direction} ")
                    retrydir += 1
                    if retrydir == 4:
                        writeLog("\ngoto end\n")
                        break

                writeLog("\n")

                direction_str = ""
                if direction == UP:
                    direction_str = " 上"
                elif direction == RIGHT:
                    direction_str = " 右"
                elif direction == DOWN:
                    direction_str = " 下"
                elif direction == LEFT:
                    direction_str = " 左"

                writeLog(f"方向{direction_str}")

                step = rand(MINSTEP, MAXSTEP)
                writeLog(f"距离{step}")

                while step > 0:
                    if mapWillHitWall(x, y, map_data, row, col, direction) == YES:
                        writeLog(f"当前位置({y},{x}),预计撞墙")
                        break

                    if mapWillHitRoad(x, y, map_data, row, col, direction) == YES:
                        writeLog(f"当前位置({y},{x}),预计撞路")
                        break

                    if direction == UP:
                        y -= 1
                    elif direction == RIGHT:
                        x += 1
                    elif direction == DOWN:
                        y += 1
                    elif direction == LEFT:
                        x -= 1

                    map_data[y][x] = 0
                    step -= 1
                    allstep += 1

                S.push((y, x))
                writeLog(f"({y},{x})写入拐点集")
                writeLog(f"当前位置({y},{x})")
                writeLogMap(map_data, row, col, room)  # 这个函数需要实现

            writeLog(f"当前位置({y},{x})无法移动，退回原点({iy},{ix})")

        writeLog("拐点集已取尽")
        writeLog(f"总步数{allstep}")

        if allstep < (row * col * 0.16) and retrytime < 4:
            writeLog(f"总步数小于{min(row, col) * 4},重新启动次数{retrytime}小于4，重新启动")
            for i in range(room.length()):
                turndot = room.stack[i]
                writeLog(f"将拐点集({turndot[0]},{turndot[1]}),放入栈内")
                S.push(turndot)
            retrytime += 1
            writeLog("goto restart")
            continue
        break

    return map_data, room


def mapCreateM(mapA: List[List[int]], row: int, col: int):
    # 这个函数在C代码中为空，这里也保持简单实现
    return None


# 使用示例
if __name__ == "__main__":
    openLog()
    row, col = 20, 20
    map_data, room = mapCreateA(row, col)
    if map_data:
        printMap(map_data, row, col)