import requests
import streamlit as st

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
    .section-card {
        padding: 22px;
        border: 1px solid #ddd;
        border-radius: 12px;
        background-color: #ffffff;
        margin-bottom: 25px;
    }
    .recommendation-card {
        padding: 18px;
        border: 1px solid #ddd;
        border-radius: 12px;
        margin-bottom: 14px;
        background-color: #ffffff;
    }
    .small-muted {
        color: #666;
        font-size: 14px;
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


try:
    options = load_options()

    with st.container(border=True):
        st.subheader("Choose your session preferences")

        genres = st.multiselect(
            "Genre",
            options["genres"],
            placeholder="Select one or more genres",
        )

        mood = st.selectbox(
            "Mood",
            [""] + options["moods"],
            format_func=lambda x: "Select one" if x == "" else x,
        )

        artist = st.selectbox(
            "Artist You Like (Optional)",
            [""] + options["artists"],
            format_func=lambda x: "No artist selected" if x == "" else x,
        )

        generate = st.button("Generate Recommendations", type="primary")

    if generate:
        if not genres or not mood:
            st.warning("Please select at least one genre and one mood.")
        else:
            payload = {
                "genres": genres,
                "mood": mood,
                "seed_artists": [artist] if artist else [],
            }

            response = requests.post(f"{API_URL}/recommend", json=payload, timeout=10)
            response.raise_for_status()

            recommendations = response.json()["recommendations"][:5]

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

                    with right:
                        if rec.get("spotify_url"):
                            st.link_button("Open in Spotify", rec["spotify_url"])

except requests.exceptions.RequestException:
    st.error("Could not connect to the NextTrack backend. Make sure FastAPI is running.")

st.divider()

st.subheader("About NextTrack")

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("Dataset Size", "250 tracks")

with col2:
    st.metric("Method", "Cosine Similarity")

with col3:
    st.metric("User Profiles", "Not stored")

st.write(
    "NextTrack is a stateless session-based recommendation system. "
    "It uses only the current genre, mood and optional artist input to generate recommendations. "
    "It does not store user accounts, listening history, playlists or long-term profiles."
)