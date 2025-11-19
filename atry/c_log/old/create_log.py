import os
import time

def dir_filepath():
    # 确保文件创建在模块所在目录
    module_dir = os.path.dirname(os.path.abspath(__file__))
    return module_dir
#指向要创建的文件位置
def dir_filename(test,filepath,filename,testfile):
    if test == False:
        if not os.path.exists('atryLog'):
            os.makedirs('atryLog')
        path='atrylog//'+filename
    else:
        filepath=dir_filepath()
        if not os.path.exists(filepath+'\\'+testfile):
            os.makedirs(filepath+'\\'+testfile)
        path = os.path.join(filepath, testfile+'\\' + filename)
    return path

def openLog(test=False,testfile='test_log'):
    logname='1.log'
    logname=dir_filename(test,'',logname,testfile)
    try:
        with open(logname,'w',encoding='utf8')as f:
            pass
        return True
    except Exception as e:
        print(f"Cannot Open Log File: {logname}, error: {e}")
        return False

def writeLog(word,test=False,testfile='test_log'):
    logname = '1.log'
    logname = dir_filename(test, '', logname, testfile)
    try:
        with open(logname, 'a', encoding='utf-8') as out_file:
            out_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}:\n")
            out_file.write(f"{word}")
        return True
    except Exception as e:
        print(f"Cannot Open File: {logname}, error: {e}")
        return False

def writeMapDataLog(map,test=False,testfile='test_log'):
    logname = '1.log'
    logname = dir_filename(test, '', logname, testfile)
    try:
        with open(logname, 'a', encoding='utf-8') as out_file:
            out_file.write(f"{time.strftime('%Y-%m-%d %H:%M:%S', time.localtime())}:\n")
            from dictionary import mapDictionary
            for i in range (len(map)):
                out_file.write(f"{i}\t")
                for j in range (len(map[i])):
                    if map[i][j] ==mapDictionary.soild:
                        if i==0 or i==len(map)-1 or j==0 or j==len(map[i])-1:
                            out_file.write('% ')
                        else:
                            out_file.write('■ ')
                    elif map[i][j] ==mapDictionary.air:
                        out_file.write('  ')
                out_file.write('\n')
            out_file.write('\n')
        return True
    except Exception as e:
        print(f"Cannot Open File: {logname}, error: {e}")
        return False

if __name__ == "__main__":
    openLog(test=True)
    writeLog('你有病',test=True)