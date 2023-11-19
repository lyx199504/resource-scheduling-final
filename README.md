# resource_scheduling-final
本项目提供了一种基于排队论和贪心思想的芯片制作工艺的晶圆调度方案，该方案是《首届全国工业互联网创新大赛》赛题四“产品生产资源调度优化”决赛第一名的参赛作品。

## 目录 Table of Contents

- [项目目录](#项目目录)
- [项目声明](#项目声明)

<h2 id="project">项目目录</h2>

├─ src (主要代码)<br>
&emsp;├─ processing.py (晶圆处理模块)<br>
&emsp;├─ modules.py (各模块数据定义)<br>
&emsp;├─ loadport.py (晶圆装卸载功能模块)<br>
&emsp;├─ llouter.py (LLOuter功能模块)<br>
&emsp;├─ robot.py (机械臂模块)<br>
&emsp;├─ update.py (数据更新模块)<br>
&emsp;├─ interval_time_60.json (以60秒为基础生成的时间间隔表)<br>
&emsp;├─ interval_time_61.json (以61秒为基础生成的时间间隔表)<br>
&emsp;├─ interval_time_62.json (以62秒为基础生成的时间间隔表)<br>
├─ main.py (程序入口) <br>
├─ result.txt (生成的调度结果) <br>


<h2 id="statement">项目声明</h2>

本项目的作者及单位：<br>

    项目名称：resource_scheduling-final
    项目作者：Yixiang Lu, Kaichuan Kong
    作者单位：暨南大学网络空间安全学院（College of Cyber Security, Jinan University）
