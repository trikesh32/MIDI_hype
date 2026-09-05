from __future__ import annotations

from PySide6.QtWidgets import QPlainTextEdit, QWidget, QVBoxLayout


class DumpPreview(QWidget):
    def __init__(self, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.editor = QPlainTextEdit(self)
        self.editor.setReadOnly(True)
        self.editor.setPlaceholderText("Здесь появится MIDI dump в hex-формате")
        layout = QVBoxLayout(self)
        layout.addWidget(self.editor)

    def set_text(self, text: str) -> None:
        self.editor.setPlainText(text)

    def text(self) -> str:
        return self.editor.toPlainText()

