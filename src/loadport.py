
from src.modules import *

class LoadPort(object):
    _instance = None

    @staticmethod
    def instance():
        if LoadPort._instance is None:
            LoadPort._instance = LoadPort()
        return LoadPort._instance

    @staticmethod
    def release():
        LoadPort._instance = None

    # 判断LP是否可装载
    def judge_LP_load(self, LP):
        if not LP['wafer_id_list']:
            return True
        return False

    # LP装载
    def LP_load(self, LP):
        wafer_id_list = list(range(1, 1001, 2)) + list(range(2, 1001, 2))
        LP['load_use'] = True
        for i in wafer_id_list:
            if Wafer_list[i]['index'] == -1 and len(LP['wafer_id_list']) < LP['capacity']:
                LP['wafer_id_list'].append(i)
                Wafer_list[i]['index'] = 0
                Wafer_list[i]['use'] = True
        print("[%s] [%s] [Load]" % (Real_time.strftime(Time_format), LP['name']))

    # 装载策略，两个装载，一个卸载，只要至少有两个空就装载
    def LP_load_strategy(self):
        count = 0
        if self.judge_LP_load(LP1):
            count += 1
        if self.judge_LP_load(LP2):
            count += 1
            if count > 1:
                self.LP_load(LP2)
        if self.judge_LP_load(LP3):
            count += 1
            if count > 1:
                self.LP_load(LP3)

    # 判断LP是否可卸载
    def judge_LP_unload(self, LP):
        if LP['unload_type'] and LP['capacity'] == len(LP['wafer_id_list']):
            return True
        return False

    # LP卸载
    def LP_unload(self, LP):
        LP['unload_use'] = True
        for i in LP['wafer_id_list']:
            Wafer_list[i]['use'] = True
        print("[%s] [%s] [Unload]" % (Real_time.strftime(Time_format), LP['name']))

    # 卸载策略，有加工完且满了就卸载
    def LP_unload_strategy(self):
        if self.judge_LP_unload(LP1):
            self.LP_unload(LP1)
        if self.judge_LP_unload(LP2):
            self.LP_unload(LP2)
        if self.judge_LP_unload(LP3):
            self.LP_unload(LP3)
