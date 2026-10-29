from shelve import Shelf
from P07_View.Qt_Designer_ui_py.Ui_ComponentGenerateWidget import Ui_ComponentGenerateWidget

from PySide6.QtWidgets import QWidget
from PySide6.QtCore import Qt, Signal, QObject

import importlib.util
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGraphicsScene, QFileDialog, QGraphicsView, QTreeWidgetItem
import subprocess
import sys
import os
import tempfile

from P06_Utils.services_bus.services_bus import service_bus, ServiceID
from P06_Utils.services_bus.config_manager import ConfigManager
from P06_Utils.services_bus.ui_manager import UIManager
import numpy as np
import h5py

from P03_Components.customGraphicsView import CustomImageView


# 在page_component.py文件开头添加这段改进的检测代码
try:
    from keras.utils.vis_utils import model_to_dot
    pydot_available = True
    # 检查graphviz是否可用
    try:
        # 方法1: 直接调用dot命令
        subprocess.run(['dot', '-V'], capture_output=True, check=True, shell=True)
        graphviz_available = True
    except Exception:
        # 方法2: 尝试从Windows常见安装路径查找
        graphviz_paths = [
            'C:\\Program Files\\Graphviz\\bin\\dot.exe',
            'C:\\Program Files (x86)\\Graphviz\\bin\\dot.exe',
            os.path.expanduser('~\\AppData\\Local\\Graphviz\\bin\\dot.exe')
        ]
        graphviz_available = False
        for path in graphviz_paths:
            if os.path.exists(path):
                try:
                    subprocess.run([path, '-V'], capture_output=True, check=True)
                    graphviz_available = True
                    # 添加到环境变量
                    os.environ['PATH'] += os.pathsep + os.path.dirname(path)
                    break
                except:
                    continue
except ImportError:
    pydot_available = False
    graphviz_available = False

from keras.models import load_model

import re
from threading import Thread
from functools import partial
import random
from datetime import datetime
import json
import importlib
import subprocess

class ShowModelStructureSignals(QObject):
    """训练信号类"""
    update_model_structure_image = Signal(QPixmap)

