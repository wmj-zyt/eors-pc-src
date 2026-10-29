# EORS PC 端软件

> 基于 GEC 的轻量级鸿蒙的驻留方法及应用 —— 相关材料

EORS（Embedded Object Recognition System，嵌入式物体认知系统）的 **PC 端配套软件**：完成数据采集与标注、模型训练、模型导出与构件生成，为上板端运行提供模型与工程文件。

本仓库对应《基于 GEC 的轻量级鸿蒙的驻留方法及应用》中的**应用承载层**——端侧焊接缺陷识别用例的上位机工具链。

---

## 目录

- [功能概览](#功能概览)
- [技术栈](#技术栈)
- [目录结构](#目录结构)
- [环境要求](#环境要求)
- [快速开始](#快速开始)
- [打包发布](#打包发布)
- [架构说明](#架构说明)
- [文档说明](#文档说明)

---

## 功能概览

| 模块 | 能力 |
|---|---|
| **数据采集** | 串口收图、摄像头实时采集、本地图片导入、视频导入与逐帧分解 |
| **数据增强** | 旋转（顺/逆时针 90°）、水平/垂直镜像、批量删除、应用到所有图片 |
| **模型训练** | 多网络可选、轮数/批量/学习率配置、自动训练（超参组合遍历）、实时曲线 |
| **模型推理** | 加载训练好的模型对单张/批量图片进行预测，输出类别与置信度 |
| **构件生成** | 将模型与配置打包为可部署到板端的构件 |
| **辅助功能** | 参数配置、串口管理、帮助文档 |

内置网络结构：`CNN`、`MobileNetV2`、`ShuffleNetV1`、`EfficientNetLite0`、`NCP`（Neural Circuit Policies，基于 `kerasncp`）。

---

## 技术栈

| 类别 | 选型 |
|---|---|
| 语言 | Python 3.10 |
| GUI | PySide6 6.5.0（Qt for Python）+ Qt Designer |
| 深度学习 | TensorFlow 2.12.0 / Keras 2.12.0 |
| 图像处理 | OpenCV 4.7、Pillow |
| 串口通信 | pyserial 3.5 |
| 数据处理 | NumPy 1.23.5、scikit-learn、scipy |
| 打包 | PyInstaller 5.13 + Inno Setup |

---

## 目录结构

```
EORS_PC_SRC_V5.31/
├── main.py                     # 程序入口：初始化服务总线 → 启动主窗口
├── requirements.txt            # 依赖清单
├── main.spec / EORS.spec       # PyInstaller 打包配置
├── EORS_installer.iss          # Inno Setup 安装包脚本
├── EORS.png / logo.ico         # 应用图标
│
├── P01_Doc/                    # 说明文档与更新记录（大文件未纳入版本库）
│   └── readme.txt              # 版本变更记录
├── P02_Resource/               # 静态资源
│   ├── configs/config.json     # 运行配置
│   ├── image.qrc / images/     # 图标资源
│   └── HelpDoc.html            # 内置帮助文档
├── P03_Components/             # 自定义 Qt 控件（按钮/图表/标签/视频播放器等）
├── P04_Model/                  # 网络结构定义
│   ├── CNN.py / MobileNetv2.py / ShuffleNetv1.py / EfficientNetLite0.py / NCP.py
│   ├── CustomCallback.py       # 训练回调（曲线刷新、早停）
│   └── kerasncp/               # NCP 网络依赖
├── P05_Database/               # 运行时数据库目录（空，首次运行生成）
├── P06_Utils/                  # 基础能力层
│   ├── serial_port/            # 串口收发
│   └── services_bus/           # 服务总线（服务注册/发现/UI 与配置管理）
├── P07_View/                   # 视图层（Qt Designer 产物）
│   ├── Qt_Designer_ui/         # *.ui 源文件
│   └── Qt_Designer_ui_py/      # 由 .ui 转出的 Ui_*.py
└── P08_Activity/               # 业务逻辑层
    ├── main_window.py          # 主窗口与模块调度
    ├── data_acuisition_widget.py   # 数据采集
    ├── model_training_widget.py    # 模型训练
    ├── model_predict_widget.py     # 模型推理
    ├── component_generate_widget.py# 构件生成
    ├── additional_function_widget.py# 辅助功能
    └── auto_train.py           # 自动训练（超参遍历）
```

---

## 环境要求

- **Windows 10 / 11**（串口与打包流程依赖 Windows）
- **Python 3.10**（TensorFlow 2.12 支持 3.8–3.11，不建议 3.12+）
- 已连接的串口设备（数据采集功能需要，缺失时其余功能仍可正常使用）

---

## 快速开始

```bash
# 1. 克隆
git clone https://gitee.com/wmj1126/eors-pc-src.git
cd eors-pc-src

# 2. 创建虚拟环境（推荐）
python -m venv venv
venv\Scripts\activate

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行
python main.py
```

> 依赖较多（TensorFlow 完整包），首次安装约 500 MB，建议使用国内镜像：
> `pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple`

---

## 打包发布

```bash
# 生成可执行目录
pyinstaller main.spec

# 生成安装包（需先安装 Inno Setup 6）
iscc EORS_installer.iss
```

产物默认输出到 `dist/`，安装包输出到 `Output/`。

---

## 架构说明

程序采用**分层 + 服务总线**的结构，各层之间通过 `P06_Utils/services_bus` 解耦，避免业务窗口直接互相引用：

```
        ┌───────────────────────────────┐
        │  P08_Activity  业务逻辑层      │  ← 窗口行为与流程编排
        ├───────────────────────────────┤
        │  P07_View      视图层          │  ← Qt Designer 生成的界面
        ├───────────────────────────────┤
        │  P03_Components 控件层         │  ← 可复用的自定义控件
        ├───────────────────────────────┤
        │  P04_Model     算法层          │  ← 网络结构与训练回调
        ├───────────────────────────────┤
        │  P06_Utils     基础能力层      │  ← 服务总线 / 串口 / 配置
        └───────────────────────────────┘
                    P02_Resource 静态资源
```

启动流程：`main.py` → 实例化 `MainWindow` → `service_initializer.initialize_services()` 注册服务 → 进入 Qt 事件循环。

服务通过 `ServiceID` 枚举标识（`SERIAL_PORT_MANAGER` / `UI_MANAGER` / `CONFIG_MANAGER`），调用方只依赖枚举与服务接口，不依赖具体实现类。

---

## 文档说明

`P01_Doc/` 中的详细设计文档（实现过程、用户手册、训练程序运行说明）体积较大（单文件最大 58 MB，含 648 张截图），**未纳入本仓库版本管理**，如需获取请通过赛事材料包或联系作者。

---

## 相关材料

- 上位机源码：本仓库
- 板端侧：LiteOS 驻留框架 + 端侧推理程序（见赛事材料包）
- 技术方案书与答辩 PPT：见赛事材料包

---

**苏州大学 · 逸君攻坚小队**
