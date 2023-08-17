from src.loadport import LoadPort
from src.modules import *


class Robot(object):
    _instance = None

    @staticmethod
    def instance():
        if Robot._instance is None:
            Robot._instance = Robot()
        return Robot._instance

    @staticmethod
    def release():
        Robot._instance = None

    # place策略
    def place_strategy(self, r):
        id = r['wafer_id']
        ix = Wafer_list[id]['index'] + 1
        mdl_list = Path[id%2][ix]
        if LP1 in mdl_list:
            LP = LoadPort.instance().LP_place_strategy()
            LP['unload_type'] = True
            LP['wafer_id_list'].append(id)
        elif PRE in mdl_list:
            if not PRE['use']:
                PRE['use'] = True
                PRE['wafer_id'] = id
                Wafer_list[id]['index'] += 1
            else:
                raise
        elif LLOuter_1 in mdl_list:
            if LP1 in Path[id%2][ix+1]:
                if not LLOuter_2['use'] and len(LLOuter_2['wafer_id_list']) < LLOuter_2['capacity']:
                    LLOuter_2['wafer_id_list'].append(id)
                else:
                    raise
            else:
                if not LLOuter_1['use'] and len(LLOuter_1['wafer_id_list']) < LLOuter_1['capacity']:
                    LLOuter_1['wafer_id_list'].append(id)
                else:
                    raise
        elif PM2 in mdl_list:
            if not PM2['use']:
                PM2['use'] = True
                PM2['wafer_id'] = id
            elif not PM3['use']:
                PM3['use'] = True
                PM3['wafer_id'] = id
            else:
                raise
        elif Multi_PM in mdl_list:
            if len(Multi_PM['wafer_id_list']) < Multi_PM['capacity']:
                Multi_PM['wafer_id_list'].append(id)
                Multi_PM['run_time_list'].append(0)
            else:
                raise
        elif LLInner in mdl_list:
            if len(LLInner['wafer_id_list']) < LLInner['capacity']:
                LLInner['wafer_id_list'].append(id)
                LLInner['run_time_list'].append(0)
            else:
                raise
        elif PM22 in mdl_list:
            if not PM22['use']:
                PM22['use'] = True
                PM22['wafer_id'] = id
            elif not PM21['use']:
                PM21['use'] = True
                PM21['wafer_id'] = id
            else:
                raise
        elif PM23 in mdl_list:
            if not PM23['use']:
                PM23['use'] = True
                PM23['wafer_id'] = id
            elif not PM24['use']:
                PM24['use'] = True
                PM24['wafer_id'] = id
            else:
                raise
        else:
            raise
        Wafer_list[id]['index'] += 1
        r['use'] = False
        r['run_time'] = 0
        r['wafer_id'] = 0

    # 急需pick的策略
    def pick_urgent_strategy(self, r):
        mdl_set = r['modules_list']
        for mdl in mdl_set:
            if mdl['name'] in {'PRE', 'PM2', 'PM3', 'PM4', 'PM21', 'PM22', 'PM23', 'PM24', 'PM25'}:
                if mdl['use'] and mdl['run_time'] - mdl['deal_time'] == mdl['reside']:
                    id = mdl['wafer_id']
                    mdl['use'] = False
                    mdl['run_time'] = 0
                    mdl['wafer_id'] = 0
                    r['use'] = True
                    r['run_time'] = 0
                    r['wafer_id'] = id
                    Wafer_list[id]['pick'] = False
                    return True
            elif mdl['name'] == 'Multi_PM':
                if mdl['wafer_id_list'] and mdl['run_time_list'][0] - mdl['deal_time'] == mdl['reside']:
                    id = mdl['wafer_id_list'][0]
                    mdl['wafer_id_list'].pop(0)
                    mdl['run_time_list'].pop(0)
                    r['use'] = True
                    r['run_time'] = 0
                    r['wafer_id'] = id
                    Wafer_list[id]['pick'] = False
                    return True
            elif mdl['name'] == 'LLInner':
                for i, id in enumerate(mdl['wafer_id_list']):
                    if mdl['run_time_list'][i] - mdl['deal_time'] == mdl['reside']:
                        mdl['wafer_id_list'].pop(i)
                        mdl['run_time_list'].pop(i)
                        r['use'] = True
                        r['run_time'] = 0
                        r['wafer_id'] = id
                        Wafer_list[id]['pick'] = False
                        return True
        return False

    # pick 策略
    def pick_strategy(self, r):
        # 需要先判断下一个模块能不能放
        mdl_list = r['modules_list']
        id_list = []
        for mdl in mdl_list:
            if mdl['name'] in {'PRE', 'PM2', 'PM3', 'PM4', 'PM21', 'PM22', 'PM23', 'PM24', 'PM25'}:
                if mdl['use'] and mdl['run_time'] > mdl['deal_time']:
                    id_list.append(mdl['wafer_id'])
            # elif mdl['name'] in {}
                # if mdl['use'] and mdl['run_time'] - mdl['deal_time'] == mdl['reside']:
        #             id = mdl['wafer_id']
        #             mdl['use'] = False
        #             mdl['run_time'] = 0
        #             mdl['wafer_id'] = 0
        #             r['use'] = True
        #             r['run_time'] = 0
        #             r['wafer_id'] = id
        #             Wafer_list[id]['pick'] = False
        #             return True
        #     elif mdl['name'] == 'Multi_PM':
        #         if mdl['wafer_id_list'] and mdl['run_time_list'][0] - mdl['deal_time'] == mdl['reside']:
        #             id = mdl['wafer_id_list'][0]
        #             mdl['wafer_id_list'].pop(0)
        #             mdl['run_time_list'].pop(0)
        #             r['use'] = True
        #             r['run_time'] = 0
        #             r['wafer_id'] = id
        #             Wafer_list[id]['pick'] = False
        #             return True
        #     elif mdl['name'] == 'LLInner':
        #         for i, id in enumerate(mdl['wafer_id_list']):
        #             if mdl['run_time_list'][i] - mdl['deal_time'] == mdl['reside']:
        #                 mdl['wafer_id_list'].pop(i)
        #                 mdl['run_time_list'].pop(i)
        #                 r['use'] = True
        #                 r['run_time'] = 0
        #                 r['wafer_id'] = id
        #                 Wafer_list[id]['pick'] = False
        #                 return True
        # return False

    #
    def robot_strategy(self, r):
        if r[0]['use'] and r[1]['use']:
            if r[0]['run_time'] > r[1]['run_time']:
                self.place_strategy(r[0])
            else:
                self.place_strategy(r[1])
        else:
            if r[0]['use'] and r[0]['run_time'] - r[0]['deal_time'] == r[0]['reside']:
                self.place_strategy(r[0])
            elif r[1]['use'] and r[1]['run_time'] - r[1]['deal_time'] == r[1]['reside']:
                self.place_strategy(r[1])
            else:
                if not r[0]['use']:
                    pick = self.pick_urgent_strategy(r[0])
                else:
                    pick = self.pick_urgent_strategy(r[1])
                if not pick:
                    if r[0]['use']:
                        self.place_strategy(r[0])
                    elif r[1]['use']:
                        self.place_strategy(r[1])
                    else:
                        self.pick_strategy(r[0])


if __name__ == "__main__":
    Robot.instance().ATR_strategy()