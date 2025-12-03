import json

from PIL import Image
from PySide6.QtWidgets import QDialog, QWidget, QFrame, QPushButton, QLabel, QMessageBox, QFileDialog
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt, QSize, QRect, QThread

from .qss import get_qss


class ImagePreviewWindow(QDialog):
    def __init__(self, image: Image.Image, parent: QWidget = None):
        super().__init__(parent=parent)
        self.image = image
        self.msg_box = QMessageBox()
        self.qss = get_qss()
        self.initializeUI()

    def initializeUI(self):
        self.setFixedSize(QSize(340, 370))
        self.setWindowTitle("Demotivational Poster Maker - preview")
        self.setUpWindow()

    def setUpWindow(self):
        self.frame = QFrame(self)
        self.frame.setGeometry(QRect(20, 20, 300, 330))
        self.frame.setFrameShape(QFrame.Shape.StyledPanel)
        self.frame.setStyleSheet(self.qss.get("QFrame"))

        self.meme_label = QLabel(self.frame)
        self.meme_label.setGeometry(QRect(20, 20, 260, 260))
        self.meme_label.setStyleSheet(self.qss.get("QLabel"))
        self.meme_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        width = 256 / (self.image.height / self.image.width) if self.image.width < self.image.height else 256
        height = 256 / (self.image.width / self.image.height) if self.image.width > self.image.height else 256

        qimage = self.image.toqpixmap()
        self.meme_label.setPixmap(QPixmap(qimage).scaled(QSize(width, height), mode=Qt.TransformationMode.SmoothTransformation))

        self.download_button = QPushButton("Download", self.frame)
        self.download_button.setGeometry(QRect(30, 290, 110, 24))
        self.download_button.setStyleSheet(self.qss.get("QPushButton"))
        self.download_button.clicked.connect(self.downloadButtonPressed)

        self.show_button = QPushButton("Show image", self.frame)
        self.show_button.setGeometry(QRect(160, 290, 110, 24))
        self.show_button.setStyleSheet(self.qss.get("QPushButton"))
        self.show_button.clicked.connect(self.showButtonPressed)

    def downloadButtonPressed(self):
        save_path = QFileDialog.getSaveFileName(
            parent=self,
            caption="Save file as",
            filter="Image File (*.png *.jpg *.jpeg *.webp)"
        )[0]
        if save_path:
            self.image.save(save_path)
            self.msg_box.information(self, "Download", "Image successfully downloaded!")

    def showButtonPressed(self):
        self.show_thread = QThread()
        self.show_thread.started.connect(self.showImage)
        self.show_thread.finished.connect(self.show_thread.deleteLater)
        self.show_thread.start()

    def showImage(self):
        self.image.show()
        self.show_thread.quit()