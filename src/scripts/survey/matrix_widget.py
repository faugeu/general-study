import streamlit as st
from .constants import SAATY_OPTIONS
from .tooltip import tooltip_html


def _get_default_value(matrix_key: str, pair: tuple) -> int:
    """
    Get default slider value for a pair from example data.
    Returns slider position (-9 to 9), defaulting to 1 if not in example mode.
    """
    # Check if we have example survey data
    example_data = st.session_state.get("ahp_matrices", {})

    if not example_data or matrix_key not in example_data:
        return 1  # Default: equal importance

    # Get the comparison value (e.g., 2.0, 0.5, etc.)
    comparison_val = example_data[matrix_key].get(pair, 1.0)

    # Convert to slider position
    if comparison_val >= 1:
        slider_pos = int(comparison_val)
    else:
        # Reciprocal: 0.5 → -2, 0.33 → -3, etc.
        slider_pos = -int(round(1 / comparison_val))

    # Clamp to valid range
    slider_pos = max(-9, min(9, slider_pos))
    if slider_pos == 0:
        slider_pos = 1

    return slider_pos


def render_pairs(matrix: dict, container) -> dict:
    """
    Render all pairwise-comparison rows for a single AHP matrix.
    Now supports prefilled example values.
    """
    results = {}
    pairs = matrix["pairs"]
    key_prefix = matrix["key"]

    with container:
        for i, (a, b) in enumerate(pairs):
            radio_key = f"{key_prefix}_{i}_side"
            scale_key = f"{key_prefix}_{i}_scale"

            # Get default slider value from example data
            default_slider = _get_default_value(key_prefix, (a, b))

            # Determine which criterion is preferred by default
            default_chosen_index = 0 if default_slider > 0 else 1
            default_scale = abs(default_slider)

            c_left, c_right = st.columns([0.5, 0.9], gap="small")

            with c_left:
                chosen = st.radio(
                    "prefer",
                    options=[a, b],
                    index=default_chosen_index,  # ← Prefilled!
                    key=radio_key,
                    label_visibility="collapsed",
                    horizontal=False,
                )

                # Overlay styled labels
                _wrap = (
                    '<div style="position:relative;margin-top:-85px;'
                    'padding-left:50px;pointer-events:none;">'
                )
                st.markdown(
                    f"""
                    <style>
                    div[data-testid="stRadio"] p {{
                        color: transparent !important;
                        user-select: none;
                        pointer-events: none;
                    }}
                    div[data-testid="stRadio"] > div > label {{
                        align-items: center !important;
                        min-height: 35px !important;
                        padding: 4px 0 !important;
                    }}
                    </style>
                    {_wrap}
                      <div style="height:3px"></div>
                      <div style="height:12px;display:flex;align-items:center;pointer-events:all;">
                        {tooltip_html(a)}
                      </div>
                      <div style="height:8px"></div>
                      <div style="height:42px;display:flex;align-items:center;pointer-events:all;">
                        {tooltip_html(b)}
                      </div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

            with c_right:
                st.markdown('<div style="height:10px"></div>', unsafe_allow_html=True)
                scale = st.select_slider(
                    "Intensity",
                    options=SAATY_OPTIONS,
                    value=default_scale,  # ← Prefilled!
                    key=scale_key,
                    label_visibility="collapsed",
                    format_func=str,
                )

            # Calculate final comparison value
            value = (
                float(scale)
                if chosen == a
                else (1.0 / float(scale) if scale != 0 else 1.0)
            )
            results[(a, b)] = value

    return results


def render_matrix(matrix: dict, container) -> dict:
    """Render the title + pairs for one matrix block. Returns pair results."""
    with container:
        st.markdown(
            f'<div class="matrix-title">{matrix["title"]}</div>',
            unsafe_allow_html=True,
        )
    return render_pairs(matrix, container)
