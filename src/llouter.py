#!/usr/bin/env python
# -*- coding: utf-8 -*-

from src.modules import *

class LLOut(object):
    _instance = None

    @staticmethod
    def instance():
        if LLOut._instance is None:
            LLOut._instance = LLOut()
        return LLOut._instance

    @staticmethod
    def release():
        LLOut._instance = None

    # 判断晶圆出仓时能够pick
    def judge_out_pick(self, mdl):
        if mdl['out_type'] and mdl['run_time'] >= mdl['out_time']:
            return True
        return False

    # 判断晶圆进仓时能否pick
    def judge_in_pick(self, mdl):
        if not mdl['out_type'] and mdl['run_time'] >= mdl['in_time']:
            return True
        return False

    # 晶圆准备出仓时的place策略
    def out_place_strategy(self):
        if LLOuter_1['out_type'] and LLOuter_1['run_time'] == 0 and \
                LLOuter_1['wafer_id_list'] and len(LLOuter_1['wafer_id_list']) < LLOuter_1['capacity']:
            return LLOuter_1
        if LLOuter_2['out_type'] and LLOuter_2['run_time'] == 0 and \
                LLOuter_2['wafer_id_list'] and len(LLOuter_2['wafer_id_list']) < LLOuter_2['capacity']:
            return LLOuter_2
        if not LLOuter_1['wafer_id_list']:
            return LLOuter_1
        if not LLOuter_2['wafer_id_list']:
            return LLOuter_2
        raise

    # 晶圆准备进仓时的place策略
    def in_place_strategy(self):
        if not LLOuter_1['out_type'] and LLOuter_1['run_time'] == 0 and \
                LLOuter_1['wafer_id_list'] and len(LLOuter_1['wafer_id_list']) < LLOuter_1['capacity']:
            return LLOuter_1
        if not LLOuter_2['out_type'] and LLOuter_2['run_time'] == 0 and \
                LLOuter_2['wafer_id_list'] and len(LLOuter_2['wafer_id_list']) < LLOuter_2['capacity']:
            return LLOuter_2
        if not LLOuter_1['wafer_id_list']:
            return LLOuter_1
        if not LLOuter_2['wafer_id_list']:
            return LLOuter_2
        raise
