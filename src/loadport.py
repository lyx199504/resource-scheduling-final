
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
        if not LP['load_use'] and not LP['wafer_id_list']:
            return True
        return False

    # LP装载
    def LP_load(self, LP, real_time, result_list):
        wafer_id_list = list(range(1, 1001, 2)) + list(range(2, 1001, 2))
        for i in wafer_id_list:
            if Wafer_list[i]['index'] == -1 and len(LP['wafer_id_list']) < LP['capacity']:
                LP['wafer_id_list'].append(i)
                Wafer_list[i]['index'] = 0
        LP['load_use'] = True
        if LP['wafer_id_list']:
            result_list.append("[%s] [%s] [Load]" % (real_time.strftime(Time_format), LP['name']))

    # 装载策略，两个装载，一个卸载，只要至少有两个空就装载
    def LP_load_strategy(self, real_time, result_list):
        count = 0
        if self.judge_LP_load(LP1):
            count += 1
        if self.judge_LP_load(LP2):
            count += 1
            if count > 1:
                self.LP_load(LP2, real_time, result_list)
        if self.judge_LP_load(LP3):
            count += 1
            if count > 1:
                self.LP_load(LP3, real_time, result_list)

    # 判断LP是否可卸载
    def judge_LP_unload(self, LP):
        if LP['unload_type'] and not LP['unload_use'] and LP['capacity'] == len(LP['wafer_id_list']):
            return True
        return False

    # LP卸载
    def LP_unload(self, LP, real_time, result_list):
        LP['unload_use'] = True
        result_list.append("[%s] [%s] [Unload]" % (real_time.strftime(Time_format), LP['name']))
        return True

    # 卸载策略，有加工完且满了就卸载
    def LP_unload_strategy(self, real_time, result_list):
        unload = False
        if self.judge_LP_unload(LP1):
            unload = self.LP_unload(LP1, real_time, result_list)
        if not unload:
            if self.judge_LP_unload(LP2):
                unload = self.LP_unload(LP2, real_time, result_list)
        if not unload:
            if self.judge_LP_unload(LP3):
                unload = self.LP_unload(LP3, real_time, result_list)
        return unload

    # pick策略
    def LP_pick_strategy(self):
        odd = False
        if not LP1['unload_type'] and LP1['wafer_id_list'] and LP1['wafer_id_list'][0]%2 == 1:
            odd = True
        if not odd:
            if not LP2['unload_type'] and LP2['wafer_id_list'] and LP2['wafer_id_list'][0]%2 == 1:
                odd = True
        if not odd:
            if not LP3['unload_type'] and LP3['wafer_id_list'] and LP3['wafer_id_list'][0]%2 == 1:
                odd = True
        LP = None
        if odd:
            if not LP1['unload_type'] and not LP1['load_use'] and LP1['wafer_id_list']:
                if LP1['wafer_id_list'][0]%2 == 1:
                    LP = LP1
            if not LP2['unload_type'] and not LP2['load_use'] and LP2['wafer_id_list']:
                if LP2['wafer_id_list'][0]%2 == 1:
                    if LP is None or LP['wafer_id_list'][0] > LP2['wafer_id_list'][0]:
                        LP = LP2
            if not LP3['unload_type'] and not LP3['load_use'] and LP3['wafer_id_list']:
                if LP3['wafer_id_list'][0]%2 == 1:
                    if LP is None or LP['wafer_id_list'][0] > LP3['wafer_id_list'][0]:
                        LP = LP3
        else:
            if not LP1['unload_type'] and not LP1['load_use'] and LP1['wafer_id_list']:
                LP = LP1
            if not LP2['unload_type'] and not LP2['load_use'] and LP2['wafer_id_list']:
                if LP is None or LP['wafer_id_list'][0] > LP2['wafer_id_list'][0]:
                    LP = LP2
            if not LP3['unload_type'] and not LP3['load_use'] and LP3['wafer_id_list']:
                if LP is None or LP['wafer_id_list'][0] > LP3['wafer_id_list'][0]:
                    LP = LP3
        return LP

    def judge_LP_place_one(self, LP):
        if LP['unload_type'] and len(LP['wafer_id_list']) < LP['capacity']:
            return True
        if not LP['wafer_id_list']:
            return True
        return False

    # 判断可否place
    def judge_LP_place(self):
        place = self.judge_LP_place_one(LP1)
        if not place:
            place = self.judge_LP_place_one(LP2)
        if not place:
            place = self.judge_LP_place_one(LP3)
        return place

    # 判断是否可place
    def LP_place_strategy(self):
        if LP1['unload_type'] and LP1['wafer_id_list'] and len(LP1['wafer_id_list']) < LP1['capacity']:
            return LP1
        if LP2['unload_type'] and LP2['wafer_id_list'] and len(LP2['wafer_id_list']) < LP2['capacity']:
            return LP2
        if LP3['unload_type'] and LP3['wafer_id_list'] and len(LP3['wafer_id_list']) < LP3['capacity']:
            return LP3
        if not LP1['wafer_id_list']:
            return LP1
        if not LP2['wafer_id_list']:
            return LP2
        if not LP3['wafer_id_list']:
            return LP3
        raise
