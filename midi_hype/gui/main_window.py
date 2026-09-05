from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QLabel,
    QListWidget,
    QListWidgetItem,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QSplitter,
    QVBoxLayout,
    QWidget,
)

from midi_hype.core.dump_session import DumpSession, write_dump
from midi_hype.core.formatting import format_dump
from midi_hype.core.models import DeviceConfig
from midi_hype.devices.registry import DEVICES, DEVICE_REGISTRY
from midi_hype.gui.device_forms import DeviceForm
from midi_hype.gui.dump_preview import DumpPreview
from midi_hype.gui.update_dialog import UpdateDialog
from midi_hype.updates.github_releases import GitHubReleaseClient, is_newer_version
from midi_hype.version import __version__


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle(f"MIDI Hype {__version__}")
        self.resize(1100, 700)
        self.session = DumpSession()
        self.current_form: DeviceForm | None = None

        self.device_list = QListWidget(self)
        for spec in DEVICES:
            item = QListWidgetItem(spec.name)
            item.setData(Qt.ItemDataRole.UserRole, spec.key)
            self.device_list.addItem(item)
        self.device_list.currentRowChanged.connect(self._on_device_changed)

        self.form_container = QWidget(self)
        self.form_layout = QVBoxLayout(self.form_container)
        self.form_layout.addWidget(QLabel("Выберите устройство", self.form_container))
        self.form_layout.addStretch(1)

        self.config_list = QListWidget(self)
        self.preview = DumpPreview(self)

        add_button = QPushButton("Добавить устройство", self)
        add_button.clicked.connect(self._add_device)
        remove_button = QPushButton("Удалить", self)
        remove_button.clicked.connect(self._remove_selected)
        up_button = QPushButton("Выше", self)
        up_button.clicked.connect(lambda: self._move_selected(-1))
        down_button = QPushButton("Ниже", self)
        down_button.clicked.connect(lambda: self._move_selected(1))
        generate_button = QPushButton("Сгенерировать dump", self)
        generate_button.clicked.connect(self._refresh_preview)
        copy_button = QPushButton("Копировать", self)
        copy_button.clicked.connect(self._copy_dump)
        save_button = QPushButton("Сохранить", self)
        save_button.clicked.connect(self._save_dump)
        update_button = QPushButton("Проверить обновления", self)
        update_button.clicked.connect(self._check_updates)

        left = QWidget(self)
        left_layout = QVBoxLayout(left)
        left_layout.addWidget(QLabel("Устройства", left))
        left_layout.addWidget(self.device_list)
        left_layout.addWidget(add_button)
        left_layout.addWidget(self.form_container)

        right = QWidget(self)
        right_layout = QVBoxLayout(right)
        right_layout.addWidget(QLabel("Порядок вывода", right))
        right_layout.addWidget(self.config_list)
        order_buttons = QHBoxLayout()
        order_buttons.addWidget(remove_button)
        order_buttons.addWidget(up_button)
        order_buttons.addWidget(down_button)
        right_layout.addLayout(order_buttons)
        right_layout.addWidget(self.preview)
        action_buttons = QHBoxLayout()
        action_buttons.addWidget(generate_button)
        action_buttons.addWidget(copy_button)
        action_buttons.addWidget(save_button)
        action_buttons.addWidget(update_button)
        right_layout.addLayout(action_buttons)

        splitter = QSplitter(self)
        splitter.addWidget(left)
        splitter.addWidget(right)
        splitter.setStretchFactor(0, 1)
        splitter.setStretchFactor(1, 2)
        self.setCentralWidget(splitter)

        if self.device_list.count():
            self.device_list.setCurrentRow(0)

    def _on_device_changed(self, row: int) -> None:
        while self.form_layout.count():
            item = self.form_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
        if row < 0:
            self.current_form = None
            return
        key = self.device_list.item(row).data(Qt.ItemDataRole.UserRole)
        self.current_form = DeviceForm(DEVICE_REGISTRY[key], self.form_container)
        self.form_layout.addWidget(self.current_form)
        self.form_layout.addStretch(1)

    def _add_device(self) -> None:
        item = self.device_list.currentItem()
        if item is None or self.current_form is None:
            return
        key = str(item.data(Qt.ItemDataRole.UserRole))
        spec = DEVICE_REGISTRY[key]
        try:
            values = self.current_form.values()
        except ValueError as exc:
            QMessageBox.warning(self, "Ошибка параметров", str(exc))
            return
        config = DeviceConfig(device_key=key, label=spec.name, parameters=values)
        self.session.add_config(config)
        self._sync_config_list()
        self._refresh_preview()

    def _remove_selected(self) -> None:
        row = self.config_list.currentRow()
        if row >= 0:
            self.session.remove_config(row)
            self._sync_config_list()
            self._refresh_preview()

    def _move_selected(self, direction: int) -> None:
        row = self.config_list.currentRow()
        if row >= 0:
            self.session.move_config(row, direction)
            self._sync_config_list()
            self.config_list.setCurrentRow(max(0, min(row + direction, self.config_list.count() - 1)))
            self._refresh_preview()

    def _sync_config_list(self) -> None:
        self.config_list.clear()
        for config in self.session.configs:
            self.config_list.addItem(config.label)

    def _refresh_preview(self) -> None:
        result = self.session.build()
        self.preview.set_text(format_dump(result.messages))

    def _copy_dump(self) -> None:
        text = self.preview.text()
        QApplication.clipboard().setText(text)
        QMessageBox.information(self, "Готово", "Dump скопирован в буфер обмена.")

    def _save_dump(self) -> None:
        default_path = str(Path.home() / "Desktop" / "dump.txt")
        path, _ = QFileDialog.getSaveFileName(self, "Сохранить dump", default_path, "Text files (*.txt);;All files (*)")
        if path:
            write_dump(Path(path), self.preview.text())
            QMessageBox.information(self, "Готово", f"Dump сохранён в {path}")

    def _check_updates(self) -> None:
        client = GitHubReleaseClient()
        try:
            latest = client.fetch_latest_release()
            release = latest if is_newer_version(latest.version, __version__) else None
            UpdateDialog(release, parent=self).exec()
        except Exception as exc:
            UpdateDialog(None, error=str(exc), parent=self).exec()
