
from src.modules import *

class UpdateModules(object):
    _instance = None

    @staticmethod
    def instance():
        if UpdateModules._instance is None:
            UpdateModules._instance = UpdateModules()
        return UpdateModules._instance

    @staticmethod
    def release():
        UpdateModules._instance = None

    # 更新LP数据
    def update_LP(self, LP):
        if LP['load_use']:  # 更新装载
            LP['run_time'] += 1
            if LP['run_time'] == LP['load_time']:  # 装载处理完成，恢复数据，
                LP['run_time'] = 0
                LP['load_use'] = False
                for i in LP['wafer_id_list']:
                    Wafer_list[i]['pick'] = True
        if LP['unload_use']:  # 更新卸载
            LP['run_time'] += 1
            if LP['run_time'] == LP['unload_time']:  # 卸载处理完成，卸掉wafer_id，恢复数据
                LP['run_time'] = 0
                LP['unload_use'] = False
                LP['unload_type'] = False
                for i in LP['wafer_id_list']:
                    Wafer_list[i]['index'] += 1
                LP['wafer_id_list'] = []

    def update_PM(self, pm):
        if pm['use']:
            pm['run_time'] += 1

    def updata_Multi_PM(self):
        for i in range(len(Multi_PM['run_time_list'])):
            Multi_PM['run_time_list'][i] += 1

    def updata_LLInner(self):
        for i in range(len(LLInner['run_time_list'])):
            LLInner['run_time_list'][i] += 1

    def update_LLOuter(self, LLOuter, real_time, result_list):
        if LLOuter['use']:
            LLOuter['run_time'] += 1
        if LLOuter['use'] and (LLOuter['out_type'] and LLOuter['run_time'] == LLOuter['out_time']
                               or not LLOuter['out_type'] and LLOuter['run_time'] == LLOuter['in_time']):
            result_list.append("[%s] [%s] [Stop]" % (real_time.strftime(Time_format), LLOuter['name']))
            LLOuter['use'] = False

    def update_robot(self, r):
        for i in range(len(r)):
            if r[i]['use']:
                r[i]['run_time'] += 1
            if r[i]['run_time'] - r[i]['deal_time'] > r[i]['reside']:
                raise

    # 更新各模块数据
    def update(self, real_time, result_list):
        # 更新LP
        self.update_LP(LP1)
        self.update_LP(LP2)
        self.update_LP(LP3)
        self.update_PM(PRE)
        self.update_PM(PM2)
        self.update_PM(PM3)
        self.update_PM(PM4)
        self.update_PM(PM21)
        self.update_PM(PM22)
        self.update_PM(PM23)
        self.update_PM(PM24)
        self.update_PM(PM25)
        self.updata_Multi_PM()
        self.updata_LLInner()
        self.update_LLOuter(LLOuter_1, real_time, result_list)
        self.update_LLOuter(LLOuter_2, real_time, result_list)
        self.update_robot(ATR)
        self.update_robot(VTR_1)
        self.update_robot(VTR_2)
