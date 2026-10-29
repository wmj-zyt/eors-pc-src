from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

class CustomCornerWidget(QWidget):
    def __init__(self, text):
        super().__init__()
        self.label = QLabel(text)
        layout = QVBoxLayout(self)
        layout.addWidget(self.label)
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setStyleSheet("QLabel{"
                            "background-color:transparent;"
                            "font-size:16px;"
                            "font-family:Times New Roman,Microsoft YaHei;"
                            "font-weight:bold;"
                            "color:#374557;"
                            "padding-left:20px;"
                            "}")