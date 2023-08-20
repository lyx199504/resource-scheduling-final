#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import json

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
        pick_LP_again = True
        pick_LP_time = self.real_time

        result_list = []

        if os.path.exists(Interval_time_path):
            with open(Interval_time_path, "r") as f:
                INTERVAL['list'] = json.load(f)
        else:
            INTERVAL['list'] = [Interval_time] * 500
        INTERVAL['ix'] = 0

        while self.wafer_num:
            # 先更新所有模块的运行时间等的数据
            UpdateModules.instance().update(self.real_time, result_list)

            # 装载
            LoadPort.instance().LP_load_strategy(self.real_time, result_list)

            # 每组两个晶圆，间隔取下一组
            if (self.real_time - pick_LP_time).seconds >= INTERVAL['list'][INTERVAL['ix']]:
                if INTERVAL['ix'] < 500 - 1:
                    INTERVAL['ix'] += 1
                pick_LP = True
                pick_LP_again = True

            # 机械臂策略
            pick_LP_done = Robot.instance().robot_strategy(pick_LP, self.real_time, result_list)
            if pick_LP_done:
                pick_LP = False
                if pick_LP_again:
                    pick_LP = True
                    pick_LP_again = False
                    pick_LP_time = self.real_time

            # 卸载
            unload = LoadPort.instance().LP_unload_strategy(self.real_time, result_list)
            if unload:
                self.wafer_num -= 25

            self.real_time += datetime.timedelta(seconds=1)

        return result_list


if __name__ == "__main__":
    pro = Processing()
    pro.solve()
