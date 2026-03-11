from .constants import TOOLTIPS


def tooltip_html(name: str) -> str:
    """Return an HTML span for a criterion name, with a tooltip if available."""
    tip = TOOLTIPS.get(name, "")
    base_style = "font-size:14px;font-weight:600;color:#1a1a1a;"

    if tip:
        return (
            f'<span class="tooltip-wrap" style="{base_style}">'
            f"{name}"
            f'<span class="tooltip-box">{tip}</span>'
            f"</span>"
        )
    return f'<span style="{base_style}">{name}</span>'
