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

    def judge_out_pick(self, mdl):
        if mdl['out_type'] and mdl['run_time'] >= mdl['out_time']:
            return True
        return False

    def judge_in_pick(self, mdl):
        if not mdl['out_type'] and mdl['run_time'] >= mdl['in_time']:
            return True
        return False

    def judge_out_place_one(self, LLOuter):
        if LLOuter['out_type'] and LLOuter['run_time'] == 0 and \
                len(LLOuter['wafer_id_list']) < LLOuter['capacity']:
            return True
        if not LLOuter['wafer_id_list']:
            return True
        return False

    def judge_out_place(self):
        place = self.judge_out_place_one(LLOuter_1)
        if not place:
            place = self.judge_out_place_one(LLOuter_2)
        return place

    def judge_in_place(self):
        pass

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
