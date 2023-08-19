import datetime
import time
import os

from src.processing import Processing

if __name__ == '__main__':
    # RES_PATH = os.environ['RES_PATH']
    RES_PATH = "./"
    t1 = datetime.datetime.now()
    ###############
    """
    算法求解逻辑代码，操作序列result.txt保存到RES_PATH目录下
    """
    pro = Processing()
    result_list = pro.solve()
    with open(os.path.join(RES_PATH, "result.txt"), "w") as f:
        f.writelines("\n".join(result_list))

    ###############
    t2 = datetime.datetime.now()
    elapse_path = os.path.join(RES_PATH, "elapse.txt")
    with open(elapse_path, "w") as f:
        f.write(str((t2 - t1).total_seconds()))