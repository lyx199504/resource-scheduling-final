
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


    # 更新各模块数据
    def update(self):
        # 更新LP
        self.update_LP(LP1)
        self.update_LP(LP2)
        self.update_LP(LP3)