"""
类名：ComponentGenerateWidget
基类：无
功能：构件生成类
"""
class ComponentGenerateWidget(Ui_ComponentGenerateWidget):
    # 模型权重
    model_weights = dict()
    # 优化器权重
    optimizer_weights = dict()
    # 模型配置
    model_configs = dict()
    # 模型标签
    model_labels = list()
    # 模型性能
    model_performance = list()
    # 允许生成构件标志
    enabledComponent = False

    """
    函数名称：__init__
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：初始化生成构件类对象
    """
    def __init__(self):
        super().__init__()

        self.__component_generate_widget = QWidget()

        self.setupUi(self.__component_generate_widget)

        self.ui_manager: UIManager = service_bus.get_service(ServiceID.UI_MANAGER)
        self.config_manager: ConfigManager = service_bus.get_service(ServiceID.CONFIG_MANAGER)

        # 实例化自定义可滚动视口
        self.view = CustomImageView(self.frame_43)
        # 设置视图的拖拽模式 ScrollHandDrag：光标变为手型，可以拖动场景进行移动
        self.view.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        # 将自定义可滚动视口添加到布局中
        self.verticalLayout_38.addWidget(self.view)

        self.show_model_structure_signal = ShowModelStructureSignals()
        self.model_list = []

        # 模型摘要信息
        self.model_summary = ""
        # 推理工程路径
        self.inferenceProjectPath = ""
        # 当前模型
        self.model = ""
        # 实例化QGraphicsScene对象
        self.scene = QGraphicsScene()
        self.view.setScene(self.scene)
        # 连接组件模型下拉框的索引变化信号到处理函数
        self.ComponentModelComboBox.currentIndexChanged.connect(self.comboBoxIndexChanged)
        # 连接模型信息树状控件的选择变化信号到处理函数
        self.modelInfoTreeWidget.itemSelectionChanged.connect(self.showModelArchitectureInfo)
        # 连接加载终端推理项目工程按钮的点击信号到处理函数
        self.loadTerminalInferenceProject.clicked.connect(self.loadProject)
        # 生成构件按钮默认设置为禁止点击状态
        self.generateComponentButton.setEnabled(False)
        # 连接生成组件按钮的点击信号到处理函数
        self.generateComponentButton.clicked.connect(self.generateComponent)
        # 刷新模型列表
        self.ui_manager.update_model_list.connect(self.refreshModelList)
        # Graphviz软件安装提示默认不可见
        self.graphvizInfo.setVisible(False)
        
        self.show_model_structure_signal.update_model_structure_image.connect(self.drawModelStructure)

    def get_widget(self):
        return self.__component_generate_widget

    """
    函数名称：comboBoxIndexChanged
    参数说明：index:当前选择的索引 
    函数返回：无
    功能概要： 处理组件模型下拉框的索引变化事件
    """
    def comboBoxIndexChanged(self):
        print("comboBoxIndexChanged")
        # 获取当前选择的模型文件名
        selectedModelFile = self.ComponentModelComboBox.currentText()
        if not selectedModelFile:
            # 清除当前显示的模型结构
            self.show_model_structure_signal.update_model_structure_image.emit(None)
            return

        dataset_path = self.config_manager.get("foldersPath.datasetPath")
        if not dataset_path or not os.path.exists(dataset_path):
            self.ui_manager.show_message_box("错误", "请先设置数据集路径", "critical")
            # 清除当前显示的模型结构
            self.show_model_structure_signal.update_model_structure_image.emit(None)
            return
        # 设置模型路径
        modelPath = f'{dataset_path}/{selectedModelFile}'
        self.modelPath = modelPath
        # 禁用组件生成
        ComponentGenerateWidget.enabledComponent = False
        # 创建新线程来显示模型结构
        t = Thread(target=self.showModelArchitecture, args=(selectedModelFile, modelPath))
        # 启动线程
        t.start()     

    

    """
    函数名称：refreshModelList
    参数说明：comboBox:QComboBox对象，表示要刷新的模型列表下拉框
    函数返回：无
    功能概要：刷新模型列表下拉框
    """
    def refreshModelList(self, model_list: list):
        if model_list == self.model_list:
            return
        self.model_list = model_list
        # 清空下拉框中的选项
        self.ComponentModelComboBox.clear()
        # 获取模型文件夹中的模型列表，并按创建时间降序排序
        # 将模型列表添加到下拉框中
        self.ComponentModelComboBox.addItems(model_list)


    """
    函数名称：showModelArchitecture
    参数说明：modelFile:模型文件名  modelPath:模型文件路径
    函数返回：无
    功能概要：处理组件模型下拉框的索引变化事件
    """
    def showModelArchitecture(self, modelFile, modelPath):
        try:
            # 设置模型信息树的标题为模型文件名
            self.modelInfoTreeWidget.setHeaderHidden(False)
            self.modelInfoTreeWidget.setHeaderLabel(modelFile)
            # 检查模型路径和模型文件是否存在
            if os.path.exists(modelPath) and modelFile:
                # 清除当前显示的模型结构
                # self.drawModelStructure('clear', None, self.scene, self.view)
                self.show_model_structure_signal.update_model_structure_image.emit(None)
                # 加载模型
                model = load_model(modelPath, custom_objects={})
                # 获取模型摘要并保存到summary_dict
                summary_dict = []
                model.summary(print_fn=lambda x: summary_dict.append(x))
                self.model_summary = '\n'.join(summary_dict)
                # 绘制模型结构图并保存为图片文件
                timestamp = datetime.now().timestamp()
                try:
                    self.graphvizInfo.setVisible(False)
                    # 使用临时文件目录来避免权限问题
                    with tempfile.TemporaryDirectory() as temp_dir:
                        dot_file_path = os.path.join(temp_dir, f"model_{timestamp}.dot")
                        output_file_path = os.path.join(temp_dir, f"model_{timestamp}.png")  # 输出图像路径
                        with open(dot_file_path, "w") as f:
                            if not pydot_available:
                                raise ImportError('pydot do not installed, please install it by: pip install pydot==1.4.2')
                            if not graphviz_available:
                                raise ImportError('Graphviz do not installed, please install it by: https://graphviz.org/download/\n。')
                            f.write(model_to_dot(model, show_shapes=True).to_string())
                        subprocess.run(
                            ["dot", "-Tpng", dot_file_path, "-o", output_file_path],
                            check=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            creationflags=subprocess.CREATE_NO_WINDOW,
                            shell=True  # 确保在Windows上正确执行
                        )
                        # plot_model(model, to_file=f'model_{timestamp}.png', show_shapes=True)
                        pixmap = QPixmap(output_file_path)
                        # 显示模型结构图
                        # self.drawModelStructure('draw', pixmap, self.scene, self.view)
                        self.show_model_structure_signal.update_model_structure_image.emit(pixmap)
                        # 临时目录会在with块结束后自动删除，不需要手动删除文件
                except Exception as e:
                    self.ui_manager.show_message_box("错误", f"模型结构图显示失败，请根据左下角“软件帮助”安装Graphviz\n错误信息：{e}", "critical")
                    self.graphvizInfo.setVisible(True)
                    self.ui_manager.show_status_message("模型结构图显示失败，请根据左下角“软件帮助”安装Graphviz")
                # 显示模型树结构
                ComponentGenerateWidget.showModelTree(modelPath, self.modelInfoTreeWidget)
                
            else:
                # 如果模型路径或文件不存在，清除当前显示的模型结构
                # self.drawModelStructure('clear', None, self.scene, self.view)
                self.show_model_structure_signal.update_model_structure_image.emit(None)
                self.modelInfoTreeWidget.setHeaderHidden(True)
                self.modelInfoTreeWidget.clear()
                self.modelStructureInfo.clear()
        except Exception as e:
            self.ui_manager.show_message_box("错误", str(e), "critical")
            print('An exception occurred')
        
    """
    函数名称：drawModelStructure
    参数说明：command:字符串，命令类型："clear"表示清空场景，"draw"表示绘制图像  pixmap:QPixmap对象，表示要绘制的图像 scene:QGraphicsScene对象，表示绘图场景  view:CustomImageView对象，表示绘图视图 
    函数返回：无
    功能概要：绘制模型结构图
    """
    def drawModelStructure(self, pixmap):
        print("drawModelStructure")
        if pixmap is None:
            self.scene.clear()
        else:
            # 添加图像到场景中，并显示视图
            self.scene.addPixmap(pixmap)
            self.view.setScene(self.scene)
            self.view.show()



    """
    函数名称：enableButton
    参数说明：cls:当前类 
    函数返回：无
    功能概要：启用生成构件按钮
    """
    @classmethod
    def enableButton(cls):
        cls.enabledComponent = True


    """
    函数名称：showModelArchitectureInfo
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：展示模型架构信息
    """
    def showModelArchitectureInfo(self):
        selectedItem = self.modelInfoTreeWidget.selectedItems()
        if selectedItem:
            # 获取选中的QTreeWidgetItem
            selectedItem = selectedItem[0]
            # 获取选中的QTreeWidgetItem的层级
            itemLevel = self.modelInfoTreeWidget.indexOfTopLevelItem(selectedItem)
            # 获取选中项的名称
            selectedItemName = selectedItem.text(0)
            # 如果选中的是 "模型基本信息"
            if selectedItemName == "模型基本信息":
                # 显示模型基本信息
                ComponentGenerateWidget.showModelBasicInfo(ComponentGenerateWidget.model_labels,ComponentGenerateWidget.model_performance, self.modelStructureInfo)
            # 如果选中的是 "模型基本结构"
            elif selectedItemName == "模型基本结构":
                # 显示模型摘要信息
                self.modelStructureInfo.setText(self.model_summary)
            # 如果选中的是其他项，获取父项信息
            else:
                # 获取父项
                parentItem = selectedItem.parent()
                if parentItem:
                    # 获取父项名称
                    parentItemName = parentItem.text(0)
                    # 获取父项层级
                    parentItemLevel = self.modelInfoTreeWidget.indexOfTopLevelItem(parentItem)
                    # 如果父项级别为2，显示模型各层简要信息
                    if parentItemLevel == 2:
                        # 打印模型各层简要信息
                        ComponentGenerateWidget.showModelStructureDictInfo(ComponentGenerateWidget.model_configs[selectedItemName], self.modelStructureInfo)
                    # 如果父项级别为-1，显示模型各层具体权重
                    elif parentItemLevel == -1:
                        # 打印模型各层具体权重
                        ComponentGenerateWidget.showModelLayerWeight(ComponentGenerateWidget.model_weights[parentItemName][selectedItemName], self.modelStructureInfo)
                    # 如果父项级别为3，显示优化器权重
                    elif parentItemLevel == 3:
                        # 打印优化器权重
                        ComponentGenerateWidget.showModelLayerWeight(ComponentGenerateWidget.optimizer_weights[selectedItemName], self.modelStructureInfo)


    """
    函数名称：loadProject
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：导入终端推理工程
    """
    def loadProject(self):
        # 显示状态信息: 正在导入推理工程
        self.ui_manager.show_status_message("导入推理工程")
        
        # 打开文件对话框，选择推理工程目录
        projectPath = QFileDialog.getExistingDirectory(self.__component_generate_widget, caption="导入终端推理程序")
        # 如果没有选择目录，则显示取消导入信息并退出函数
        if not projectPath:
            self.ui_manager.show_status_message("取消导入推理工程")
            return
        # 如果选择了目录，则显示导入成功信息
        self.ui_manager.show_status_message("导入推理工程成功！")
        # 设置应用程序实例的推理工程路径
        self.inferenceProjectPathLineEdit.setText(projectPath)
        self.inferenceProjectPath = projectPath
        # 设置文本框的边距
        self.inferenceProjectPathLineEdit.setTextMargins(4, 4, 4, 4)
        # 生成构件按钮设置为可点击状态
        self.generateComponentButton.setEnabled(True)


    """
    函数名称：anayze_model
    参数说明：model:模型
    函数返回：无
    功能概要：解析模型结构
    """
    def analyze_model(self, model, json_model:list):
        identity_layers = ["BatchNormalization", "Activation", "Dropout"]
        model_config = dict()
        for index, layer in enumerate(model.layers):
            layer_config = dict()
            layer_name = layer.name
            # class_name
            layer_config['class_name'] = layer.__class__.__name__
            # input
            if (layer_config['class_name'] != 'InputLayer'):
                if (isinstance(layer.input, list)):
                    layer_config['input'] = list()
                    for input_tensor in layer.input:
                        layer_config['input'].append(model_config[input_tensor.name.split("/")[0]]["output"])
                else:
                    layer_config['input'] = model_config[layer.input.name.split("/")[0]]["output"]
            # output
            if (layer_config['class_name'] == "InputLayer"):
                layer_config['output'] = "g_modelInputImage"
            elif (layer_config['class_name'] in identity_layers):
                layer_config['output'] = layer_config['input']
            else:
                if (isinstance(layer.output, list)):
                    layer_config['output'] = list()
                    for output_tensor in layer.output:
                        layer_config['output'].append(output_tensor.name.split("/")[0])
                else:
                    layer_config['output'] = layer.output.name.split("/")[0]
            # output_shape
            if (isinstance(layer.output_shape, list)):
                layer_config['output_shape'] = layer.output_shape[0][1:][-1:] + layer.output_shape[0][1:][0:-1]
            else:
                layer_config['output_shape'] = layer.output_shape[1:][-1:] + layer.output_shape[1:][0:-1]
            # weight
            layer_config["weights"] = list()
            if (layer_config["class_name"] == "Conv2D" or layer_config["class_name"] == "DepthwiseConv2D"):
                for weight in layer.weights:
                    layer_config["weights"].append(weight.name.replace("/", "_").split(":")[0])
            elif (layer_config["class_name"] == "BatchNormalization"):
                layer_config["weights"].append(layer_name + "_params")
            # strides
            if hasattr(layer, "strides"):
                layer_config["stride"] = layer.strides[0]
            # activation 激活函数类型
            if layer_config["class_name"] == "Activation":
                layer_config["activation"] = json_model[index]['config']['activation']
            model_config[layer_name] = layer_config
        return model_config
    
    """
    函数名称：get_layer_code
    参数说明：class_name:层类型 layer_config:层配置
    函数返回：层对应代码
    功能概要：返回对应终端代码
    """
    def get_layer_code(self, class_name: str, layer_config: dict) -> str:
        if class_name == "InputLayer" or class_name == "Dropout":
            return ""
        elif class_name == "Conv2D":
            return f"CONV2D({layer_config['input']}, {layer_config['output']}, {layer_config['weights'][0]}, {layer_config['weights'][1]}, {layer_config['stride']}, \"same\");\n"
        elif class_name == "BatchNormalization":
            return f"BATCH_NORMALIZATION({layer_config['input']}, {layer_config['weights'][0]});\n"
        elif class_name == "Activation":
            activation = layer_config["activation"]
            if activation == "softmax":
                return f"SOFTMAX({layer_config['input']});\n"
            else:
                return f"ACTIVATION({layer_config['input']}, {activation});\n"
        elif class_name == "DepthwiseConv2D":
            return f"DEPTHWISE_CONV2D({layer_config['input']}, {layer_config['output']}, {layer_config['weights'][0]},{layer_config['weights'][1]}, {layer_config['stride']});\n"
        elif class_name == "Add":
            return f"ADD({layer_config['input'][0]}, {layer_config['input'][1]}, {layer_config['output']});\n"
        elif class_name == "GlobalAveragePooling2D":
            return f"GLOBALAVERAGEPOOLING({layer_config['input']}, {layer_config['output']});\n"
        elif class_name == "Reshape":
            return f"RESHAPE({layer_config['input']}, {layer_config['output']});\n"

    """
    函数名称：generateComponent
    参数说明：app:应用程序对象 
    函数返回：无
    功能概要：生成终端构件
    """
    def generateComponent(self):
        sort_order = ['gamma', 'beta', 'mean', 'variance']
        sort_num = len(self.model_labels)
        # 检查是否允许生成组件
        if not ComponentGenerateWidget.enabledComponent:
            self.ui_manager.show_message_box("警告", "还未选择模型文件", "warning")
            return
        
        code_generation_time = datetime.now().strftime("%Y年%m月%d日 %H:%M:%S")
        # 加载并解析模型
        # 获取数据集路径（从配置管理器中读取）
        dataset_path = self.config_manager.get("foldersPath.datasetPath")
        if not dataset_path or not os.path.exists(dataset_path):
            self.ui_manager.show_message_box("错误", "请先设置数据集路径", "critical")
            return
        # 获取数据集名称（从路径中提取最后一级目录名）
        dataset_name = os.path.basename(dataset_path)

        # 模型文件名
        model_file = self.ComponentModelComboBox.currentText()
        # 正则表达式匹配
        match = re.search(f'{dataset_name}_([^_]+)_\d+', model_file)
        # 获取模型名称
        model_name = match.group(1)
        # 指定模块加载路径
        curr_dir = os.path.dirname(__file__)
        # 构建模型配置文件的目录路径（上级目录的 P04_Model 文件夹）
        model_dir = os.path.join(curr_dir, "..", "P04_Model")
        # 构建模型配置文件的完整路径（Python 文件）
        module_path = os.path.join(model_dir, f"{model_name}.py")

        # 创建模块规范对象，指定模块名称和文件路径
        module_spec = importlib.util.spec_from_file_location(model_name, module_path)
        # 根据规范创建模块对象
        model_module = importlib.util.module_from_spec(module_spec)
        # 执行模块代码，加载模块内容
        module_spec.loader.exec_module(model_module)
        _custom_objects = getattr(model_module, 'custom_objects', None)
        self.model = load_model(f"{dataset_path}/{self.ComponentModelComboBox.currentText()}", custom_objects=_custom_objects)
        # 解析模型
        json_model = json.loads(self.model.to_json())['config']['layers']
        layer_config = self.analyze_model(self.model, json_model)  #解析模型文件结构
        model_config = dict()
        model_config['layer_config'] = layer_config
        model_config['output'] = self.model.output.name.split("/")[0]

        model_name_lower = model_name.lower()

        # 检查是否已选择推理工程路径
        if self.inferenceProjectPath:
            try:
                # 初始化头文件内容
                headerFileContent = ""
                # 打开或创建模型初始化C文件
                with open(f"{self.inferenceProjectPath}/06_AlgorithmComponent/{model_name_lower}.c", "w") as f:
                    # 写入文件头注释
                    f.write("//=====================================================================\n"
                            f"// 文件名称：{model_name_lower}.c\n"
                            "// 功能概要：模型驱动构件源文件\n"
                            "// 制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)\n"
                            "// 版    本：2025-12-07  V3.0\n"
                            "// 适用芯片：D1-H\n"
                            "//=====================================================================\n")
                    
                    # 添加必要的头文件
                    f.write(f"#include \"{model_name_lower}.h\"\n")
                    f.write("#include <math.h>\n\n")
                    
                    # ========== 添加 relu6 和 softmax 函数 ==========
                    f.write("//=====================================================================\n"
                            "// 函数名称:relu6\n"
                            "// 函数返回:激活值\n"
                            "// 参数说明:x:待激活值\n"
                            "// 功能概要:将输出值限制在(0,6)之间\n"
                            "//=====================================================================\n")
                    f.write("float relu6(float x)\n"
                            "{\n"
                            "    if (x <= 0)\n"
                            "        return 0;\n"
                            "    else if (x > 6)\n"
                            "        return 6;\n"
                            "    return x;\n"
                            "}\n\n")
                    
                    f.write("//=====================================================================\n"
                            "// 函数名称:softmax\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入数组指针, dim:数组维度\n"
                            "// 功能概要:Softmax激活函数，直接修改input数组\n"
                            "//=====================================================================\n")
                    f.write("void softmax(float *input, int dim) {\n"
                            "    float max_val = input[0];\n"
                            "    float sum_exp = 0.0;\n\n"
                            "    // 找最大值，避免指数溢出\n"
                            "    for (int i = 1; i < dim; i++) {\n"
                            "        if (input[i] > max_val) {\n"
                            "            max_val = input[i];\n"
                            "        }\n"
                            "    }\n\n"
                            "    // 计算指数并求和\n"
                            "    for (int i = 0; i < dim; i++) {\n"
                            "        input[i] = expf(input[i] - max_val);\n"
                            "        sum_exp += input[i];\n"
                            "    }\n\n"
                            "    // 归一化输出\n"
                            "    for (int i = 0; i < dim; i++) {\n"
                            "        input[i] /= sum_exp;\n"
                            "    }\n"
                            "}\n\n")
                    f.write("//=====================================================================\n"
                            "// 文件名称：model.c\n"
                            "// 功能概要：模型驱动构件源文件\n"
                            "// 制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)\n"
                            "// 版    本：2025-12-07  V3.0\n"
                            "// 适用芯片：D1-H\n"
                            "//=====================================================================\n")
                    f.write(f"#include \"{model_name_lower}.h\"\n\n")
                    
                    # 处理模型权重数据格式转换 (Keras默认channels_last格式):
                    # Conv2D: (h,w,c_in,c_out) --> (c_in,c_out,h,w) 转为MCU格式
                    # DepthwiseConv2D: (h,w,c_in,depth_mult) --> (c_in,depth_mult,h,w) 转为MCU格式
                    for layer_name, weightdict in self.model_weights.items():
                        layer = layer_name.rsplit('_')
                        layer_num = layer[-1]
                        if layer_num.isdigit():
                            layer_num = int(layer_num)
                        else:
                            layer_num = 0
                        # 各层类型
                        layerName = layer[0]
                        # 处理卷积层权重数据
                        if layerName == "conv2d":
                            # 遍历权重字典
                            for weight_name, _weight in weightdict.items():
                                # 权重形状
                                weight_shape = _weight[0]
                                # 权重值，MumPy数组
                                weight = _weight[1]
                                # 卷积核权重
                                if weight_name.endswith("kernel:0"):
                                    weight = weight.transpose((2, 3, 0, 1))
                                    f.write(f"//卷积层{layer_num + 1}卷积核的权重\n")
                                    f.write(f"const float {weight_name.replace('/', '_').split(':')[0]}{''.join([f'[{x}]' for x in weight.shape])}=\n")
                                    # 头文件声明内容
                                    headerFileContent += f"const float {weight_name.replace('/', '_').split(':')[0]}{''.join([f'[{x}]' for x in weight.shape])};  //卷积层{layer_num + 1}卷积核的权重\n"
                                    f.write(ComponentGenerateWidget.numpyArrayToCArray(weight))
                                # 卷积偏置权重
                                else: 
                                    f.write(f"\n//卷积层{layer_num + 1}卷积核的偏置\n")
                                    f.write(f"const float {weight_name.replace('/', '_').split(':')[0]}[{weight_shape[0]}]=")
                                    # 头文件声明内容
                                    headerFileContent += f"const float {weight_name.replace('/', '_').split(':')[0]}[{weight_shape[0]}];  //卷积层{layer_num + 1}卷积核的偏置\n"
                                    f.write('{'+f"{', '.join([str(x) for x in weight])}"+'};\n')
                        # 处理深度卷积层权重数据
                        elif layerName == "depthwise":
                            # 遍历权重字典
                            for weight_name, _weight in weightdict.items():
                                # 权重形状
                                weight_shape = _weight[0]
                                # 权重值，MumPy数组
                                weight = _weight[1]
                                # 深度卷积核权重
                                if weight_name.endswith("kernel:0"):
                                    weight = weight.transpose((2, 3, 0, 1))
                                    f.write(f"//深度卷积层{layer_num + 1}卷积核的权重\n")
                                    f.write(f"const float {weight_name.replace('/', '_').split(':')[0]}{''.join([f'[{x}]' for x in weight.shape])}=\n")
                                    # 头文件声明内容
                                    headerFileContent += f"const float {weight_name.replace('/', '_').split(':')[0]}{''.join([f'[{x}]' for x in weight.shape])};  //深度卷积层{layer_num + 1}卷积核的权重\n"
                                    f.write(ComponentGenerateWidget.numpyArrayToCArray(weight))
                                # 深度卷积核偏置
                                else:
                                    f.write(f"//深度卷积层{layer_num + 1}卷积核的偏置\n")
                                    f.write(f"const float {weight_name.replace('/', '_').split(':')[0]}[{weight_shape[0]}]=\n")
                                    # 头文件声明内容
                                    headerFileContent += f"const float {weight_name.replace('/', '_').split(':')[0]}[{weight_shape[0]}];  //深度卷积层{layer_num + 1}卷积核的偏置\n"
                                    f.write('{'+f"{', '.join([str(x) for x in weight])}"+'};')
                        # 处理归一化层权重数据        
                        elif layerName == "batch":
                            # 根据sort_order顺序重新排序权重字典
                            weightdict = dict(sorted(weightdict.items(), key=lambda item: ComponentGenerateWidget.get_sort_index(item[0], sort_order)))
                            f.write(f"//BN归一层{layer_num + 1}参数\n")
                            random_key = random.choice(list(weightdict.keys()))
                            dimension = weightdict[random_key][0][0]
                            f.write(f"const float {layer_name}_params[{len(weightdict)}][{dimension}]=\n")
                            # 头文件声明内容
                            headerFileContent += f"const float {layer_name}_params[{len(weightdict)}][{dimension}];  //BN归一层{layer_num + 1}参数\n"
                            f.write("{\n")
                            weightlist = [v for _, v in weightdict.values()]
                            for w in weightlist:
                                f.write('{'+f"{', '.join([str(x) for x in w])}"+'},\n')
                            f.write("};\n")
                # 打开或创建模型初始化头文件
                with open(f"{self.inferenceProjectPath}/06_AlgorithmComponent/{model_name_lower}.h", "w") as f:
                    # 文件头注释
                    f.write("//=====================================================================\n"
                            "//文件名称：model_ops.h\n"
                            "//功能概要：模型驱动构件源文件\n"
                            "//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)\n"
                            "//版    本：2022-07-14  V1.0\n"
                            "//适用芯片：D1\n"
                            "//=====================================================================\n")
                    
                    # 头文件保护
                    f.write("#ifndef MODEL_OPS_H\n")
                    f.write("#define MODEL_OPS_H\n\n")
                    
                    # 包含头文件
                    f.write("#include <math.h>\n")
                    f.write("#include <string.h>\n\n")
                    
                    # max宏定义
                    f.write("#define max(a, b) (((a) > (b)) ? (a) : (b))\n\n")
                    
                    # GETLENGTH宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:GETLENGTH\n"
                            "// 函数返回:数组长度\n"
                            "// 参数说明:array:输入数组\n"
                            "// 功能概要:计算数组元素个数\n"
                            "//=====================================================================\n")
                    f.write("#define GETLENGTH(array) (sizeof(array) / sizeof(*(array)))\n\n")
                    
                    # GETCOUNT宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:GETCOUNT\n"
                            "// 函数返回:float数组元素个数\n"
                            "// 参数说明:array:输入数组\n"
                            "// 功能概要:计算float类型的数组个数\n"
                            "//=====================================================================\n")
                    f.write("#define GETCOUNT(array) (sizeof(array) / sizeof(float))\n\n")
                    
                    # FOREACH宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:FOREACH\n"
                            "// 函数返回:无\n"
                            "// 参数说明:   i:临时计数变量\n"
                            "//        count:总循环次数\n"
                            "// 功能概要:进行for循环\n"
                            "//=====================================================================\n")
                    f.write("#define FOREACH(i, count) for (int i = 0; i < count; ++i)\n\n")
                    
                    # Data_Padding宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:Data_Padding\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组指针，afterPadding:填充后元素数组指针,p:填充所需元素\n"
                            "// 功能概要:填充输入层\n"
                            "//=====================================================================\n")
                    f.write("#define Data_Padding(input, afterPadding, pad_top, pad_right, pad_bottom, pad_left)                                                       \\\n"
                            "\t{                                                                                                                                     \\\n"
                            "\t\tFOREACH(h, GETLENGTH(afterPadding))                                                                                               \\\n"
                            "\t\tFOREACH(w, GETLENGTH(*afterPadding))                                                                                              \\\n"
                            "\t\t{                                                                                                                                 \\\n"
                            "\t\t\tif (w < pad_left || w >= (GETLENGTH(*afterPadding) - pad_right) || h < pad_top || h >= (GETLENGTH(afterPadding) - pad_bottom)) \\\n"
                            "\t\t\t\tafterPadding[h][w] = 0;                                                                                                   \\\n"
                            "\t\t\telse                                                                                                                          \\\n"
                            "\t\t\t\tafterPadding[h][w] = input[h - pad_top][w - pad_left];                                                                    \\\n"
                            "\t\t}                                                                                                                                 \\\n"
                            "\t}\n\n")
                    
                    # CONVOLUTE_VALID宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:CONVOLUTE_VALID\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//\t\t  output:输出层元素数组首地址指针\n"
                            "//        weight:输入层与输出层之间权重数组指针\n"
                            "//        s:步长\n"
                            "// 功能概要:进行权重的赋值传播\n"
                            "//=====================================================================\n")
                    f.write("#define CONVOLUTE_VALID(input, output1, weight, s)                                 \\\n"
                            "\t{                                                                              \\\n"
                            "\t\tfor (int o0 = 0; o0 < GETLENGTH(output1); ++o0)                            \\\n"
                            "\t\t\tfor (int o1 = 0; o1 < GETLENGTH(*output1); ++o1)                       \\\n"
                            "\t\t\t\tFOREACH(w0, GETLENGTH(weight))                                     \\\n"
                            "\t\t\t\t\tFOREACH(w1, GETLENGTH(*(weight)))                                          \\\n"
                            "\t\t\t\t\t\t(output1)[o0][o1] += (input)[o0 * s + w0][o1 * s + w1] * (weight)[w0][w1]; \\\n"
                            "\t}\n\n")
                    
                    # DEPTHWISE_CONVOLUTE_VALID宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:DEPTHWISE_CONVOLUTE_VALID\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//\t\t  output:输出层元素数组首地址指针\n"
                            "//        weight:输入层与输出层之间权重数组指针\n"
                            "//        s:步长\n"
                            "// 功能概要:进行深度可分离卷积操作(使用赋值而非累加)\n"
                            "//=====================================================================\n")
                    f.write("#define DEPTHWISE_CONVOLUTE_VALID(input, output1, weight, s)                       \\\n"
                            "\t{                                                                              \\\n"
                            "\t\tfor (int o0 = 0; o0 < GETLENGTH(output1); ++o0) {                          \\\n"
                            "\t\t\tfor (int o1 = 0; o1 < GETLENGTH(*output1); ++o1) {                     \\\n"
                            "\t\t\t\tfloat sum = 0;                                                     \\\n"
                            "\t\t\t\tFOREACH(w0, GETLENGTH(weight)) {                                   \\\n"
                            "\t\t\t\t\tFOREACH(w1, GETLENGTH(*(weight))) {                            \\\n"
                            "\t\t\t\t\t\tsum += (input)[o0 * s + w0][o1 * s + w1] * (weight)[w0][w1];   \\\n"
                            "\t\t\t\t\t}                                                              \\\n"
                            "\t\t\t\t}                                                              \\\n"
                            "\t\t\t\t(output1)[o0][o1] = sum;                                           \\\n"
                            "\t\t\t}                                                              \\\n"
                            "\t\t}                                                                  \\\n"
                            "\t}\n\n")
                    
                    # CONV2D宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:Conv2D\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//\t\t   output:输出层元素数组首地址指针\n"
                            "//         kernel:输入层与输出层之间权值数组指针\n"
                            "//         bias:输入层与输出层之间偏置数组指针\n"
                            "//         strides:步长\n"
                            "//         padding:填充\n"
                            "// 功能概要:进行卷积操作，填充输入，随后做卷积操作\n"
                            "//=====================================================================\n")
                    f.write("#define CONV2D(input, output, kernel, bias, strides, padding)                                                           \\\n"
                            "\t{                                                                                                                   \\\n"
                            "\t\tint pad_top = 0, pad_bottom = 0, pad_left = 0, pad_right = 0;                                                \\\n"
                            "\t\tint pad_along_height = 0, pad_along_width = 0;    \\\n"
                            "\t\tif(strcmp(padding, \"valid\") == 0) {                                                           	                \\\n"
                            "\t\t\tpad_top = pad_bottom = pad_left = pad_right = 0;                                          		            \\\n"
                            "\t\t} else if(strcmp(padding, \"same\") == 0) {                                                    		            \\\n"
                            "\t\t\tpad_along_height = max((GETLENGTH(*output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(*input), 0); \\\n"
                            "\t\t\tpad_along_width = max((GETLENGTH(**output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(**input), 0);  \\\n"
                            "\t\t\tpad_top = pad_along_height / 2;                                                                             \\\n"
                            "\t\t\tpad_bottom = pad_along_height - pad_top;                                                                    \\\n"
                            "\t\t\tpad_left = pad_along_width / 2;                                                                             \\\n"
                            "\t\t\tpad_right = pad_along_width - pad_left;                                                                     \\\n"
                            "\t\t}                                                                                                               \\\n"
                            "\t\tfloat padded[GETLENGTH(input)][(GETLENGTH(*input) + pad_along_height)][(GETLENGTH(**input) + pad_along_width)]; \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                                                                    \\\n"
                            "\t\t\tData_Padding(input[i], padded[i], pad_top, pad_right, pad_bottom, pad_left);                                   \\\n"
                            "\t\tFOREACH(x, GETLENGTH(kernel))                                                                                   \\\n"
                            "\t\t\tFOREACH(y, GETLENGTH(*kernel))                                                                                  \\\n"
                            "\t\t\t\tCONVOLUTE_VALID(padded[x], output[y], kernel[x][y], strides);                                                  \\\n"
                            "\t\tFOREACH(j, GETLENGTH(output))                                                                                  \\\n"
                            "\t\t\tFOREACH(i, GETCOUNT(output[j]))                                                                                 \\\n"
                            "\t\t\t\t((float *)output[j])[i] = ((float *)output[j])[i] + bias[j];                                                    \\\n"
                            "\t}\n\n")
                    
                    # DEPTHWISE_CONV2D宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:DEPTHWISE_CONV2D\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//\t\t  output:输出层元素数组首地址指针\n"
                            "//        kernel:输入层与输出层之间权值数组指针\n"
                            "//          bias:输入层与输出层之间偏置数组指针\n"
                            "//        strides:步长\n"
                            "// 功能概要:进行卷积操作，填充输入，随后坐卷积操作\n"
                            "//=====================================================================\n")
                    f.write("#define DEPTHWISE_CONV2D(input, output, kernel, bias, strides)                                                          \\\n"
                            "\t{                                                                                                                   \\\n"
                            "\t\tint pad_along_height = max((GETLENGTH(*output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(*input), 0);    \\\n"
                            "\t\tint pad_along_width = max((GETLENGTH(**output) - 1) * strides + GETLENGTH(**kernel) - GETLENGTH(**input), 0);     \\\n"
                            "\t\tint pad_top = pad_along_height / 2;                                                                             \\\n"
                            "\t\tint pad_bottom = pad_along_height - pad_top;                                                                    \\\n"
                            "\t\tint pad_left = pad_along_width / 2;                                                                             \\\n"
                            "\t\tint pad_right = pad_along_width - pad_left;                                                                     \\\n"
                            "\t\tfloat padding[GETLENGTH(input)][(GETLENGTH(*input) + pad_along_height)][(GETLENGTH(**input) + pad_along_width)]; \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                                                                    \\\n"
                            "\t\t\tData_Padding(input[i], padding[i], pad_top, pad_right, pad_bottom, pad_left);                               \\\n"
                            "\t\tFOREACH(x, GETLENGTH(kernel))                                                                                   \\\n"
                            "\t\t\tDEPTHWISE_CONVOLUTE_VALID(padding[x], output[x], kernel[x][0], strides);                                                  \\\n"
                            "\t\tFOREACH(j, GETLENGTH(output))                                                                                   \\\n"
                            "\t\t\tFOREACH(i, GETCOUNT(output[j]))                                                                                 \\\n"
                            "\t\t\t\t((float *)output[j])[i] = ((float *)output[j])[i] + bias[j];                                                    \\\n"
                            "\t}\n\n")
                    
                    # BATCH_NORMALIZATION宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:BATCH_NORMALIZATION\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组指针，output:输出元素数组指针\n"
                            "// 数据：eps：增加到方差中的小浮动，以避免被零整除\n"
                            "//     momentum：移动到平均值和移动方差的动量\n"
                            "//     bnParam  0-gamma  1-beta 2-move_mean 3 -move_var\n"
                            "// 功能概要:批量归一化处理\n"
                            "//=====================================================================\n")
                    f.write("#define BATCH_NORMALIZATION(input, bnParam)                                                          \\\n"
                            "\t{                                                                                                \\\n"
                            "\t\tfloat eps = 0.001;                                                                           \\\n"
                            "\t\tfloat beta[GETLENGTH(*bnParam)];                                                             \\\n"
                            "\t\tfloat gamma[GETLENGTH(*bnParam)];                                                            \\\n"
                            "\t\tfloat move_mean[GETLENGTH(*bnParam)];                                                        \\\n"
                            "\t\tfloat move_var[GETLENGTH(*bnParam)];                                                         \\\n"
                            "\t\tfloat x_normed[GETLENGTH(input)][GETLENGTH(*input)][GETLENGTH(**input)];                     \\\n"
                            "\t\tFOREACH(w, GETLENGTH(*bnParam))                                                              \\\n"
                            "\t\t{                                                                                            \\\n"
                            "\t\t\t(beta)[w] = (bnParam)[1][w];                                                             \\\n"
                            "\t\t\t(gamma)[w] = (bnParam)[0][w];                                                            \\\n"
                            "\t\t\t(move_mean)[w] = (bnParam)[2][w];                                                        \\\n"
                            "\t\t\t(move_var)[w] = (bnParam)[3][w];                                                         \\\n"
                            "\t\t}                                                                                            \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                                                 \\\n"
                            "\t\t\tFOREACH(j, GETLENGTH(*input))                                                                \\\n"
                            "\t\t\t\tFOREACH(k, GETLENGTH(**input))                                                               \\\n"
                            "\t\t\t\t{                                                                                            \\\n"
                            "\t\t\t\t\t(x_normed)[i][j][k] = ((input)[i][j][k] - (move_mean)[i]) / (sqrt((move_var)[i] + eps)); \\\n"
                            "\t\t\t\t\t(input)[i][j][k] = gamma[i] * (x_normed)[i][j][k] + (beta)[i];                           \\\n"
                            "\t\t\t\t}                                                                                            \\\n"
                            "\t}\n\n")
                    
                    # ACTIVATION宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:ACTIVATION\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组指针\n"
                            "//         Active_Fun：激活函数\n"
                            "// 功能概要:激活函数\n"
                            "//=====================================================================\n")
                    f.write("#define ACTIVATION(input, Active_Fun)                                                \\\n"
                            "\t{                                                                                \\\n"
                            "\t\tFOREACH(j, GETLENGTH(input))                                                 \\\n"
                            "\t\t\tFOREACH(i, GETCOUNT(input[j]))                                               \\\n"
                            "\t\t\t\t((float *)input[j])[i] = Active_Fun(((float *)input[j])[i]);                 \\\n"
                            "\t}\n\n")
                    
                    # SOFTMAX宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:SOFTMAX\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组指针\n"
                            "// 功能概要:softmax激活函数\n"
                            "//=====================================================================\n")
                    f.write("#define SOFTMAX(input)                                                                 \\\n"
                            "\t{                                                                                   \\\n"
                            "\t\tfloat exparr[GETLENGTH(input)];                                                 \\\n"
                            "\t\tfloat expsum = 0;                                                               \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                                   \\\n"
                            "\t\t{                                                                               \\\n"
                            "\t\t\texparr[i] = (float)exp((input)[i][0][0]);                                   \\\n"
                            "\t\t\texpsum += exparr[i];                                                         \\\n"
                            "\t\t}                                                                               \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                                   \\\n"
                            "\t\t\t(input)[i][0][0] = exparr[i] / expsum;                                           \\\n"
                            "\t}\n\n")
                    
                    # GLOBALAVERAGEPOOLING宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:GLOBALAVERAGEPOOLING\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//\t\t   output:输出层元素数组首地址指针\n"
                            "// 功能概要:全局平均池化 对最后一层卷积的特征图，每个通道求整个特征图的均值\n"
                            "//=====================================================================\n")
                    f.write("#define GLOBALAVERAGEPOOLING(input, output)                              \\\n"
                            "\t{                                                                    \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input))                                     \\\n"
                            "\t\t{                                                                \\\n"
                            "\t\t\tfloat temp = 0;                                              \\\n"
                            "\t\t\tFOREACH(j, GETLENGTH(*input))                                 \\\n"
                            "\t\t\t\tFOREACH(k, GETLENGTH(**input))                              \\\n"
                            "\t\t\t\t\ttemp += (input)[i][j][k];                            \\\n"
                            "\t\t\t(output)[i] = temp / ((GETLENGTH(*input)) * (GETLENGTH(**input))); \\\n"
                            "\t\t}                                                                \\\n"
                            "\t}\n\n")
                    
                    # ADD宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:ADD\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input1:输入层元素数组首地址指针\n"
                            "//\t\t   input2:输出层元素数组首地址指针\n"
                            "//         output:输出层元素数组首地址指针\n"
                            "// 功能概要:残差连接\n"
                            "//=====================================================================\n")
                    f.write("#define ADD(input1, input2, output)                                     \\\n"
                            "\t{                                                                   \\\n"
                            "\t\tFOREACH(i, GETLENGTH(input1))                                   \\\n"
                            "\t\t\tFOREACH(j, GETLENGTH(*input1))                                  \\\n"
                            "\t\t\t\tFOREACH(k, GETLENGTH(**input1))                                 \\\n"
                            "\t\t\t\t\t(output)[i][j][k] = (input1)[i][j][k] + (input2)[i][j][k];      \\\n"
                            "\t}\n\n")
                    
                    # RESHAPE宏定义
                    f.write("//=====================================================================\n"
                            "// 函数名称:RESHAPE\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入层元素数组首地址指针\n"
                            "//         output:输出层元素数组首地址指针\n"
                            "// 功能概要:变换维度\n"
                            "//=====================================================================\n")
                    f.write("#define RESHAPE(input, output)                                         \\\n"
                            "\t{                                                                 \\\n"
                            "\t\tmemcpy(output, input, GETCOUNT(input) * sizeof(float));         \\\n"
                            "\t}\n\n")
                    
                    # 函数声明
                    f.write("//=====================================================================\n"
                            "// 函数名称:relu6\n"
                            "// 函数返回:激活值\n"
                            "// 参数说明:x:待激活值\n"
                            "// 功能概要:将输出值限制在(0,6)之间\n"
                            "//=====================================================================\n")
                    f.write("float relu6(float x);\n\n")
                    
                    f.write("//=====================================================================\n"
                            "// 函数名称:softmax\n"
                            "// 函数返回:无\n"
                            "// 参数说明:input:输入数组指针, dim:数组维度\n"
                            "// 功能概要:Softmax激活函数\n"
                            "//=====================================================================\n")
                    f.write("void softmax(float *input, int dim);\n\n")
                    
                    # 结束符
                    f.write("#endif /* MODEL_OPS_H */\n")

                    f.write("//===================================================================== \n"
                        f"//文件名称：{model_name_lower}.h \n"
                        "//功能概要：模型驱动构件头文件 \n"
                        "//版    本：V3.0 \n"
                        "//使用芯片：D1-H \n"
                        f"//构件生成时间：{code_generation_time}\n"
                        "//===================================================================== \n"
                        "#ifndef MODEL_H \n"
                        "#define MODEL_H \n\n"
                        f"#define SortNum {str(sort_num)}\n\n")
                    # 向头文件中写入内容
                    for i in range(10):
                        if(i < sort_num):
                            f.write(f'#define SORT{i} "{self.model_labels[i]}"\n')
                        else:
                            f.write(f'#define SORT{i} ""\n')
                    f.write("\n")
                    # 获取图片调整后的高度和宽度
                    resizeHeight = self.config_manager.get("globalSettings.imageSize.height")
                    resizeWidth = self.config_manager.get("globalSettings.imageSize.width")
                    f.write(f"#define RESIZED_IMAGE_HEIGHT {resizeHeight}\n")
                    f.write(f"#define RESIZED_IMAGE_WIDTH {resizeWidth}\n\n")
                    f.write(headerFileContent)

                with open(f"{self.inferenceProjectPath}/06_AlgorithmComponent/{model_name_lower}.c", "a") as f:
                    # 文件注释
                    f.write("//=====================================================================\n"
                            f"// 文件名称：{model_name_lower}.c\n"
                            "// 功能概要：模型驱动构件源文件\n"
                            "// 制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)\n"
                            "// 版    本：2025-12-07  V3.0\n"
                            "// 适用芯片：D1-H\n"
                            "//=====================================================================\n")
                    # 引用头文件
                    f.write(f"#include \"{model_name_lower}.h\"\n"
                            "#include \"stdlib.h\"\n"
                            "#include \"includes.h\"\n\n")
                    # 声明全局变量
                    f.write("// 声明全局变量\n")
                    variable_list = list()
                    for layer_name, layer in model_config["layer_config"].items():
                        if layer["output"] != "g_modelInputImage":
                            variable_list.append((layer["output"], layer["output_shape"]))
                    variable_list = list(dict.fromkeys(variable_list))
                    for var, shape in variable_list:
                        f.write(f"float {var}{''.join(['[' + str(i) + ']' for i in list(shape)])} = {{0}};\n")
                    f.write("\n")
                    # clear函数
                    f.write("//=====================================================================\n"
                            "//函数名称：clear\n"
                            "//函数返回：无\n"
                            "//参数说明：无\n"
                            "//功能概要：将全局变量清空为0\n"
                            "//=====================================================================\n")
                    f.write("void clear()\n")
                    f.write("{\n")
                    for var, shape in variable_list:
                        f.write(f"    memset({var}, 0, {''.join([str(i) + '*' for i in list(shape)])}sizeof(float));\n")
                    f.write("}\n")
                    f.write("\n")
                    # 模型推理函数
                    f.write("//=====================================================================\n"
                            "//函数名称：Model_PredictImage\n"
                            "//函数返回：无\n"
                            "//参数说明：result：保存推理结果\n"
                            "//功能概要：模型推理函数\n"
                            "//=====================================================================\n")
                    f.write("void Model_PredictImage(float *result)\n")
                    f.write("{\n")
                    f.write("    clear();\n\n")
                    for layer_name, layer in model_config["layer_config"].items():
                        layer_class = layer["class_name"]
                        layer_code = self.get_layer_code(layer_class, layer)
                        if layer_code != "":
                            f.write(f"    {layer_code}\n")
                    f.write("    // 将结果赋值给result\n")
                    f.write("    for (int i = 0; i < SortNum; i++)\n"
                            "    {\n"
                            f"        result[i] = {model_config['output']}[i];\n"
                            "    }\n")
                    f.write("}\n")
                    f.write("\n")
                
                with open(f"{self.inferenceProjectPath}/06_AlgorithmComponent/{model_name_lower}.h", "a") as f:
                    f.write("//=====================================================================\n"
                            f"//文件名称：{model_name_lower}.h\n"
                            "//功能概要：模型驱动构件头文件\n"
                            "//制作单位：苏州大学嵌入式系统与物联网研究所(sumcu.suda.edu.cn)\n"
                            "//版    本：2022-07-14  V1.0\n"
                            "//适用芯片：D1\n"
                            f"//构件生成时间：{code_generation_time}\n"
                            "//=====================================================================\n"
                            "\n"
                            "//=====================================================================\n"
                            "//函数名称:Model_PredictImage\n"
                            "//函数返回:无\n"
                            "//参数说明:result:传出参数，存储推理结果\n"
                            "//功能概要:模型推理函数\n"
                            "//=====================================================================\n"
                            "void Model_PredictImage(float *result);\n"
                            "\n"
                            "#endif /* MODEL_H */ \n")
                # 显示成功提示框
                self.ui_manager.show_message_box("提示", "构件生成成功！", "information")
                # 更新状态栏显示：构件生成成功！
                self.ui_manager.show_status_message("构件生成成功！")
            except FileNotFoundError as e: 
                print(e)
                # 显示错误提示框
                self.ui_manager.show_message_box("错误", str(e), "critical")
                
        else:
            # 显示警告提示框
            self.ui_manager.show_message_box("警告", "请先选择终端推理工程！", "warning")

    """
    函数名称：showModelTree
    参数说明：modelPath:字符串，表示模型文件的路径  tree:QTreeWidget对象，表示要显示模型信息的树形结构
    函数返回：无
    功能概要：在树形结构中显示模型信息
    """
    @staticmethod
    def showModelTree(modelPath, tree):
        # 清空树形结构
        tree.clear()
        # 创建树形节点并设置节点文本内容
        modelBasicInfo = QTreeWidgetItem(tree)
        modelBasicInfo.setText(0, '模型基本信息')
        modelBasicStructure = QTreeWidgetItem(tree)
        modelBasicStructure.setText(0, '模型基本结构')
        modelLayerWeight = QTreeWidgetItem(tree)
        modelLayerWeight.setText(0, '模型各层权重')
        modelOptimizerWeight = QTreeWidgetItem(tree)
        modelOptimizerWeight.setText(0, '优化器权重')
        # 初始化模型信息
        model_labels = []
        model_performance = []
        model_weights = dict()
        optimizer_weights = dict()
        model_configs = dict()
        # 读取模型文件
        with h5py.File(modelPath, mode='r') as hdf:
            infoGroup = hdf.get("additional_data")
            # 获取模型名称
            try:
                modelName = infoGroup.attrs['model'] if infoGroup is not None else ""
            except (KeyError, AttributeError):
                pass
            # 获取图像类别标签
            try:
                category_data = infoGroup.get('categoryLabels') if infoGroup is not None else None
                if category_data is not None:
                    model_labels = [x.decode('utf-8') for x in list(category_data)]
            except (TypeError, AttributeError):
                pass
            # 获取模型性能信息
            try:
                performance_data = infoGroup.get('performance') if infoGroup is not None else None
                if performance_data is not None:
                    model_performance = [x for x in list(performance_data)]
            except (TypeError, AttributeError):
                pass
            # 获取模型各层权重
            # 查找名为"模型各层权重"的树节点
            layersNode = tree.findItems("模型各层权重", Qt.MatchFlag.MatchRecursive)[0]
            # 遍历模型文件中的所有层名
            for layer_name in hdf['model_weights'].attrs['layer_names']:
                # 创建一个树节点，代表当前层，添加到"模型各层权重"节点下
                item = QTreeWidgetItem(layersNode)
                item.setText(0, layer_name)
                # 获取当前层的所有权重名
                weight_names = hdf['model_weights'][layer_name].attrs['weight_names']
                # 如果当前层有权重
                if weight_names.size:
                    model_weights[layer_name] = dict()
                    # 遍历当前层的所有权重名
                    for weight_name in weight_names:
                        # 在树节点中找到当前层的节点
                        layerItem = tree.findItems(layer_name, Qt.MatchFlag.MatchRecursive)[0]
                        # 创建一个子节点，代表当前权重，添加到当前层节点下
                        childItem = QTreeWidgetItem(layerItem)
                        childItem.setText(0, weight_name)
                        # 获取当前权重的值
                        weight = np.asarray(hdf['model_weights'][layer_name][weight_name])
                        # 存储当前权重的形状和值
                        model_weights[layer_name][weight_name] = (weight.shape, weight)
            # 获取优化器权重
            # 查找名为"优化器权重"的树节点
            optimizerNode = tree.findItems("优化器权重", Qt.MatchFlag.MatchRecursive)[0]
            # 遍历优化器权重名列表
            for optimizer_weight_name in hdf['optimizer_weights'].attrs['weight_names']:
                # 创建一个树节点，代表当前优化器权重，添加到"优化器权重"节点下
                optTreeItem = QTreeWidgetItem(optimizerNode)
                optTreeItem.setText(0, optimizer_weight_name)
                # 获取当前优化器权重的值
                optimizer_weight = np.asarray(hdf['optimizer_weights'][optimizer_weight_name])
                # 存储当前优化器权重的形状和值
                optimizer_weights[optimizer_weight_name] = (optimizer_weight.shape, optimizer_weight)
            # 获取模型各层简要信息
            model_config = hdf.attrs['model_config']
            # 解析模型配置信息中的层信息
            layers_info = json.loads(model_config)['config']['layers']
            # 遍历每个层的配置信息
            for layer in layers_info:
                # 获取层的类名和配置
                class_name = layer['class_name']
                config = layer['config']
                # 将类名添加到配置中
                config['class_name'] = class_name
                # 将配置存储到模型配置字典中，以层名为键
                model_configs[config['name']] = config
        # 发送信号，携带模型标签、性能、权重、优化器权重和模型配置信息
        ComponentGenerateWidget.handleResult(model_labels, model_performance, model_weights, optimizer_weights, model_configs)


    """
    函数名称：handleResult
    参数说明：cls:当前类  model_labels:模型标签列表  model_performance:模型性能列表  model_weights:模型权重字典  optimizer_weights:优化器权重字典  model_configs:模型配置字典
    函数返回：无
    功能概要：处理模型结果并更新类属性
    """
    @classmethod
    def handleResult(cls, model_labels, model_performance, model_weights, optimizer_weights, model_configs):
        # 更新类的属性为传入的参数值
        cls.model_labels = model_labels
        cls.model_performance = model_performance
        cls.model_weights = model_weights
        cls.optimizer_weights = optimizer_weights
        cls.model_configs = model_configs
        # 启用生成构件按钮
        cls.enableButton()
            
    """
    函数名称：showModelLayerWeight
    参数说明：info:包含权重信息的元组，格式为(shape,weight) textEdit:QTextEdit对象，表示要显示权重的文本编辑框
    函数返回：无
    功能概要：在文本编辑框中显示模型各层具体权重
    """
    @staticmethod
    def showModelLayerWeight(info: tuple, textEdit):
        # 获取权重形状
        weight_shape = info[0]
        # 获取权重值
        weight = info[1]
        # 将文本编辑框的文本设置为构造的文本行
        textEdit.setText(f'Shape:{weight_shape}\nWeight:\n{weight}')

    """
    函数名称：showModelStructureDictInfo
    参数说明：info:字典，表示要显示的模型结构字典信息 textEdit:QTextEdit对象，表示要显示信息的文本编辑框
    函数返回：无
    功能概要：在文本编辑框中显示模型各层简要信息
    """
    @staticmethod
    def showModelStructureDictInfo(info: dict, textEdit):
        text = []
        # 计算字典键的最大长度
        maPkey_length = max(len(key) for key in info.keys())
        # 计算值的最大长度
        maPvalue_length = max(len(str(value)) for value in info.values())
        # 遍历字典，构造每一行的文本
        for k, v in info.items():
            key_padding = maPkey_length - len(k)
            value_padding = maPvalue_length - len(str(v))
            text.append(f"{k}: {' ' * key_padding}{v}{' ' * value_padding}")
        # 将文本编辑框的文本设置为构造的文本行，并以换行符连接
        textEdit.setText('\n'.join(text))

    """
    函数名称：showModelBasicInfo
    参数说明：labels:包含模型标签的列表  performance:包含模型性能的列表，格式为[test_loss, test_accuracy] textEdit:QTextEdit对象，表示要显示信息的文本编辑框
    函数返回：无
    功能概要：在文本编辑框中显示模型基本信息
    """
    @staticmethod
    def showModelBasicInfo(labels, performance, textEdit):
        info = []
        # 如果存在模型标签，则添加到信息列表中
        if labels:
            info.append(f"Label: {',  '.join(labels)}")
        else:
            info.append("未解析到Label.")
        # 如果存在模型性能，则添加到信息列表中
        if performance:
            info.append(f"test loss: {performance[0]:.4f}  test accuracy: {performance[1]*100:.4f}%")
        else:
            info.append("未解析到test loss 和 test accuracy.")
        # 将信息列表中的元素以换行符连接，并设置到文本编辑框中
        textEdit.setText('\n'.join(info))

    """
    函数名称：get_sort_index
    参数说明：key:权重名称字符串  sort_order:包含排序子字符串的列表
    函数返回：权重名称中子字符串的位置索引，如果没有匹配则返回排序列表长度
    功能概要：根据权重名称排序
    """
    @staticmethod
    def get_sort_index(key, sort_order):
        # 遍历sort_order列表
        for index, substring in enumerate(sort_order):
            # 若sort_order中包含key，则返回key所在的索引值
            if substring in key:
                return index
        # 如果没有匹配则返回排序列表长度
        return len(sort_order)


    """
    函数名称：numpyArrayToCArray
    参数说明：array: NumPy四维数组
    函数返回：C数组字符串
    功能概要：将NumPy数组转换为C数组字符串
    """
    @staticmethod
    def numpyArrayToCArray(array):
        # 初始化C数组字符串
        c_array_str = "{\n"
        # 遍历NumPy数组第0维度
        for i in range(array.shape[0]):
            c_array_str += "    {\n"
            # 遍历NumPy数组第1维度
            for j in range(array.shape[1]):
                c_array_str += "        {\n"
                # 遍历NumPy数组第2维度
                for k in range(array.shape[2]):
                    c_array_str += "            {"
                    # 遍历NumPy数组第3维度
                    for l in range(array.shape[3]):
                        c_array_str += "%s, " % array[i][j][k][l]
                    c_array_str = c_array_str.rstrip(", ")
                    c_array_str += "},\n"
                c_array_str += "        },\n"
            c_array_str += "    },\n"
        c_array_str += "};"
        return c_array_str



