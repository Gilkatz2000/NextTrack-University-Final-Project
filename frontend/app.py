import requests
import streamlit as st

from api import get_recommendations, load_options
from components import (
    render_about,
    render_evaluation_form,
    render_hero,
    render_preferences,
    render_recommendations,
)
from helpers import (
    initialise_session_state,
    load_css,
)

MAX_RECOMMENDATIONS = 10


st.set_page_config(
    page_title="NextTrack",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)


def generate_recommendations(
    genres,
    mood,
    artist,
):
    if not genres or not mood:
        st.session_state["recommendations"] = []

        st.warning(
            "Please select at least one genre and one mood before "
            "generating recommendations."
        )

        return

    payload = {
        "genres": genres,
        "mood": mood,
        "seed_artists": [artist] if artist else [],
    }

    with st.spinner(
        "Analysing your preferences and selecting tracks..."
    ):
        recommendations = get_recommendations(payload)

    st.session_state["recommendations"] = recommendations[
        :MAX_RECOMMENDATIONS
    ]
    
    st.session_state["generated_artist"] = artist

    if st.session_state["recommendations"]:
        recommendation_count = len(
            st.session_state["recommendations"]
        )

        st.success(
            f"Your session is ready. NextTrack found "
            f"{recommendation_count} recommendations."
        )

        st.toast(
            "Recommendations generated successfully.",
            icon="🎵",
        )


def run_app():
    load_css()
    initialise_session_state()
    render_hero()

    options = {}

    try:
        options = load_options()

        genres, mood, artist, generate = render_preferences(
            options
        )

        if generate:
            st.session_state["feedback_submitted"] = False

            generate_recommendations(
                genres,
                mood,
                artist,
            )

        recommendations = st.session_state[
            "recommendations"
        ]

        if recommendations:
            render_recommendations(
                recommendations,
                selected_artist=st.session_state[
                    "generated_artist"
                ],
            )

            render_evaluation_form(
                genres=genres,
                mood=mood,
                artist=artist,
            )

        elif generate and genres and mood:
            st.info(
                "No recommendations were found for this session. "
                "Try choosing another mood, genre or artist."
            )

    except requests.exceptions.Timeout:
        st.error(
            "The NextTrack backend took too long to respond. "
            "Make sure FastAPI is running and try again."
        )

    except requests.exceptions.ConnectionError:
        st.error(
            "Could not connect to the NextTrack backend. "
            "Start FastAPI and then refresh this page."
        )

    except requests.exceptions.HTTPError as error:
        status_code = (
            error.response.status_code
            if error.response is not None
            else "unknown"
        )

        st.error(
            f"The backend returned an error with status code "
            f"{status_code}. Check the FastAPI terminal for more "
            f"information."
        )

    except (KeyError, TypeError, ValueError):
        st.error(
            "NextTrack received an unexpected response from the backend. "
            "Check that the frontend and backend are using compatible "
            "versions."
        )

    render_about(options)


if __name__ == "__main__":
    run_app()