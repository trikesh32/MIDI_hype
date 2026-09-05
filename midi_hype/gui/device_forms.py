from __future__ import annotations

from PySide6.QtWidgets import QComboBox, QFormLayout, QSpinBox, QWidget

from midi_hype.core.models import DeviceSpec
from midi_hype.core.validation import validate_parameters


class DeviceForm(QWidget):
    def __init__(self, spec: DeviceSpec, parent: QWidget | None = None) -> None:
        super().__init__(parent)
        self.spec = spec
        self._widgets: dict[str, QSpinBox | QComboBox] = {}

        layout = QFormLayout(self)
        for param in spec.parameters:
            if param.field_type == "choice":
                widget = QComboBox(self)
                for option in param.options:
                    widget.addItem(option.label, option.value)
                index = widget.findData(param.default)
                widget.setCurrentIndex(max(index, 0))
            else:
                widget = QSpinBox(self)
                widget.setMinimum(param.minimum if param.minimum is not None else -999_999)
                widget.setMaximum(param.maximum if param.maximum is not None else 999_999)
                widget.setValue(param.default)
            self._widgets[param.key] = widget
            layout.addRow(param.label, widget)

    def values(self) -> dict[str, int]:
        result: dict[str, int] = {}
        for key, widget in self._widgets.items():
            if isinstance(widget, QComboBox):
                result[key] = int(widget.currentData())
            else:
                result[key] = int(widget.value())
        return validate_parameters(self.spec.parameters, result)

