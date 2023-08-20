#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.modules import *


class Output(object):
    _instance = None

    @staticmethod
    def instance():
        if Output._instance is None:
            Output._instance = Output()
        return Output._instance

    @staticmethod
    def release():
        Output._instance = None

    def pick(self, real_time, robot_name, wafer_id, mdl_name):
        return "[%s] [%s] [Pick] [Wafer_%d] [%s]" % (
            real_time.strftime(Time_format), robot_name, wafer_id, mdl_name
        )

    def place(self, real_time, robot_name, wafer_id, mdl_name):
        return "[%s] [%s] [Place] [Wafer_%d] [%s]" % (
            real_time.strftime(Time_format), robot_name, wafer_id, mdl_name
        )

    def LLOuter_start(self, real_time, mdl_name):
        return "[%s] [%s] [Start]" % (real_time.strftime(Time_format), mdl_name)

    def LLOuter_stop(self, real_time, mdl_name):
        return "[%s] [%s] [Stop]" % (real_time.strftime(Time_format), mdl_name)

    def LP_load(self, real_time, mdl_name):
        return "[%s] [%s] [Load]" % (real_time.strftime(Time_format), mdl_name)

    def LP_unload(self, real_time, mdl_name):
        return "[%s] [%s] [Unload]" % (real_time.strftime(Time_format), mdl_name)