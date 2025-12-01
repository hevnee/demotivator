import sys
import json
from typing import Optional

from PIL import Image
from PySide6.QtWidgets import (QApplication, QWidget, QLabel,
                               QPushButton, QLineEdit, QMessageBox,
                               QGridLayout, QFrame, QFileDialog)
from PySide6.QtCore import QThread, QSize, QRect

from .qss import create_qss
# from settings import SettingsWindow
from .image_preview import ImagePreviewWindow
from .qimage import QMemeImage


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        # self.settings_window = SettingsWindow(self)
        self.msg_box = QMessageBox()
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(QSize(370, 270))
        self.setMinimumSize(QSize(310, 230))
        self.setMaximumSize(QSize(850, 540))
        self.setWindowTitle("Demotivational Poster Maker")
        self.getQSS()
        self.setUpMainWindow()

    def getQSS(self):
        self.qss = dict()
        try:
            with open("qss.json", "r", encoding="utf-8") as file:
                self.qss: dict = json.loads(file.read())
        except FileNotFoundError:
            self.qss = create_qss()
        except Exception as e:
            print(e)

    def setUpMainWindow(self):
        self.grid_layout = QGridLayout(self)

        self.setStyleSheet(self.qss.get("QWidget"))

        self.frame = QFrame(self)
        self.frame.setMinimumSize(QSize(250, 170))
        self.frame.setMaximumSize(QSize(250, 170))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setStyleSheet(self.qss.get("QFrame"))

        self.choose_image_button = QPushButton("Choose Image", self.frame)
        self.choose_image_button.setGeometry(QRect(10, 10, 150, 24))
        self.choose_image_button.setStyleSheet(self.qss.get("QPushButton"))
        self.choose_image_button.clicked.connect(self.chooseImageButtonPressed)

        self.settings_button = QPushButton("Settings", self.frame)
        self.settings_button.setGeometry(QRect(170, 10, 70, 24))
        self.settings_button.setStyleSheet(self.qss.get("QPushButton"))
        self.settings_button.clicked.connect(self.settingsButtonPressed)
        self.settings_button.setDisabled(True)

        self.current_file_path_label = QLabel("", self.frame)
        self.current_file_path_label.setGeometry(QRect(10, 44, 230, 16))
        self.current_file_path_label.setStyleSheet(self.qss.get("QLabel"))

        self.title_text_line_edit = QLineEdit(self.frame)
        self.title_text_line_edit.setGeometry(QRect(10, 70, 230, 24))
        self.title_text_line_edit.setPlaceholderText("Title text")
        self.title_text_line_edit.setStyleSheet(self.qss.get("QLineEdit"))

        self.subtitle_text_line_edit = QLineEdit(self.frame)
        self.subtitle_text_line_edit.setGeometry(QRect(10, 100, 230, 24))
        self.subtitle_text_line_edit.setPlaceholderText("Subtitle text")
        self.subtitle_text_line_edit.setStyleSheet(self.qss.get("QLineEdit"))

        self.generate_button = QPushButton("Generate", self.frame)
        self.generate_button.setGeometry(QRect(10, 136, 110, 24))
        self.generate_button.setStyleSheet(self.qss.get("QPushButton"))
        self.generate_button.clicked.connect(self.generateButtonPressed)

        self.reset_button = QPushButton("Reset", self.frame)
        self.reset_button.setGeometry(QRect(130, 136, 110, 24))
        self.reset_button.setStyleSheet(self.qss.get("QPushButton"))
        self.reset_button.clicked.connect(self.resetButtonPressed)

        self.grid_layout.addWidget(self.frame, 0, 0, 1, 1)

    def chooseImageButtonPressed(self):
        file_path = QFileDialog.getOpenFileName(
            parent=self,
            caption="Select a file",
            filter="Image File (*.png *.jpg *.jpeg *.webp)"
        )[0]
        self.current_file_path_label.setText(file_path)
        self.current_file_path_label.setToolTip(file_path)

    def settingsButtonPressed(self):
        ...
        # self.settings_window.exec()

    def generateButtonPressed(self):
        current_file = self.current_file_path_label.text()
        if current_file == "":
            return self.msg_box.critical(self, "ERROR", "Please choose an image.")

        title_text = self.title_text_line_edit.text()
        if title_text == "":
            return self.msg_box.critical(self, "ERROR", "Please fill in the title text field.")

        subtitle_text = self.subtitle_text_line_edit.text() if self.subtitle_text_line_edit.text() else None

        self.startMemeImageThread(current_file, title_text, subtitle_text)

    def resetButtonPressed(self):
        self.current_file_path_label.setText("")
        self.title_text_line_edit.setText("")
        self.subtitle_text_line_edit.setText("")

    def startMemeImageThread(self, file_path: str, title_text: str, subtitle_text: Optional[str] = None):
        self.image_thread = QThread()
        self.image_worker = QMemeImage(file_path, title_text, subtitle_text)
        self.image_worker.moveToThread(self.image_thread)
        self.image_worker.error_handler.connect(self.imageWorkerErrorHandler)
        self.image_worker.update_state.connect(self.updateWidgetState)
        self.image_worker.finished.connect(self.getMemeImage)
        self.image_thread.started.connect(self.image_worker.generateMeme)
        self.image_worker.finished.connect(self.image_thread.quit)
        self.image_thread.finished.connect(self.image_worker.deleteLater)
        self.image_thread.finished.connect(self.image_thread.deleteLater)
        self.image_thread.start()

    def updateWidgetState(self, value: bool):
        self.choose_image_button.setDisabled(value)
        # self.settings_button.setDisabled(value)
        self.title_text_line_edit.setDisabled(value)
        self.subtitle_text_line_edit.setDisabled(value)
        self.generate_button.setDisabled(value)
        self.reset_button.setDisabled(value)

    def getMemeImage(self, image: Image.Image):
        ImagePreviewWindow(image, self).exec()

    def imageWorkerErrorHandler(self, error: Exception):
        self.msg_box.critical(self, "ERROR", str(error))

    def closeEvent(self, event):
        try:
            self.image_thread.quit()
            self.image_thread.wait()

        except AttributeError:
            pass

        except Exception:
            pass

        return super().closeEvent(event)