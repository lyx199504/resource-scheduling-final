#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

from src.modules import *
from src.loadport import LoadPort
from src.robot import Robot
from src.update import UpdateModules


class Processing(object):
    def __init__(self):
        self.real_time = datetime.datetime.now()
        self.wafer_num = 1000

    def solve(self):
        pick_LP = True
        pick_LP_time = self.real_time

        odd_pick = True

        while self.wafer_num:
            # 先更新所有模块的运行时间等的数据
            UpdateModules.instance().update()

            # 装载
            LoadPort.instance().LP_load_strategy(self.real_time)
            # 卸载
            LoadPort.instance().LP_unload_strategy(self.real_time)

            if self.wafer_num > 500:
                if (self.real_time - pick_LP_time).seconds >= 30:
                    pick_LP = True
                    odd_pick = True
                # 机械臂
                pick_LP_done = Robot.instance().robot_strategy(pick_LP, self.real_time, self.wafer_num)
                if pick_LP_done:
                    self.wafer_num -= 1
                    pick_LP = False
                    if odd_pick:
                        pick_LP_time = self.real_time
                        pick_LP = True
                        odd_pick = False
            else:
                if (self.real_time - pick_LP_time).seconds >= 60:
                    pick_LP = True
                pick_LP_done = Robot.instance().robot_strategy(pick_LP, self.real_time, self.wafer_num)
                if pick_LP_done:
                    pick_LP_time = self.real_time

            self.real_time += datetime.timedelta(seconds=1)




if __name__ == "__main__":
    pro = Processing()
    pro.solve()
