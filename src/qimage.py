import importlib
from typing import Optional

from PySide6.QtCore import QObject, Signal


class QMemeImage(QObject):
    finished = Signal(object)
    update_state = Signal(bool)
    error_handler = Signal(Exception)

    def __init__(self, file_path: str, title_text: str, subtitle_text: Optional[str] = None):
        super().__init__()
        self.file_path = file_path
        self.title_text = title_text
        self.subtitle_text = subtitle_text

    def generateMeme(self) -> None:
        try:
            self.update_state.emit(True)
            image_module = importlib.import_module(".image", "src")
            image = image_module.ImageCreation(self.file_path, self.title_text, self.subtitle_text).generate_image()
            self.finished.emit(image)
        except Exception as e:
            self.error_handler.emit(e)
        finally:
            self.update_state.emit(False)