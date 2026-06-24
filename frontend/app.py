import requests
import streamlit as st

from feedback import save_feedback

API_URL = "http://127.0.0.1:8000"

st.set_page_config(page_title="NextTrack", page_icon="🎵", layout="wide")

st.markdown(
    """
    <style>
    .main-title {
        font-size: 46px;
        font-weight: 800;
        margin-bottom: 0px;
    }
    .subtitle {
        font-size: 18px;
        color: #555;
        margin-bottom: 25px;
    }
    .stApp {
        background: linear-gradient(180deg, #f7f9fc 0%, #eef2f7 100%);
    }
    .block-container {
        max-width: 1100px;
        padding-top: 2rem;
        padding-bottom: 2rem;
    }
    [data-testid="stVerticalBlockBorderWrapper"] {
        background-color: white;
        border-radius: 14px;
        box-shadow: 0 4px 14px rgba(0, 0, 0, 0.06);
    }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="main-title">🎵 NextTrack</div>', unsafe_allow_html=True)
st.markdown(
    '<div class="subtitle">Generate music recommendations based on genre, mood and an artist you like.</div>',
    unsafe_allow_html=True,
)


@st.cache_data
def load_options():
    response = requests.get(f"{API_URL}/tracks/options", timeout=10)
    response.raise_for_status()
    return response.json()


def reset_inputs():
    st.session_state["genres"] = []
    st.session_state["mood"] = ""
    st.session_state["artist"] = ""
    st.session_state["recommendations"] = []


try:
    options = load_options()

    if "recommendations" not in st.session_state:
        st.session_state["recommendations"] = []

    with st.container(border=True):
        st.subheader("Choose your session preferences")

        genres = st.multiselect(
            "Genre",
            options["genres"],
            placeholder="Select one or more genres",
            key="genres",
        )

        mood = st.selectbox(
            "Mood",
            [""] + options["moods"],
            format_func=lambda x: "Select one" if x == "" else x,
            key="mood",
        )

        artist = st.selectbox(
            "Artist You Like (Optional)",
            [""] + options["artists"],
            format_func=lambda x: "No artist selected" if x == "" else x,
            key="artist",
        )

        col_generate, col_reset = st.columns([1, 1])

        with col_generate:
            generate = st.button("Generate Recommendations", type="primary")

        with col_reset:
            st.button("Reset / Clear", on_click=reset_inputs)

    if generate:
        if not genres or not mood:
            st.warning("Please select at least one genre and one mood.")
            st.session_state["recommendations"] = []
        else:
            payload = {
                "genres": genres,
                "mood": mood,
                "seed_artists": [artist] if artist else [],
            }

            response = requests.post(f"{API_URL}/recommend", json=payload, timeout=10)
            response.raise_for_status()

            st.session_state["recommendations"] = response.json().get(
                "recommendations",
                [],
            )[:10]

    recommendations = st.session_state["recommendations"]

    if recommendations:
        st.subheader("Recommendations")

        for i, rec in enumerate(recommendations, start=1):
            with st.container(border=True):
                left, right = st.columns([5, 1])

                with left:
                    st.markdown(f"### {i}. {rec['track']}")
                    st.write(f"**Artist:** {rec['artist']}")
                    st.write(f"**Genre:** {rec['genre']} | **Mood:** {rec['mood']}")
                    st.write(f"**Why recommended:** {rec['reason']}")
                    st.write(f"**Score:** {round(float(rec['score']), 3)}")

                    with st.expander("View track details"):
                        st.write(f"Tempo: {rec['tempo']}")
                        st.write(f"Energy: {rec['energy']}")
                        st.write(f"Popularity: {rec['popularity']}")
                        st.write(f"Danceability: {rec['danceability']}")
                        st.write(f"Valence: {rec['valence']}")
                        st.write(f"Release year: {rec['release_year']}")

                with right:
                    if rec.get("spotify_url"):
                        st.link_button("Search on Spotify", rec["spotify_url"])

                    if rec.get("youtube_url"):
                        st.link_button("Search on YouTube", rec["youtube_url"])

        st.divider()
        st.subheader("Evaluation Form")

        st.write(
            "Use this section during user testing. "
            "Feedback is saved anonymously to a local CSV file for evaluation evidence."
        )

        match_rating = st.slider(
            "How well did the recommendations match your taste? (1 = poor, 5 = excellent)",
            1,
            5,
            3,
        )

        diversity_rating = st.slider(
            "How diverse were the recommendations? (1 = not diverse, 5 = very diverse)",
            1,
            5,
            3,
        )

        usability_rating = st.slider(
            "How easy was the interface to use? (1 = difficult, 5 = very easy)",
            1,
            5,
            3,
        )

        overall_rating = st.slider(
            "Overall satisfaction (1 = poor, 5 = excellent)",
            1,
            5,
            3,
        )

        comments = st.text_area("Optional comments")

        if st.button("Submit Evaluation"):
            save_feedback(
                genres,
                mood,
                artist,
                match_rating,
                diversity_rating,
                usability_rating,
                overall_rating,
                comments,
            )

            st.success(
                "Evaluation submitted anonymously and saved to evaluation/user_feedback.csv."
            )

            st.write(f"Recommendation match rating: {match_rating}/5")
            st.write(f"Diversity rating: {diversity_rating}/5")
            st.write(f"Usability rating: {usability_rating}/5")
            st.write(f"Overall satisfaction: {overall_rating}/5")

            if comments:
                st.write(f"Comments: {comments}")

    elif generate:
        st.info("No recommendations found for this session. Try choosing another mood or genre.")

except requests.exceptions.RequestException:
    st.error(
        "Could not connect to the NextTrack backend. "
        "Make sure FastAPI is running, then try again."
    )

st.divider()

st.subheader("About NextTrack")

stats = options.get("stats", {})

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset Size", f"{stats.get('track_count', 350)} tracks")

with col2:
    st.metric("Genres", stats.get("genre_count", "Available"))

with col3:
    st.metric("Artists", stats.get("artist_count", "Available"))

st.write(
    "NextTrack is a stateless session-based recommendation system. "
    "It uses only the current genre, mood and optional artist input to generate recommendations. "
    "It does not store user accounts, listening history, playlists or long-term profiles. "
    "Spotify and YouTube search links are generated dynamically to help users explore recommended tracks. "
    "Evaluation feedback is saved anonymously for project testing only. "
    "No audio files are stored by the project."
)

st.divider()
st.caption("NextTrack | University of London Final Project | Gil Katz")