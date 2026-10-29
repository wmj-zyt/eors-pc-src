from PySide6.QtCharts import QChart, QValueAxis, QSplineSeries
from PySide6.QtCore import Qt

"""
类名：LossAccChart
基类：QChart:Qt框架中的二维图表类
功能：自定义图表组件
"""
class LossAccChart(QChart):

    """
    函数名称：__init__
    参数说明：title:图标标题
    函数返回：无
    功能概要：初始化自定义图表组件
    """
    def __init__(self, title):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super(LossAccChart, self).__init__()
        # 设置图表标题
        self.setTitle(title)
        # 当前图表是否为空标志，True=图表为空 False=图表非空
        self.empty = True
        # 声明及初始化X轴和Y轴为None
        self.axisX = None
        self.axisYLoss = None
        self.axisYAcc = None


    """
    函数名称：setAxis
    参数说明：type:轴类型str  range:坐标轴范围tuple  title:坐标轴名称str  tickcount:坐标轴主分割数int  position: 坐标轴位置str
    函数返回：无
    功能概要：初始化自定义图表组件
    """
    def setAxis(self, type, range, title, tickcount, position=None):
        # 设置图表不为空
        self.empty = False
        # 设置X坐标轴
        if type == 'x':
            # 实例化X坐标轴
            self.axisX = QValueAxis()
            # 设置X坐标轴范围
            self.axisX.setRange(range[0], range[1]) 
            # 设置X坐标轴标签格式
            self.axisX.setLabelFormat("%d") 
            # 设置X坐标轴主分割数
            self.axisX.setTickCount(tickcount) 
            # 设置X坐标轴标题
            self.axisX.setTitleText(title)
            # 显示背景网格X轴框线
            self.axisX.setGridLineVisible(True)
            # 隐藏X轴次网格线
            self.axisX.setMinorGridLineVisible(False)
            # 将X轴添加到图表下方
            self.addAxis(self.axisX, Qt.AlignBottom)
        # 设置左侧Y坐标轴
        elif type == 'y' and position == 'l':
            # 实例化Y坐标轴
            self.axisYLoss = QValueAxis()
            # 设置左侧Y坐标轴范围
            self.axisYLoss.setRange(range[0], range[1])
            # 设置左侧Y坐标轴标签格式
            self.axisYLoss.setLabelFormat("%.1f")
            # 设置左侧Y坐标轴主分割数
            self.axisYLoss.setTickCount(tickcount)
            # 设置左侧Y坐标轴标题
            self.axisYLoss.setTitleText(title)
            # 隐藏Y轴次网格线
            self.axisYLoss.setMinorGridLineVisible(False)
            # 将Y轴添加到图表左侧
            self.addAxis(self.axisYLoss, Qt.AlignLeft)
        # 设置右侧Y坐标轴
        elif type == 'y' and position == 'r':
            # 实例化Y坐标轴
            self.axisYAcc = QValueAxis()
            # 设置右侧Y坐标轴范围
            self.axisYAcc.setRange(range[0], range[1])
            # 设置右侧Y坐标轴标签格式
            self.axisYAcc.setLabelFormat("%.1f")
            # 设置右侧Y坐标轴主分割数
            self.axisYAcc.setTickCount(tickcount)
            # 设置右侧Y坐标轴标题
            self.axisYAcc.setTitleText(title)
            # 隐藏Y轴次网格线
            self.axisYAcc.setMinorGridLineVisible(False)
            # 将Y轴添加到图表右侧
            self.addAxis(self.axisYAcc, Qt.AlignRight)


    """
    函数名称：setSeries
    参数说明：无
    函数返回：无
    功能概要：设置图表曲线
    """
    def setSeries(self):
        # 实例化训练Loss曲线
        self.seriesTrainLoss = QSplineSeries() 
        # 实例化训练准确率曲线
        self.seriesTrainAcc = QSplineSeries()
        # 实例化验证Loss曲线
        self.seriesTestLoss = QSplineSeries()
        # 实例化验证准确率曲线
        self.seriesTestAcc = QSplineSeries()
        # 设置训练Loss曲线的名称为"training loss"
        # self.seriesTrainLoss.setName("training loss")
        self.seriesTrainLoss.setName("训练损失")
        # 设置训练准确率曲线的名称为"training accuracy"
        # self.seriesTrainAcc.setName("training accuracy")
        self.seriesTrainAcc.setName("训练精确度")
        # 设置验证Loss曲线的名称为"validation loss"
        # self.seriesTestLoss.setName("validation loss")
        self.seriesTestLoss.setName("验证损失")
        # 设置验证准确率曲线的名称为"validation accuracy"
        # self.seriesTestAcc.setName("validation accuracy")
        self.seriesTestAcc.setName("验证精确度")
        # 添加训练Loss曲线到图表中
        self.addSeries(self.seriesTrainLoss)
        # 添加训练准确率曲线到图表中
        self.addSeries(self.seriesTrainAcc)
        # 添加验证Loss曲线到图表中
        self.addSeries(self.seriesTestLoss)
        # 添加验证准确率曲线到图表中
        self.addSeries(self.seriesTestAcc)
        # 将X轴绑定到训练Loss曲线上
        self.setAxisX(self.axisX, self.seriesTrainLoss)
        # 将X轴绑定到训练准确率曲线上
        self.setAxisX(self.axisX, self.seriesTrainAcc)
        # 将X轴绑定到验证Loss曲线上
        self.setAxisX(self.axisX, self.seriesTestLoss)
        # 将X轴绑定到验证准确率曲线上
        self.setAxisX(self.axisX, self.seriesTestAcc)
        # 将Loss的Y轴绑定到训练Loss曲线上
        self.setAxisY(self.axisYLoss, self.seriesTrainLoss)
        # 将Loss的Y轴绑定到验证Loss曲线上
        self.setAxisY(self.axisYLoss, self.seriesTestLoss)
        # 将准确率的Y轴绑定到训练准确率曲线上
        self.setAxisY(self.axisYAcc, self.seriesTrainAcc)
        # 将准确率的Y轴绑定到验证准确率曲线上
        self.setAxisY(self.axisYAcc, self.seriesTestAcc)


    """
    函数名称：clear
    参数说明：无
    函数返回：无
    功能概要：清空图表
    """
    def clear(self):
        # 判读图表是否为空
        if not self.empty:
            # 删除X轴
            self.removeAxis(self.axisX)
            # 删除Y轴
            self.removeAxis(self.axisYAcc)
            self.removeAxis(self.axisYLoss)
            # 删除所有曲线
            self.removeAllSeries()
            # 设置图表为空
            self.empty = True
