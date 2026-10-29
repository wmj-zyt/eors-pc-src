from PySide6.QtCore import QObject, Signal, QIODeviceBase
from PySide6.QtSerialPort import QSerialPort, QSerialPortInfo


"""
类名：SerialPort
基类：QObject:Qt基础类
功能：串口通信封装类，支持端口标识
""" 
class SerialPort(QObject):
    # 定义信号，当接收到数据时发射 - 增加端口名参数
    dataReceived = Signal(str, bytes, name='dataReceived')  # 端口名, 数据

    """
    函数名称：__init__
    参数说明：port_name:串口名称（可选）,parent:父控件（可选）
    函数返回：无
    功能概要：初始化UI组件及绑定响应事件
    """
    def __init__(self, port_name: str = None, parent=None):
        # 调用父类的初始化方法，初始化父类的属性和方法
        super().__init__(parent)
        # 创建一个QSerialPort对象，用于串口通信
        self._serial = QSerialPort()
        # 存储端口名称
        self._port_name = port_name or "未知端口"
        # 绑定串口数据接收信号
        self._serial.readyRead.connect(self._on_ready_read)

    """
    函数名称：openFull
    参数说明：portName:串口号str baudRate: 波特率int dataBits: 数据位int stopBits: 停止位int parity:奇偶校验位int flowControl:流控int
    函数返回：若串口打开成功，返回True 若串口打开失败，返回False 
    功能概要：全参数打开串口
    """
    def openFull(self, portName: str, baudRate: int, dataBits: int, stopBits: int, parity: int, flowControl: int):
        # 设置端口名称标识
        self._port_name = portName
        
        # 设置串口名称
        self._serial.setPortName(portName)
        # 设置串口波特率
        self._serial.setBaudRate(baudRate)
        # 设置串口数据位
        self._serial.setDataBits(dataBits)
        # 设置串口停止位
        self._serial.setStopBits(stopBits)
        # 设置串口校验
        self._serial.setParity(parity)
        # 设置串口流控
        self._serial.setFlowControl(flowControl)
        # 判断串口是否成功打开
        if not self._serial.open(QIODeviceBase.OpenModeFlag.ReadWrite):
            # 串口打开失败，函数返回False
            return False
        # 串口打开成功，返回True
        return True

    """
    函数名称：open
    参数说明：portName:串口号str baudRate: 波特率int
    函数返回：若串口打开成功，返回元组(True,"") 若串口打开失败，返回元组(False,"失败原因") 
    功能概要：简化参数打开串口
    """
    def open(self, portName: str, baudRate: int):
        # 设置端口名称标识
        self._port_name = portName
        
        # 设置串口名称
        self._serial.setPortName(portName)
        # 设置串口波特率
        self._serial.setBaudRate(baudRate)
        # 设置串口8位数据位
        self._serial.setDataBits(QSerialPort.DataBits.Data8)
        # 设置串口1位停止位
        self._serial.setStopBits(QSerialPort.StopBits.OneStop)
        # 设置串口无校验
        self._serial.setParity(QSerialPort.Parity.NoParity)
        # 设置串口无流控
        self._serial.setFlowControl(QSerialPort.FlowControl.NoFlowControl)
        # 判断串口是否成功打开
        if not self._serial.open(QIODeviceBase.OpenModeFlag.ReadWrite):
            # 串口打开失败，发出错误信号
            return False
        # 串口打开成功，返回True及空字符串
        return True

    """
    函数名称：close
    参数说明：无
    函数返回：无
    功能概要：关闭串口
    """
    def close(self):
        # 关闭串口
        if self._serial.isOpen():
            self._serial.close()

    """
    函数名称：write
    参数说明：data:字节类型，待写入串口的数据
    函数返回：无
    功能概要：写数据到串口
    """
    def write(self, data: bytes):
        # 向串口写入数据
        self._serial.write(data)

    """
    函数名称：_on_ready_read
    参数说明：无
    函数返回：无
    功能概要：接收串口收到的数据并发送数据
    """
    def _on_ready_read(self):
        # 获取串口接收到的数据
        data = self._serial.readAll()
        # 发送dataReceived信号，包含端口名和数据
        self.dataReceived.emit(self._port_name, data)

    """
    函数名称：isOpen
    参数说明：无
    函数返回：串口状态 True=打开状态, False=关闭状态
    功能概要：返回串口状态
    """
    def isOpen(self):
        # 返回串口状态
        return True if self._serial.isOpen() else False
