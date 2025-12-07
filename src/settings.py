import json

from PySide6.QtWidgets import (QDialog, QWidget, QFrame, QLabel, 
                               QLineEdit, QDialogButtonBox, QMessageBox)
from PySide6.QtCore import QSize, QRect, Qt

from .qss import get_qss
from .options import change_options


class SettingsWindow(QDialog):
    def __init__(self, options: dict, parent: QWidget = None):
        super().__init__(parent=parent)
        self.options = options
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(QSize(350, 416))
        self.setWindowTitle("Demotivational Poster Maker - settings")
        self.qss = get_qss()
        self.setUpWindow()

    def setUpWindow(self):
        frame = QFrame(self)
        frame.setGeometry(QRect(10, 10, 330, 360))
        frame.setFrameShape(QFrame.Shape.StyledPanel)
        frame.setStyleSheet(self.qss.get("QFrame"))

        labels = ["Mode", "Size", "Background color", "Text color", "Frame color", 
                  "Frame divide by", "Frame width", "Frame padding", "Font family",
                  "Title font size", "Subtitle font size"]
        
        for label_name in labels:
            label = QLabel(f"{label_name}:", frame)
            label.setGeometry(QRect(20, 20 + 30 * labels.index(label_name), 110, 22))
            label.setStyleSheet(self.qss.get("QLabel"))
        
        self.mode_line_edit = QLineEdit(frame)
        self.mode_line_edit.setGeometry(QRect(150, 20, 160, 22))
        self.mode_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.mode_line_edit.setText(str(self.options.get("mode")))

        self.size_line_edit = QLineEdit(frame)
        self.size_line_edit.setGeometry(QRect(150, 50, 160, 22))
        self.size_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.size_line_edit.setText(str(self.options.get("size")).replace("[", "(").replace("]", ")"))

        self.background_color_line_edit = QLineEdit(frame)
        self.background_color_line_edit.setGeometry(QRect(150, 80, 160, 22))
        self.background_color_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.background_color_line_edit.setText(str(self.options.get("background_color")).replace("[", "(").replace("]", ")"))

        self.text_color_line_edit = QLineEdit(frame)
        self.text_color_line_edit.setGeometry(QRect(150, 110, 160, 22))
        self.text_color_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.text_color_line_edit.setText(str(self.options.get("text_color")).replace("[", "(").replace("]", ")"))
        
        self.frame_color_line_edit = QLineEdit(frame)
        self.frame_color_line_edit.setGeometry(QRect(150, 140, 160, 22))
        self.frame_color_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.frame_color_line_edit.setText(str(self.options.get("frame_outline_color")).replace("[", "(").replace("]", ")"))

        self.frame_divide_by_line_edit = QLineEdit(frame)
        self.frame_divide_by_line_edit.setGeometry(QRect(150, 170, 160, 22))
        self.frame_divide_by_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.frame_divide_by_line_edit.setText(str(self.options.get("frame_outline_divide_by")))

        self.frame_width_line_edit = QLineEdit(frame)
        self.frame_width_line_edit.setGeometry(QRect(150, 200, 160, 22))
        self.frame_width_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.frame_width_line_edit.setText(str(self.options.get("frame_outline_width")))

        self.frame_padding_line_edit = QLineEdit(frame)
        self.frame_padding_line_edit.setGeometry(QRect(150, 230, 160, 22))
        self.frame_padding_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.frame_padding_line_edit.setText(str(self.options.get("frame_padding")))

        self.font_family_line_edit = QLineEdit(frame)
        self.font_family_line_edit.setGeometry(QRect(150, 260, 160, 22))
        self.font_family_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.font_family_line_edit.setText(str(self.options.get("font_family")))

        self.title_font_size_line_edit = QLineEdit(frame)
        self.title_font_size_line_edit.setGeometry(QRect(150, 290, 160, 22))
        self.title_font_size_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.title_font_size_line_edit.setText(str(self.options.get("title_font_size")))

        self.subtitle_font_size_line_edit = QLineEdit(frame)
        self.subtitle_font_size_line_edit.setGeometry(QRect(150, 320, 160, 22))
        self.subtitle_font_size_line_edit.setStyleSheet(self.qss.get("QLineEdit"))
        self.subtitle_font_size_line_edit.setText(str(self.options.get("subtitle_font_size")))

        self.button_box = QDialogButtonBox(self)
        self.button_box.setGeometry(QRect(10, 380, 330, 24))
        self.button_box.setStyleSheet(self.qss.get("QDialogButtonBox"))
        self.button_box.setOrientation(Qt.Orientation.Horizontal)
        self.button_box.setStandardButtons(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

    def accept(self):
        try:
            options = {
                "mode": self.mode_line_edit.text(),
                "size": json.loads(self.size_line_edit.text().replace("(", "[").replace(")", "]")),
                "background_color": json.loads(self.background_color_line_edit.text().replace("(", "[").replace(")", "]")),
                "text_color": json.loads(self.text_color_line_edit.text().replace("(", "[").replace(")", "]")),
                "frame_outline_color": json.loads(self.frame_color_line_edit.text().replace("(", "[").replace(")", "]")),
                "frame_outline_divide_by": int(self.frame_divide_by_line_edit.text()),
                "frame_outline_width": int(self.frame_width_line_edit.text()),
                "frame_padding": int(self.frame_padding_line_edit.text()),
                "font_family": self.font_family_line_edit.text(),
                "title_font_size": int(self.title_font_size_line_edit.text()),
                "subtitle_font_size": int(self.subtitle_font_size_line_edit.text())
            }
            change_options(options)
            return super().accept()
        except Exception as e:
            QMessageBox().critical(self, "ERROR", str(e))
    
    def reject(self):
        return super().reject()

    def exec_(self) -> int:
        return self.exec()