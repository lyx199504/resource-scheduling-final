#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.modules import *

class Processing(object):
    def __init__(self):
        pass

    def pick_strategy(self):
        wafer_id_list = range(1, 1001, 2) if Wafer_num > 500 else range(2, 1001, 2)
        for i in wafer_id_list:
            print(Wafer_list[i])
            wafer = Wafer_list[i]
            if wafer['done'] or wafer['index'] == wafer['length'] - 1:
                continue

            print(Wafer_list[i])
            exit()

    def solve(self):
        self.pick_strategy()


if __name__ == "__main__":
    pro = Processing()
    pro.solve()
