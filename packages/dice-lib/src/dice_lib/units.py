from __future__ import annotations


def convert_to_largest_unit(
    value: float, unit: str, scale: float = 1000.0
) -> tuple[float, str]:
    """Converts value to largest unit of the same type.
    Largest unit is the largest unit where value < scale

    E.g.
        with scale = 1000.0, unit='m' and value=1.0:
        1.0 m -> 1.0 m

        with scale = 1000.0, unit='m' and value=231234.0:
        231234.0 m -> 231.234 km

    """
    prefixes = ["", "k", "M", "G", "T", "P", "E", "Z", "Y"]
    current_scale = value
    prefix_index = 0
    for i, _ in enumerate(prefixes):
        if current_scale < scale:
            prefix_index = i
            break
        current_scale /= scale
    return current_scale, prefixes[prefix_index] + unit
