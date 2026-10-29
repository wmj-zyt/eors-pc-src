# 基于GEC的轻量级鸿蒙的驻留方法及应用

2026 开源鸿蒙大学生创新大赛赛道一参赛材料，包含上位机源码、板端 C 工程、技术方案书与答辩 PPT。

## 01_EORS_Source

EORS 上位机源码，版本 V5.31 release 20260703，Python + PySide6 桌面程序，入口文件为 main.py。

P01_Doc 说明文档
P02_Resource 图标、配置、帮助页等资源
P03_Components 自定义控件
P04_Model 模型定义与训练逻辑
P05_Database 数据库文件目录
P06_Utils 串口、配置与业务总线等工具层
P07_View Qt Designer 界面文件及生成的界面代码
P08_Activity 各业务界面逻辑

## 02_C工程

板端 C 工程。

GEC_BIOS BIOS 驻留层，含已固化 LiteOS 内核的固件 BIOS-LiteOS-D1-H-V3.2.hex
User/02-Hand-MobileNetV2 用户工程，板端运行程序
User/04-Hand-MobileNetV2-Test 用户工程测试版本

两个用户工程目录结构一致：

00_Spl 启动代码
01_Doc 工程说明
02_CPU CPU 相关驱动
03_MCU 片上外设驱动
04_GEC 驻留适配层
05_UserBoard 统一 API 层，含 Os_United_API.h 与 Os_United_API.c
06_AlgorithmComponent 算法组件
07_AppPrg 应用主程序，含 main.c 与业务线程

## 03_Docs

技术方案书 基于GEC的轻量级鸿蒙的驻留方法及应用-261011.docx

## 04_PPT

答辩演示文稿 基于GEC的轻量级鸿蒙的驻留方法及应用-261013.pptx，共 28 页

## 编译工具与演示视频

编译工具 AHL-GEC-vsCode-IDE v5.13

https://github.com/wmj-zyt/eors-pc-src/releases/download/v1.0/AHL-GEC-vsCode-IDE-v5.13.zip

演示视频

https://github.com/wmj-zyt/eors-pc-src/releases/download/v1.0/demo-video.mp4

全部下载文件见

https://github.com/wmj-zyt/eors-pc-src/releases
