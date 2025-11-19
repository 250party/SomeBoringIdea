import os
from c_log import *
from invaild_filename.invaild import has_invalid_filename_chars
import random

module_name='create_bmp'
logger=get_module_logger(module_name)

#指向该模块目录
def dir_filepath():
    # 确保文件创建在模块所在目录
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return module_dir
#指向要创建的文件位置
def dir_filename(test,filepath,filename,testfile):
    if test == False:
        path=os.path.join(filepath, filename)
    else:
        if not os.path.exists(filepath+'\\'+testfile):
            os.makedirs(filepath+'\\'+testfile)
        path = os.path.join(filepath, testfile+'\\' + filename)
    return path
#初始化bmp
def create_bmp_data(width,height):
    # 计算行字节数（每行必须是4的倍数）
    row_size = (width * 3 + 3) & ~3
    image_size = row_size * height
    file_size = 54 + image_size  # 54 = 文件头+信息头大小

    # BMP文件头 (14字节)
    bmp_header = bytearray(14)
    bmp_header[0:2] = b'BM'  # 签名
    bmp_header[2:6] = file_size.to_bytes(4, 'little')  # 文件大小
    bmp_header[6:8] = b'\x00\x00'  # 保留字段1
    bmp_header[8:10] = b'\x00\x00'  # 保留字段2
    bmp_header[10:14] = (54).to_bytes(4, 'little')  # 数据偏移

    # BMP信息头 (40字节)
    bmp_info_header = bytearray(40)
    bmp_info_header[0:4] = (40).to_bytes(4, 'little')  # 信息头大小
    bmp_info_header[4:8] = width.to_bytes(4, 'little')  # 宽度
    bmp_info_header[8:12] = height.to_bytes(4, 'little')  # 高度
    bmp_info_header[12:14] = (1).to_bytes(2, 'little')  # 平面数
    bmp_info_header[14:16] = (24).to_bytes(2, 'little')  # 每像素位数
    bmp_info_header[16:20] = (0).to_bytes(4, 'little')  # 压缩方式
    bmp_info_header[20:24] = image_size.to_bytes(4, 'little')  # 图像数据大小
    bmp_info_header[24:28] = (0).to_bytes(4, 'little')  # 水平分辨率
    bmp_info_header[28:32] = (0).to_bytes(4, 'little')  # 垂直分辨率
    bmp_info_header[32:36] = (0).to_bytes(4, 'little')  # 使用的颜色数
    bmp_info_header[36:40] = (0).to_bytes(4, 'little')  # 重要颜色数

    # 像素数据
    pixel_data = bytearray(image_size)
    return row_size,pixel_data,bmp_header,bmp_info_header

def create_random_bmp(filename, width, height,test=False,testfile='test_bmp'):
    if has_invalid_filename_chars(filename):
        return None
    #重定向到该文件夹
    filepath=dir_filepath()
    #如果在测试，那就放到测试文件夹
    filename = dir_filename(test, filepath,filename,testfile)
    #初始化bmp
    row_size,pixel_data,bmp_header,bmp_info_header = create_bmp_data(width, height)


    for y in range(height):
        for x in range(width):
            pixel_index = y * row_size + x * 3

            pixel_data[pixel_index] = random.randint(0,255)   # 蓝色
            pixel_data[pixel_index+1] = random.randint(0,255)  # 绿色
            pixel_data[pixel_index+2] = random.randint(0,255)  # 红色


    # 写入文件
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(bmp_info_header)
        f.write(pixel_data)

    print(f"成功创建图片: {filename} ({width}x{height})")
    return True


def create_bmp(filename, map_data, test=False, testfile='test_bmp'):
    if has_invalid_filename_chars(filename):
        return None
    # 重定向到该文件夹
    #filepath = dir_filepath()
    filepath=''
    # 如果在测试，那就放到测试文件夹
    filename = dir_filename(test, filepath, filename, testfile)

    height=len(map_data)
    width =len(map_data[0])

    # 初始化bmp
    row_size, pixel_data, bmp_header, bmp_info_header = create_bmp_data(width, height)

    padding=width%4
    #python对未赋值的数组元素自动填充0000000000
    for y in range(height):
        for x in range(width):
            pixel_index = y * row_size + x * 3
            from dictionary import mapDictionary
            if map_data[y][x] == mapDictionary.soild:
                pixel_data[pixel_index] = 0  # 蓝色
                pixel_data[pixel_index + 1] = 0  # 绿色
                pixel_data[pixel_index + 2] = 0  # 红色
            elif map_data[y][x] == mapDictionary.air:
                pixel_data[pixel_index] = 255  # 蓝色
                pixel_data[pixel_index + 1] = 255  # 绿色
                pixel_data[pixel_index + 2] = 255  # 红色
            else:
                pixel_data[pixel_index] = 127  # 蓝色
                pixel_data[pixel_index + 1] = 127  # 绿色
                pixel_data[pixel_index + 2] = 127  # 红色

    # 写入文件
    with open(filename, 'wb') as f:
        f.write(bmp_header)
        f.write(bmp_info_header)
        f.write(pixel_data)

    print(f"create bmp success: {filename} ({width}x{height})")
    return True
# 使用示例
if __name__=='__main__':
    for i in range(5):
        filename='test'+str(i)+'.bmp'
        create_random_bmp(filename, 200, 100,test=True)