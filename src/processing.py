#!/usr/bin/env python
# -*- coding: utf-8 -*-
import time

from src.loadport import LoadPort
from src.modules import *
from src.update import UpdateModules


class Processing(object):
    def __init__(self):
        self.time_format = "%Y/%m/%d %H:%M:%S"
        self.real_time = datetime.datetime.now()

    # 判断PRE是否在使用
    def judge_PRE_run(self):
        if PRE['use']:
            return True
        return False

    # 执行PRE
    def PRE_run(self, id):
        PRE['use'] = True
        PRE['wafer_id'] = id

    def pick_strategy(self):
        wafer_id_list = range(1, 1001, 2) if Wafer_num > 500 else range(2, 1001, 2)
        for i in wafer_id_list:
            print(Wafer_list[i])
            wafer = Wafer_list[i]
            if wafer['index'] >= wafer['length'] - 1:
                continue

            print(Wafer_list[i])
            exit()

    def solve(self):
        while Wafer_num:
            # 先更新所有模块的运行时间等的数据
            UpdateModules.instance().update()

            # 装载
            LoadPort.instance().LP_load_strategy()
            # 卸载
            LoadPort.instance().LP_unload_strategy()

            # ATR



            # print(LP1)
            # print(LP2)
            # print(LP3)

            # time.sleep(1)


            self.real_time += datetime.timedelta(seconds=1)




if __name__ == "__main__":
    pro = Processing()
    pro.solve()
