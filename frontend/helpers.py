import html
from pathlib import Path

import streamlit as st


def load_css():
    css_path = Path(__file__).parent / "styles" / "style.css"

    if not css_path.exists():
        st.error(f"CSS file was not found: {css_path}")
        return

    css = css_path.read_text(encoding="utf-8")

    st.markdown(
        f"<style>{css}</style>",
        unsafe_allow_html=True,
    )


def initialise_session_state():
    defaults = {
        "genres": [],
        "mood": "",
        "artist": "",
        "recommendations": [],
        "generated_artist": "",
        "feedback_submitted": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value

def reset_inputs():
    st.session_state["genres"] = []
    st.session_state["mood"] = ""
    st.session_state["artist"] = ""
    st.session_state["recommendations"] = []
    st.session_state["generated_artist"] = ""
    st.session_state["feedback_submitted"] = False

def safe_text(value, default="Unknown"):
    if value is None:
        return default

    text = str(value).strip()

    if not text:
        return default

    return html.escape(text)

def format_genre(value):
    """Return a safely escaped, human-readable genre label."""

    cleaned = str(
        value or "Unknown"
    ).strip().lower()

    display_names = {
        "r&b": "R&B",
        "hip hop": "Hip Hop",
        "synthpop": "Synthpop",
    }

    display_value = display_names.get(
        cleaned,
        cleaned.title(),
    )

    return html.escape(
        display_value
    )

def safe_percentage(value):
    try:
        numeric_value = float(value)

        if numeric_value <= 1:
            numeric_value *= 100

        return max(0, min(100, round(numeric_value)))

    except (TypeError, ValueError):
        return 0


def safe_number(value, default=0):
    try:
        return round(float(value))

    except (TypeError, ValueError):
        return default


def shorten_reason(
    reason,
    maximum_length=155,
):
    """Create a concise recommendation explanation for the result card."""

    cleaned_reason = str(
        reason or ""
    ).strip()

    if not cleaned_reason:
        return (
            "Selected using your current genre, mood and artist preferences."
        )

    cleaned_reason = cleaned_reason.replace(
        "Recommended because ",
        "",
        1,
    )

    cleaned_reason = cleaned_reason.rstrip(".")

    replacements = {
        "it matches both your selected genre and labelled mood":
            "matches your selected genre and mood",
        "it matches both your selected genre and mood":
            "matches your selected genre and mood",
        "it matches your selected genre":
            "matches your selected genre",
        "it matches your selected mood while adding genre variety":
            "matches your selected mood while adding genre variety",
        "although its labelled mood differs from your selection":
            "with a different labelled mood",
        "has a high energy level":
            "has high energy",
        "has strong danceability":
            "has strong danceability",
        "is a popular track in the dataset":
            "is popular in the dataset",
    }

    for original, replacement in replacements.items():
        cleaned_reason = cleaned_reason.replace(
            original,
            replacement,
        )

    cleaned_reason = " ".join(
        cleaned_reason.split()
    )

    # Capitalise before either the full or shortened version is returned.
    # Previously, truncated explanations could remain lowercase.
    if cleaned_reason:
        cleaned_reason = (
            cleaned_reason[0].upper()
            + cleaned_reason[1:]
        )

    if len(cleaned_reason) <= maximum_length:
        return cleaned_reason + "."

    shortened = (
        cleaned_reason[:maximum_length]
        .rsplit(
            " ",
            1,
        )[0]
    )

    return (
        shortened.rstrip(
            ",;:"
        )
        + "…"
    )