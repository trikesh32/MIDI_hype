from __future__ import annotations

from midi_hype.core.models import ParameterSpec


def validate_parameter(spec: ParameterSpec, value: int) -> int:
    if spec.field_type == "choice":
        allowed = {option.value for option in spec.options}
        if value not in allowed:
            raise ValueError(f"{spec.label}: значение {value} не входит в {sorted(allowed)}")
        return value

    if spec.minimum is not None and value < spec.minimum:
        raise ValueError(f"{spec.label}: значение должно быть >= {spec.minimum}")
    if spec.maximum is not None and value > spec.maximum:
        raise ValueError(f"{spec.label}: значение должно быть <= {spec.maximum}")
    return value


def validate_parameters(specs: tuple[ParameterSpec, ...], values: dict[str, int]) -> dict[str, int]:
    validated: dict[str, int] = {}
    for spec in specs:
        validated[spec.key] = validate_parameter(spec, int(values.get(spec.key, spec.default)))
    return validated

