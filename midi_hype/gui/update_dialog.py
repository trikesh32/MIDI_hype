from __future__ import annotations

import webbrowser

from PySide6.QtWidgets import QDialog, QDialogButtonBox, QLabel, QPushButton, QVBoxLayout, QWidget

from midi_hype.updates.github_releases import ReleaseInfo


class UpdateDialog(QDialog):
    def __init__(self, release: ReleaseInfo | None, error: str | None = None, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.release = release
        self.setWindowTitle("Обновления MIDI Hype")

        layout = QVBoxLayout(self)
        if error:
            layout.addWidget(QLabel(f"Не удалось проверить обновления:\n{error}", self))
        elif release is None:
            layout.addWidget(QLabel("Установлена последняя версия.", self))
        else:
            layout.addWidget(QLabel(f"Доступна версия {release.version}\n\n{release.notes}", self))
            open_button = QPushButton("Открыть релиз", self)
            open_button.clicked.connect(self._open_release)
            layout.addWidget(open_button)

        buttons = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok, self)
        buttons.accepted.connect(self.accept)
        layout.addWidget(buttons)

    def _open_release(self) -> None:
        if self.release:
            webbrowser.open(self.release.url)

