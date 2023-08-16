import datetime
import time
import os

if __name__ == '__main__':
    # RES_PATH = os.environ['RES_PATH']
    RES_PATH = "./"
    t1 = datetime.datetime.now()
    ###############
    """
    算法求解逻辑代码，操作序列result.txt保存到RES_PATH目录下
    """

    ###############
    t2 = datetime.datetime.now()
    elapse_path = os.path.join(RES_PATH, "elapse.txt")
    with open(elapse_path, "w") as f:
        f.write(str((t2 - t1).total_seconds()))