#导入应用系统和主窗口模块
from PySide6.QtWidgets import QApplication, QMainWindow,QMessageBox
from PySide6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QTextEdit, QMessageBox,
                            QTableWidget, QTableWidgetItem, QHeaderView)
from PySide6.QtCore import Qt
#导入从QT Designer设计转换而来的窗体框架模块

from P07_View.Qt_Designer_ui_py.Ui_AutoDialog import Ui_Dialog


class ParamDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.param_combinations = []   #参数列表【轮次、批量大小、学习率】
        
        self.setup_connections()       #设置信号槽

        self.ui.text_edit.setPlaceholderText("请输入参数组合，每行一组：\n100,16,0.0001\n200,32,0.0002\n300,16,0.0001")
        # 初始化表格
        self.setup_table()

        
    def setup_ui(self):
        """设置UI界面"""
        self.setWindowTitle("自动训练参数设置")
        self.setModal(True)
        self.setFixedSize(600, 400)
        
        # 创建UI实例
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        
    def setup_connections(self):
        """连接信号和槽"""
        self.ui.add_btn.clicked.connect(self.addExampleParams)  #添加示例
        self.ui.clear_btn.clicked.connect(self.clearParams)     #清除
        self.ui.ok_btn.clicked.connect(self.accept)             #点击OK
        self.ui.cancel_btn.clicked.connect(self.reject)         #取消
        self.ui.updata_btn.clicked.connect(self.updatePreview)  #更新参数

        # 🔴 关键：连接表格单元格修改信号
        self.ui.table_widget.cellChanged.connect(self.on_table_cell_changed)

    def setup_table(self):
        """设置表格属性"""
        # 设置表格可编辑
        self.ui.table_widget.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        #隐藏垂直表头
        self.ui.table_widget.verticalHeader().setVisible(False)                  
        # 设置表头
        self.ui.table_widget.setHorizontalHeaderLabels(["序号", "训练轮数", "批量大小", "学习率"])
        
        # 设置列宽
        header = self.ui.table_widget.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeToContents)  # 序号列自适应
        header.setSectionResizeMode(1, QHeaderView.Stretch)  # 训练轮数拉伸
        header.setSectionResizeMode(2, QHeaderView.Stretch)  # 批量大小拉伸
        header.setSectionResizeMode(3, QHeaderView.Stretch)  # 学习率拉伸
        
    def on_table_cell_changed(self, row, column):
        """表格单元格内容修改时的处理"""
        try:
            # 跳过序号列（第0列）
            if column == 0:
                return
                
            # 获取修改后的值
            item = self.ui.table_widget.item(row, column)
            if not item or not item.text().strip():
                return
            new_value = item.text().strip()
        
            # 根据列索引更新对应的参数
            if column == 1:  # 训练轮数列
                try:
                    epochs = int(new_value)
                    if epochs > 0:
                        # 更新参数组合
                        if row < len(self.param_combinations):
                            old_epochs, batchsize, lr = self.param_combinations[row]
                            self.param_combinations[row] = (epochs, batchsize, lr)
                            print(f"更新第{row+1}行训练轮数: {old_epochs} -> {epochs}")
                        self.update_text_edit_from_table()
                except ValueError:
                    QMessageBox.warning(self, "输入错误", f"训练轮数必须是正整数！\n输入值: '{new_value}'\n错误: {str(ValueError)}")
                    # QMessageBox.warning(self, "输入错误", "训练轮数必须是正整数！")
                    # 恢复原值
                    self.update_table_from_params()
                    
            elif column == 2:  # 批量大小列
                try:
                    batchsize = int(new_value)
                    if batchsize > 0:
                        if row < len(self.param_combinations):
                            epochs, old_batchsize, lr = self.param_combinations[row]
                            self.param_combinations[row] = (epochs, batchsize, lr)
                            print(f"更新第{row+1}行批量大小: {old_batchsize} -> {batchsize}")
                        self.update_text_edit_from_table()
                except ValueError:
                    QMessageBox.warning(self, "输入错误", "批量大小必须是正整数！")
                    self.update_table_from_params()
                    
            elif column == 3:  # 学习率列
                try:
                    lr = float(new_value)
                    if lr > 0:
                        if row < len(self.param_combinations):
                            epochs, batchsize, old_lr = self.param_combinations[row]
                            self.param_combinations[row] = (epochs, batchsize, lr)
                            print(f"更新第{row+1}行学习率: {old_lr}-> {lr}")
                        self.update_text_edit_from_table()
                except ValueError:
                    QMessageBox.warning(self, "输入错误", "学习率必须是浮点数！")
                    self.update_table_from_params()
                    
        except Exception as e:
            print(f"表格更新错误: {e}")
            
    def update_text_edit_from_table(self):
        """根据表格内容更新文本编辑框"""
        try:
            # 临时断开信号，避免循环触发
            self.ui.text_edit.blockSignals(True)
            
            text_lines = []
            for i in range(self.ui.table_widget.rowCount()):
                if i >= len(self.param_combinations):
                    break
                    
                epochs_item = self.ui.table_widget.item(i, 1)
                batchsize_item = self.ui.table_widget.item(i, 2)
                lr_item = self.ui.table_widget.item(i, 3)
                
                if epochs_item and batchsize_item and lr_item:
                    epochs = epochs_item.text().strip()
                    batchsize = batchsize_item.text().strip()
                    lr = lr_item.text().strip()
                    
                    if epochs and batchsize and lr:
                        text_lines.append(f"{epochs},{batchsize},{lr}")
            
            # 更新文本编辑框
            self.ui.text_edit.setPlainText("\n".join(text_lines))
            
            # 重新连接信号
            self.ui.text_edit.blockSignals(False)
            
        except Exception as e:
            print(f"更新文本编辑框错误: {e}")
            self.ui.text_edit.blockSignals(False)
            
    def update_table_from_params(self):
        """根据参数组合更新表格（用于恢复数据）"""
        try:
            # 临时断开信号，避免循环触发
            self.ui.table_widget.blockSignals(True)
            
            # 清空表格
            self.ui.table_widget.setRowCount(0)
            
            # 重新填充表格
            for i, (epochs, batchsize, lr) in enumerate(self.param_combinations):
                self.ui.table_widget.insertRow(i)
                
                # 序号
                self.ui.table_widget.setItem(i, 0, QTableWidgetItem(str(i + 1)))
                # 训练轮数
                self.ui.table_widget.setItem(i, 1, QTableWidgetItem(str(epochs)))
                # 批量大小
                self.ui.table_widget.setItem(i, 2, QTableWidgetItem(str(batchsize)))
                # 学习率
                self.ui.table_widget.setItem(i, 3, QTableWidgetItem(str(lr)))
            
            # 重新连接信号
            self.ui.table_widget.blockSignals(False)
            
        except Exception as e:
            print(f"更新表格错误: {e}")
            self.ui.table_widget.blockSignals(False)
            
    def addExampleParams(self):
        """添加示例参数"""
        example_params = """100,16,0.0001
200,16,0.0001
300,16,0.0001
400,16,0.0001
100,32,0.0002
200,32,0.0002
300,32,0.0002"""
        self.ui.text_edit.setPlainText(example_params)
        self.updatePreview()
        
    def clearParams(self):
        """清空参数"""
        self.ui.text_edit.clear()
        self.param_combinations = []
        self.ui.table_widget.setRowCount(0)
        
    def updatePreview(self):
        """更新参数预览"""
        try:
            text = self.ui.text_edit.toPlainText().strip()
            if not text:
                self.param_combinations = []
                self.ui.table_widget.setRowCount(0)
                return
                
            lines = text.split('\n')
            self.param_combinations = []
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                    
                try:
                    parts = line.split(',')
                    if len(parts) == 3:
                        epochs = int(parts[0].strip())
                        batchsize = int(parts[1].strip())
                        lr = float(parts[2].strip())
                        
                        if epochs > 0 and batchsize > 0 and lr > 0:
                            self.param_combinations.append((epochs, batchsize, lr))
                            
                except (ValueError, IndexError):
                    continue
            
            # 更新表格显示
            self.update_table_from_params()
            
        except Exception as e:
            print(f"更新预览错误: {e}")
            
    def on_ok(self):
        """确定按钮点击"""
        # 确保参数组合是最新的
        self.updatePreview()
        
        if not self.param_combinations:
            QMessageBox.warning(self, "警告", "请输入有效的参数组合！")
            return
        
        # 打印最终参数
        print("\n=== 最终参数组合 ===")
        for i, (epochs, batchsize, lr) in enumerate(self.param_combinations):
            print(f"组合{i+1}: 轮数={epochs}, 批量={batchsize}, 学习率={lr}")
        print("==================\n")
        
        self.accept()
        
    def get_params(self):
        """获取参数组合"""
        return self.param_combinations