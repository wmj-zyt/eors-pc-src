from keras.callbacks import Callback
from P06_Utils.services_bus.ui_manager import UIManager
from P06_Utils.services_bus.services_bus import ServiceID, service_bus

"""
类名：CustomCallback
基类：Callback：用于构建新回调的基类
功能：自定义回调函数
"""
class CustomCallback(Callback):

    """
    函数名称：__init__
    参数说明：window:应用程序对象 chart:界面图表组件
    函数返回：无
    功能概要：初始化模型训练Loss曲线和Accuracy曲线、模型测试Loss曲线和Accuracy曲线
    """
    def __init__(self, chart):
        super(CustomCallback, self).__init__()

        self.ui_manager: UIManager = service_bus.get_service(ServiceID.UI_MANAGER)
        self.seriesTrainLoss = chart.seriesTrainLoss
        self.seriesTrainAcc = chart.seriesTrainAcc
        self.seriesTestLoss = chart.seriesTestLoss
        self.seriesTestAcc = chart.seriesTestAcc

    """
    函数名称：on_train_begin
    参数说明：logs:字典类型，训练开始时的聚合度量结果。
    函数返回：无
    功能概要：在训练开始时调用
    """
    def on_train_begin(self, logs=None):
        # 模型训练信息框中显示"开始训练"文本
        self.ui_manager.update_training_info("train_info", ("开始训练\n", False))
        # 设置进度条为0%
        self.ui_manager.update_training_info("progress", 0)


    """
    函数名称：on_train_end
    参数说明：logs:字典类型，训练结束时的聚合度量结果。
    函数返回：无
    功能概要：在训练结束时调用
    """
    def on_train_end(self, logs=None):
        # 模型训练信息框中显示"训练结束"文本
        self.ui_manager.update_training_info("train_info", ("训练结束\n", False))
        # 设置进度条为100%
        self.ui_manager.update_training_info("progress", 100)
    
    """
    函数名称：on_train_batch_end
    参数说明：batch:整数类型，当前批次的索引。 logs:字典类型，此批次之前的聚合度量结果。
    函数返回：无
    功能概要：在拟合方法中的一批数据集训练结束时调用
    """
    def on_train_batch_end(self, batch, logs=None):
        # 模型训练信息框中显示当前训练的loss值和accuracy值
        self.ui_manager.update_training_info("train_info", (f'{(batch+1)}/{self.total_batches} [' +
                               f'{"=" * int(((batch + 1) / self.total_batches) * 16)}>' +
                               f'{"-" * int(16 - (((batch + 1) / self.total_batches) * 16))}] - loss: {logs["loss"]:.4f} - accuracy: {logs["accuracy"]:.4f}\n', batch != 0))
        # 设置进度条当前进度值
        self.ui_manager.update_training_info("progress", round((100/self.params["epochs"])*self.epoch + (100/self.params["epochs"])/self.total_batches * (batch+1)))
    """
    函数名称：on_epoch_begin
    参数说明：epoch:整数类型，轮数索引。logs:字典类型，本轮训练开始时的聚合度量结果。
    函数返回：无
    功能概要：在每轮训练开始时调用
    """
    def on_epoch_begin(self, epoch, logs=None):
        # 获取本轮训练中的batch总数
        self.total_batches = self.params["steps"]
        # 获取当前轮数索引
        self.epoch = epoch
        # 模型训练信息框中显示：当前轮数/总轮数
        self.ui_manager.update_training_info("train_info", (f'Epoch:{epoch+1}/{self.params["epochs"]}\n', False))
    
    """
    函数名称：on_epoch_end
    参数说明：epoch:整数类型，轮数索引。logs:字典类型，本轮之前的聚合度量结果。
    函数返回：无
    功能概要：在每轮训练结束时调用
    """
    def on_epoch_end(self, epoch, logs=None):
        # 设置训练loss曲线
        self.seriesTrainLoss.append(epoch+1, logs["loss"])
        # 设置训练accuracy曲线
        self.seriesTrainAcc.append(epoch+1, logs["accuracy"])
        # 设置测试loss曲线
        self.seriesTestLoss.append(epoch+1, self.testLoss)
        # 设置测试accuracy曲线
        self.seriesTestAcc.append(epoch+1, self.testAcc)

    """
    函数名称：on_test_end
    参数说明：logs:字典类型，本轮测试之前的聚合度量结果。
    函数返回：无
    功能概要：在评估或验证结束时调用
    """
    def on_test_end(self, logs=None):
        # 获取当前测试loss值
        self.testLoss = logs["loss"]
        # 获取当前测试accuracy值
        self.testAcc = logs["accuracy"]
        self.ui_manager.update_training_info("train_info", (f' - val_loss: {self.testLoss:.4f} - val_accuracy: {self.testAcc:.4f}\n', False))
