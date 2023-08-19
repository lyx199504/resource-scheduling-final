from src.llouter import LLOut
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
        LLOuter_start = False
        if LP1 in mdl_list:
            LP = LoadPort.instance().LP_place_strategy()
            LP['unload_type'] = True
            LP['wafer_id_list'].append(id)
            mdl_name = LP['name']
        elif PRE in mdl_list:
            if not PRE['use']:
                PRE['use'] = True
                PRE['wafer_id'] = id
                mdl_name = PRE['name']
            else:
                raise
        elif LLOuter_1 in mdl_list:
            if LP1 in Path[id%2][ix+1]:  # 出
                LLOuter = LLOut.instance().out_place_strategy()
                LLOuter['out_type'] = True
                LLOuter['wafer_id_list'].append(id)
                LLOuter_start = True
                LLOuter['use'] = True
            else:  # 进
                LLOuter = LLOut.instance().in_place_strategy()
                LLOuter['out_type'] = False
                LLOuter['wafer_id_list'].append(id)
                if len(LLOuter['wafer_id_list']) == LLOuter['capacity']:
                    LLOuter_start = True
                    LLOuter['use'] = True
            mdl_name = LLOuter['name']
        elif PM2 in mdl_list:
            if not PM2['use']:
                PM2['use'] = True
                PM2['wafer_id'] = id
                mdl_name = PM2['name']
            elif not PM3['use']:
                PM3['use'] = True
                PM3['wafer_id'] = id
                mdl_name = PM3['name']
            else:
                raise
        elif PM4 in mdl_list:
            if not PM4['use']:
                PM4['use'] = True
                PM4['wafer_id'] = id
                mdl_name = PM4['name']
            else:
                raise
        elif Multi_PM in mdl_list:
            if len(Multi_PM['wafer_id_list']) < Multi_PM['capacity']:
                Multi_PM['wafer_id_list'].append(id)
                Multi_PM['run_time_list'].append(0)
                mdl_name = Multi_PM['name']
            else:
                raise
        elif LLInner in mdl_list:
            if len(LLInner['wafer_id_list']) < LLInner['capacity']:
                LLInner['wafer_id_list'].append(id)
                LLInner['run_time_list'].append(0)
                mdl_name = LLInner['name']
            else:
                raise
        elif PM22 in mdl_list:
            if not PM22['use']:
                PM22['use'] = True
                PM22['wafer_id'] = id
                mdl_name = PM22['name']
            elif not PM21['use']:
                PM21['use'] = True
                PM21['wafer_id'] = id
                mdl_name = PM21['name']
            else:
                raise
        elif PM23 in mdl_list:
            if not PM23['use']:
                PM23['use'] = True
                PM23['wafer_id'] = id
                mdl_name = PM23['name']
            elif not PM24['use']:
                PM24['use'] = True
                PM24['wafer_id'] = id
                mdl_name = PM24['name']
            else:
                raise
        elif PM25 in mdl_list:
            if not PM25['use']:
                PM25['use'] = True
                PM25['wafer_id'] = id
                mdl_name = PM25['name']
            else:
                raise
        else:
            raise
        Wafer_list[id]['index'] += 1
        r['use'] = False
        r['run_time'] = 0
        r['wafer_id'] = 0
        return r['name'], id, mdl_name, LLOuter_start

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
                    return r['name'], id, mdl['name']
            elif mdl['name'] == 'Multi_PM':
                if mdl['wafer_id_list'] and mdl['run_time_list'][0] - mdl['deal_time'] == mdl['reside']:
                    id = mdl['wafer_id_list'][0]
                    mdl['wafer_id_list'].pop(0)
                    mdl['run_time_list'].pop(0)
                    r['use'] = True
                    r['run_time'] = 0
                    r['wafer_id'] = id
                    Wafer_list[id]['pick'] = False
                    return r['name'], id, mdl['name']
            elif mdl['name'] == 'LLInner':
                for i, id in enumerate(mdl['wafer_id_list']):
                    if mdl['run_time_list'][i] - mdl['deal_time'] == mdl['reside']:
                        mdl['wafer_id_list'].pop(i)
                        mdl['run_time_list'].pop(i)
                        r['use'] = True
                        r['run_time'] = 0
                        r['wafer_id'] = id
                        Wafer_list[id]['pick'] = False
                        return r['name'], id, mdl['name']
        return "", 0, ""

    # 紧急操作策略
    def robot_urgent_strategy(self, r, real_time, result_list):
        pick = False
        LLOuter_start = False
        if r[0]['use'] and r[1]['use']:
            if r[0]['run_time'] > r[1]['run_time']:
                r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[0])
            else:
                r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[1])
        else:
            if r[0]['use'] and r[0]['run_time'] - r[0]['deal_time'] == r[0]['reside']:
                r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[0])
            elif r[1]['use'] and r[1]['run_time'] - r[1]['deal_time'] == r[1]['reside']:
                r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[1])
            else:
                if not r[0]['use']:
                    r_name, id, mdl_name = self.pick_urgent_strategy(r[0])
                else:
                    r_name, id, mdl_name = self.pick_urgent_strategy(r[1])
                if mdl_name:
                    pick = True
                else:
                    if r[0]['use']:
                        r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[0])
                    elif r[1]['use']:
                        r_name, id, mdl_name, LLOuter_start = self.place_strategy(r[1])
                    else:
                        mdl_name = ""
        if mdl_name:
            if pick:
                result_list.append("[%s] [%s] [Pick] [Wafer_%d] [%s]" % (real_time.strftime(Time_format), r_name, id, mdl_name))
            else:
                result_list.append("[%s] [%s] [Place] [Wafer_%d] [%s]" % (real_time.strftime(Time_format), r_name, id, mdl_name))
                if LLOuter_start:
                    result_list.append("[%s] [%s] [Start]" % (real_time.strftime(Time_format), mdl_name))
        return mdl_name

    #
    def robot_strategy(self, pick_LP, real_time, result_list):
        # 先紧急pick和紧急place，再非紧急place
        ATR_mdl_name = self.robot_urgent_strategy(ATR, real_time, result_list)
        VTR1_mdl_name = self.robot_urgent_strategy(VTR_1, real_time, result_list)
        VTR2_mdl_name = self.robot_urgent_strategy(VTR_2, real_time, result_list)

        # 检查不同的机械臂是否撞模块，撞了则抛异常，下面pick策略会控制不撞模块
        if ATR_mdl_name and ATR_mdl_name == VTR1_mdl_name or VTR1_mdl_name and VTR1_mdl_name == VTR2_mdl_name \
                or ATR_mdl_name and ATR_mdl_name == VTR2_mdl_name:
            raise

        ATR_output, VTR1_output, VTR2_output = True, True, True
        if ATR_mdl_name:
            ATR_output = False
        if VTR1_mdl_name:
            VTR1_output = False
        if VTR2_mdl_name:
            VTR2_output = False

        # 非紧急pick的策略
        atr, vtr1, vtr2 = None, None, None
        pick_LP_done = False

        # pick LLOuter准备出仓的晶圆
        if not ATR_mdl_name:
            atr = ATR[0] if not ATR[0]['use'] else ATR[1]
            if LLOuter_1['name'] not in [VTR1_mdl_name, VTR2_mdl_name] and LLOut.instance().judge_out_pick(LLOuter_1):
                atr['use'] = True
                atr['wafer_id'] = LLOuter_1['wafer_id_list'][0]
                Wafer_list[atr['wafer_id']]['pick'] = False
                LLOuter_1['wafer_id_list'].pop(0)
                if not LLOuter_1['wafer_id_list']:
                    LLOuter_1['run_time'] = 0
                ATR_mdl_name = LLOuter_1['name']
            elif LLOuter_2['name'] not in [VTR1_mdl_name, VTR2_mdl_name] and LLOut.instance().judge_out_pick(LLOuter_2):
                atr['use'] = True
                atr['wafer_id'] = LLOuter_2['wafer_id_list'][0]
                Wafer_list[atr['wafer_id']]['pick'] = False
                LLOuter_2['wafer_id_list'].pop(0)
                if not LLOuter_2['wafer_id_list']:
                    LLOuter_2['run_time'] = 0
                ATR_mdl_name = LLOuter_2['name']

        # pick LLInner准备出仓的晶圆
        if not VTR1_mdl_name:
            vtr1 = VTR_1[0] if not VTR_1[0]['use'] else VTR_1[1]
            if LLInner['name'] not in [ATR_mdl_name, VTR2_mdl_name]:
                conflict = False  # 如果下一秒存在紧急的PM，则先不pick
                for pm in [PM2, PM3, PM4]:
                    if pm['deal_time'] - pm['run_time'] == 1:
                        conflict = True
                if not conflict:
                    for i, id in enumerate(LLInner['wafer_id_list']):
                        ix = Wafer_list[id]['index']
                        if ix == 5:  # 加工路径中下标第5个
                            continue
                        if LLInner['run_time_list'][i] < LLInner['deal_time']:
                            continue
                        LLInner['wafer_id_list'].pop(i)
                        LLInner['run_time_list'].pop(i)
                        vtr1['use'] = True
                        vtr1['run_time'] = 0
                        vtr1['wafer_id'] = id
                        Wafer_list[id]['pick'] = False
                        VTR1_mdl_name = LLInner['name']
                        break

        # pick LLInner准备入仓的晶圆
        if not VTR2_mdl_name:
            vtr2 = VTR_2[0] if not VTR_2[0]['use'] else VTR_2[1]
            if LLInner['name'] not in [ATR_mdl_name, VTR1_mdl_name]:
                conflict = False  # 如果下一秒存在紧急的PM，则先不pick
                for pm in [PM21, PM22, PM23, PM24, PM25]:
                    if pm['deal_time'] - pm['run_time'] == 1:
                        conflict = True
                if not conflict:
                    for i, id in enumerate(LLInner['wafer_id_list']):
                        ix = Wafer_list[id]['index']
                        if ix != 5:  # 加工路径中下标第5个
                            continue
                        if LLInner['run_time_list'][i] < LLInner['deal_time']:
                            continue
                        LLInner['wafer_id_list'].pop(i)
                        LLInner['run_time_list'].pop(i)
                        vtr2['use'] = True
                        vtr2['run_time'] = 0
                        vtr2['wafer_id'] = id
                        Wafer_list[id]['pick'] = False
                        VTR2_mdl_name = LLInner['name']
                        break

        # pick Multi_PM的晶圆
        if not VTR1_mdl_name:
            vtr1 = VTR_1[0] if not VTR_1[0]['use'] else VTR_1[1]
            # 如果有其他机械臂需要place，则先不pick
            if Multi_PM['name'] not in [ATR_mdl_name, VTR2_mdl_name] and \
                    Multi_PM['wafer_id_list'] and Multi_PM['run_time_list'][0] >= Multi_PM['deal_time']:
                conflict = False
                for r in VTR_2:
                    if r['use']:
                        i = r['wafer_id']
                        mdl_list = Path[i%2][Wafer_list[i]['index'] + 1]
                        if len(mdl_list) == 1 and mdl_list[0] == LLInner:
                            conflict = True
                            break
                if not conflict:
                    id = Multi_PM['wafer_id_list'][0]
                    Multi_PM['wafer_id_list'].pop(0)
                    Multi_PM['run_time_list'].pop(0)
                    vtr1['use'] = True
                    vtr1['run_time'] = 0
                    vtr1['wafer_id'] = id
                    Wafer_list[id]['pick'] = False
                    VTR1_mdl_name = Multi_PM['name']

        # pick LLOuter准备入仓的晶圆
        if not ATR_mdl_name:
            atr = ATR[0] if not ATR[0]['use'] else ATR[1]
            if LLOuter_1['name'] not in [VTR1_mdl_name, VTR2_mdl_name] and LLOut.instance().judge_in_pick(LLOuter_1):
                atr['use'] = True
                atr['wafer_id'] = LLOuter_1['wafer_id_list'][0]
                Wafer_list[atr['wafer_id']]['pick'] = False
                LLOuter_1['wafer_id_list'].pop(0)
                if not LLOuter_1['wafer_id_list']:
                    LLOuter_1['run_time'] = 0
                ATR_mdl_name = LLOuter_1['name']
            elif LLOuter_2['name'] not in [VTR1_mdl_name, VTR2_mdl_name] and LLOut.instance().judge_in_pick(LLOuter_2):
                atr['use'] = True
                atr['wafer_id'] = LLOuter_2['wafer_id_list'][0]
                Wafer_list[atr['wafer_id']]['pick'] = False
                LLOuter_2['wafer_id_list'].pop(0)
                if not LLOuter_2['wafer_id_list']:
                    LLOuter_2['run_time'] = 0
                ATR_mdl_name = LLOuter_2['name']

        # pick LP的晶圆
        if not ATR_mdl_name:
            atr = ATR[0] if not ATR[0]['use'] else ATR[1]
            if pick_LP and not PRE['use']:
                LP = LoadPort.instance().LP_pick_strategy()
                if LP is not None:
                    id = LP['wafer_id_list'][0]
                    atr['use'] = True
                    atr['wafer_id'] = id
                    Wafer_list[id]['pick'] = False
                    LP['wafer_id_list'].pop(0)
                    if not LP['wafer_id_list']:
                        LP['run_time'] = 0
                        LP['load_use'] = False
                    ATR_mdl_name = LP['name']
                    pick_LP_done = True

        if ATR_mdl_name and ATR_output:
            result_list.append("[%s] [%s] [Pick] [Wafer_%d] [%s]" % (real_time.strftime(Time_format), atr['name'], atr['wafer_id'], ATR_mdl_name))
        if VTR1_mdl_name and VTR1_output:
            result_list.append("[%s] [%s] [Pick] [Wafer_%d] [%s]" % (real_time.strftime(Time_format), vtr1['name'], vtr1['wafer_id'], VTR1_mdl_name))
        if VTR2_mdl_name and VTR2_output:
            result_list.append("[%s] [%s] [Pick] [Wafer_%d] [%s]" % (real_time.strftime(Time_format), vtr2['name'], vtr2['wafer_id'], VTR2_mdl_name))

        return pick_LP_done


if __name__ == "__main__":
    Robot.instance().ATR_strategy()