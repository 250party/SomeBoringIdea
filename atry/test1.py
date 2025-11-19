import os
from typing import List, Optional, Union


# 假设Stack类已经定义，这里简单定义一下
class Stack:
    def __init__(self):
        self.stack = []
        self.length = 0

    def push(self, item):
        self.stack.append(item)
        self.length += 1

    def __getitem__(self, index):
        return self.stack[index]


def openLog() -> bool:
    """创建日志文件"""
    path = "./1.log"
    try:
        with open(path, 'w', encoding='utf-8') as out_file:
            pass  # 只是创建文件，不写入内容
        return True
    except Exception as e:
        print(f"Cannot Open File: {path}, error: {e}")
        return False


def writeLog(word: str) -> bool:
    """写入普通日志"""
    path = "./1.log"
    try:
        with open(path, 'a', encoding='utf-8') as out_file:
            out_file.write(word)
        return True
    except Exception as e:
        print(f"Cannot Open File: {path}, error: {e}")
        return False


def writeLogMap(map_data: Union[List[List[int]], List[int]],
                row: Optional[int] = None,
                col: Optional[int] = None,
                room: Optional[Stack] = None,
                word: Optional[str] = None) -> bool:
    """
    写入地图日志
    支持两种重载：
    1. 二维地图 + 房间信息
    2. 一维方向数组 + 描述文字
    """
    path = "./1.log"

    try:
        with open(path, 'a', encoding='utf-8') as out_file:
            # 判断是哪种重载形式
            if isinstance(map_data, list) and len(map_data) > 0:
                if isinstance(map_data[0], list):  # 二维数组 - 地图
                    # 写入二维地图
                    for i in range(row + 2):
                        out_file.write(f"{i}\t")
                        for j in range(col + 2):
                            if map_data[i][j] == 1:
                                out_file.write("■ ")
                            elif map_data[i][j] == 0:
                                out_file.write("  ")
                        out_file.write("\n")

                    # 写入房间信息
                    if room and hasattr(room, 'stack'):
                        for i in range(1, room.length):
                            item = room[i]
                            if isinstance(item, tuple) and len(item) == 2:
                                y, x = item
                                out_file.write(f'({y},{x}) ')
                        out_file.write("\n\n")

                else:  # 一维数组 - 方向信息
                    # 写入描述文字
                    if word:
                        out_file.write(word)
                    # 写入方向数组
                    for i in range(len(map_data)):
                        out_file.write(f"{map_data[i]} ")
                    out_file.write("\n")

        return True
    except Exception as e:
        print(f"Cannot Open File: {path}, error: {e}")
        return False


# 使用示例
if __name__ == "__main__":
    # 初始化日志文件
    openLog()

    # 写入普通日志
    writeLog("开始生成地图...\n")

    # 创建测试数据
    test_map = [
        [1, 1, 1, 1, 1],
        [1, 0, 0, 0, 1],
        [1, 0, 1, 0, 1],
        [1, 0, 0, 0, 1],
        [1, 1, 1, 1, 1]
    ]

    test_room = Stack()
    test_room.push((1, 1))
    test_room.push((2, 2))
    test_room.push((3, 3))

    # 写入地图日志
    writeLogMap(test_map, row=3, col=3, room=test_room)

    # 写入方向数组日志
    test_directions = [1, 2, 3, 4, -1]
    writeLogMap(test_directions, word="禁止方向: ")

    writeLog("地图生成完成\n")