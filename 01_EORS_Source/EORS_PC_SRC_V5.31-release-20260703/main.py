import sys
from PySide6.QtWidgets import QApplication
import os
if sys.stdout is None:
    sys.stdout = open(os.devnull, "w")
# 标准错误流重定向
if sys.stderr is None:
    sys.stderr = open(os.devnull, "w")

# 确保服务总线初始化
from P06_Utils.services_bus import service_initializer
from P08_Activity.main_window import MainWindow

def main():
    app = QApplication(sys.argv)
    window = MainWindow()

    service_initializer.initialize_services()
    # 如果python文件打包成exe文件，sys模块会多出frozen属性
    if hasattr(sys, 'frozen'):
    #     pyi_splash模块控制Python闪屏
        import pyi_splash
    #     关闭应用程序启动画面（闪屏）
        pyi_splash.close()

    window.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
    
    
