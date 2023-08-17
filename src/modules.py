#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime

Time_format = "%Y/%m/%d %H:%M:%S"
Real_time = datetime.datetime.now()

LP1, LP2, LP3 = ({
    "name": "LP%d" % i,
    "capacity": 25,
    "load_time": 10,
    "unload_time": 10,
    "unload_type": False,  # 当前的晶圆是否准备卸载
    "load_use": False,
    "unload_use": False,
    "wafer_id_list": [],
    "run_time": 0,
} for i in [1, 2, 3])

Buffer = {
    "name": "Buffer",
    "capacity": 1,
    "deal_time": 1,
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 29,
}

PRE = {
    "name": "PRE",
    "capacity": 1,
    "deal_time": 5,
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 0,
}

Multi_PM = {
    "name": "Multi_PM",
    "capacity": 15,
    "deal_time": 50,
    "wafer_id_list": [],
    "run_time_list": [],
    "reside": 15,
}

PM2, PM3, PM21, PM22, PM23, PM24 = ({
    "name": "PM%d" % i,
    "capacity": 1,
    "deal_time": 30,
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 0,
} for i in [2, 3, 21, 22, 23, 24])

PM4 = {
    "name": "PM4",
    "capacity": 1,
    "deal_time": 40,
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 0,
}

PM25 = {
    "name": "PM25",
    "capacity": 1,
    "deal_time": 60,
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 0,
}

# 自定义：1进，2出
LLOuter_1, LLOuter_2 = ({
    "name": "LLOuter_%d" % i,
    "capacity": 2,
    "in_time": 20,
    "out_time": 10,
    "use": False,
    "wafer_id_list": [],
    "run_time": 0,
} for i in [1, 2])

LLInner = {
    "name": "LLInner",
    "capacity": 4,
    "deal_time": 1,
    "wafer_id_list": [],
    "run_time_list": [],
    "reside": 29,
}

ATR = [{
    "name": "ATR_%s" % i,
    "deal_time": 1,
    "modules_list": [LP1, LP2, LP3, PRE, Buffer, LLOuter_1, LLOuter_2],
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 1,
} for i in ['A', 'B']]

VTR_1 = [{
    "name": "VTR_1%s" % i,
    "deal_time": 1,
    "modules_list": [LLOuter_1, LLOuter_2, PM2, PM3, PM4, Multi_PM, LLInner],
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 1,
} for i in ['A', 'B']]

VTR_2 = [{
    "name": "VTR_2%s" % i,
    "deal_time": 1,
    "modules_list": [LLInner, PM21, PM22, PM23, PM24, PM25],
    "use": False,
    "wafer_id": 0,
    "run_time": 0,
    "reside": 1,
} for i in ['A', 'B']]

Wafer_num = 1000
Wafer_list = [{}]
Wafer_list.extend([
    {"length": 11, "index": -1, "pick": False} if i % 2 == 1 else
    {"length": 13, "index": -1, "pick": False} for i in range(1, 1001)
])

Path1 = [
    [LP1, LP2, LP3],
    [PRE],
    [LLOuter_1, LLOuter_2],
    [PM2, PM3],
    [Multi_PM],
    [LLInner],
    [PM21, PM22],
    [PM23, PM24],
    [LLInner],
    [LLOuter_1, LLOuter_2],
    [LP1, LP2, LP3],
]

Path2 = Path1[:8] + [
    [PM25],
    [LLInner],
    [PM4],
    [LLOuter_1, LLOuter_2],
    [LP1, LP2, LP3],
]

Path = [Path2, Path1]


if __name__ == "__main__":
    print(ATR)
    print(VTR_1)
    print(VTR_2)
    print(Path1)
    print(Path2)
    # print(LP2['name'] in Path1[0])
