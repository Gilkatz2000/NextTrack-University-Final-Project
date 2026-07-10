import html

import requests
import streamlit as st

from feedback import save_feedback

API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 10
MAX_RECOMMENDATIONS = 10

st.set_page_config(
    page_title="NextTrack",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="collapsed",
)

st.markdown(
    """
    <style>
    #MainMenu,
    header,
    footer {
        visibility: hidden;
    }

    .stApp {
        background:
            radial-gradient(
                circle at 15% 5%,
                rgba(99, 102, 241, 0.10),
                transparent 30%
            ),
            radial-gradient(
                circle at 90% 15%,
                rgba(14, 165, 233, 0.08),
                transparent 26%
            ),
            linear-gradient(180deg, #f8fafc 0%, #eef2f7 100%);
        color: #172033;
    }

    .block-container {
        max-width: 1320px;
        padding-top: 1.5rem;
        padding-bottom: 2.25rem;
    }

    .hero {
        margin-bottom: 1.3rem;
        padding-top: 0.2rem;
    }

    .hero-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.45rem;
        margin-bottom: 0.65rem;
        padding: 0.38rem 0.76rem;
        border: 1px solid rgba(79, 70, 229, 0.16);
        border-radius: 999px;
        background: rgba(255, 255, 255, 0.75);
        color: #4338ca;
        font-size: 0.8rem;
        font-weight: 700;
        box-shadow: 0 4px 14px rgba(30, 41, 59, 0.05);
    }

    .main-title {
        margin: 0;
        color: #172033;
        font-size: clamp(2.4rem, 5vw, 4rem);
        font-weight: 850;
        line-height: 1.04;
        letter-spacing: -0.045em;
    }

    .main-title-accent {
        color: #4f46e5;
    }

    .subtitle {
        max-width: 800px;
        margin-top: 0.7rem;
        margin-bottom: 0;
        color: #5f6b7a;
        font-size: clamp(1rem, 2vw, 1.12rem);
        line-height: 1.55;
    }

    [data-testid="stVerticalBlockBorderWrapper"] {
        overflow: hidden;
        border: 1px solid rgba(148, 163, 184, 0.25);
        border-radius: 18px;
        background: rgba(255, 255, 255, 0.94);
        box-shadow:
            0 8px 26px rgba(15, 23, 42, 0.055),
            0 2px 7px rgba(15, 23, 42, 0.025);
    }

    [data-testid="stVerticalBlockBorderWrapper"] > div {
        padding: 0.15rem;
    }

    h1,
    h2,
    h3 {
        color: #172033;
        letter-spacing: -0.025em;
    }

    h2 {
        margin-top: 0.9rem;
        margin-bottom: 0.45rem;
    }

    h3 {
        margin-top: 0.35rem;
    }

    [data-baseweb="select"] > div,
    [data-testid="stTextArea"] textarea {
        border-radius: 12px !important;
    }

    [data-testid="stMultiSelect"] [data-baseweb="tag"] {
        border-radius: 999px;
        background: #eef2ff;
        color: #3730a3;
    }

    .stButton > button,
    .stLinkButton > a {
        min-height: 2.65rem;
        border-radius: 11px;
        font-weight: 750;
        transition:
            transform 0.15s ease,
            box-shadow 0.15s ease,
            border-color 0.15s ease,
            background 0.15s ease;
    }

    .stButton > button:hover,
    .stLinkButton > a:hover {
        transform: translateY(-1px);
        box-shadow: 0 7px 18px rgba(15, 23, 42, 0.10);
    }

    .stButton > button[kind="primary"] {
        border: none;
        background: linear-gradient(135deg, #4f46e5, #6366f1);
        color: white;
    }

    .spotify-button .stLinkButton > a {
        border: 1px solid rgba(22, 163, 74, 0.28);
        background: rgba(240, 253, 244, 0.95);
        color: #166534;
    }

    .spotify-button .stLinkButton > a:hover {
        border-color: rgba(22, 163, 74, 0.55);
        background: #dcfce7;
    }

    .youtube-button .stLinkButton > a {
        border: 1px solid rgba(220, 38, 38, 0.24);
        background: rgba(254, 242, 242, 0.96);
        color: #991b1b;
    }

    .youtube-button .stLinkButton > a:hover {
        border-color: rgba(220, 38, 38, 0.5);
        background: #fee2e2;
    }

    .track-position {
        margin-bottom: 0.22rem;
        color: #4f46e5;
        font-size: 0.7rem;
        font-weight: 850;
        letter-spacing: 0.09em;
        text-transform: uppercase;
    }

    .track-title {
        margin: 0;
        color: #172033;
        font-size: clamp(1.18rem, 2.4vw, 1.5rem);
        font-weight: 820;
        line-height: 1.2;
        letter-spacing: -0.025em;
    }

    .track-artist {
        margin-top: 0.18rem;
        margin-bottom: 0.6rem;
        color: #657184;
        font-size: 0.94rem;
        font-weight: 620;
    }

    .metadata-row {
        display: flex;
        flex-wrap: wrap;
        gap: 0.4rem;
        margin: 0.55rem 0 0.7rem;
    }

    .metadata-pill {
        display: inline-flex;
        align-items: center;
        padding: 0.28rem 0.62rem;
        border: 1px solid #dfe5ee;
        border-radius: 999px;
        background: #f8fafc;
        color: #475569;
        font-size: 0.75rem;
        font-weight: 720;
    }

    .reason-box {
        margin: 0.65rem 0;
        padding: 0.68rem 0.85rem;
        border-left: 3px solid #6366f1;
        border-radius: 0 10px 10px 0;
        background: #f5f7ff;
        color: #465166;
        font-size: 0.87rem;
        line-height: 1.5;
    }

    .reason-label {
        color: #3730a3;
        font-weight: 820;
    }

    .match-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 1rem;
        margin-top: 0.55rem;
        margin-bottom: 0.25rem;
    }

    .match-label {
        color: #475569;
        font-size: 0.84rem;
        font-weight: 720;
    }

    .match-value {
        color: #3730a3;
        font-size: 0.92rem;
        font-weight: 850;
    }

    .listen-heading {
        margin-bottom: 0.55rem;
        color: #172033;
        font-size: 0.98rem;
        font-weight: 800;
    }

    [data-testid="stMetric"] {
        min-height: 108px;
        padding: 0.9rem;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.82);
        box-shadow: 0 6px 17px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stMetricValue"] {
        color: #3730a3;
        font-weight: 800;
    }

    .section-description {
        max-width: 850px;
        margin-bottom: 0.85rem;
        color: #64748b;
        line-height: 1.55;
    }

    .about-box {
        padding: 0.95rem 1.1rem;
        border: 1px solid rgba(148, 163, 184, 0.22);
        border-radius: 15px;
        background: rgba(255, 255, 255, 0.72);
        color: #526074;
        line-height: 1.65;
    }

    [data-testid="stAlert"] {
        border-radius: 13px;
    }

    [data-testid="stExpander"] {
        border: 1px solid #e2e8f0;
        border-radius: 10px;
        background: #fbfdff;
    }

    [data-testid="stExpander"] summary {
        min-height: 2.55rem;
    }

    [data-testid="stProgressBar"] {
        margin-bottom: 0.35rem;
    }

    hr {
        margin: 1.65rem 0 !important;
        border-color: rgba(148, 163, 184, 0.22) !important;
    }

    @media (max-width: 768px) {
        .block-container {
            padding: 1rem 0.9rem 1.8rem;
        }

        .hero {
            margin-bottom: 1rem;
        }

        .main-title {
            font-size: 2.45rem;
        }

        .subtitle {
            line-height: 1.5;
        }

        [data-testid="stHorizontalBlock"] {
            flex-wrap: wrap;
            gap: 0.65rem;
        }

        [data-testid="column"] {
            min-width: 100% !important;
            width: 100% !important;
            flex: 1 1 100% !important;
        }


        .stButton > button,
        .stLinkButton > a {
            width: 100%;
        }

        [data-testid="stMetric"] {
            min-height: auto;
        }

        .listen-heading {
            margin-top: 0.25rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


def initialise_session_state():
    defaults = {
        "genres": [],
        "mood": "",
        "artist": "",
        "recommendations": [],
        "feedback_submitted": False,
    }

    for key, default_value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = default_value


@st.cache_data(ttl=300)
def load_options():
    response = requests.get(
        f"{API_URL}/tracks/options",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def reset_inputs():
    st.session_state["genres"] = []
    st.session_state["mood"] = ""
    st.session_state["artist"] = ""
    st.session_state["recommendations"] = []
    st.session_state["feedback_submitted"] = False


def safe_text(value, default="Unknown"):
    if value is None:
        return default

    text = str(value).strip()
    return html.escape(text) if text else default


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


def shorten_reason(reason, maximum_length=155):
    cleaned_reason = str(reason or "").strip()

    if not cleaned_reason:
        return "Selected using your current genre, mood and artist preferences."

    cleaned_reason = cleaned_reason.replace("Recommended because ", "")
    cleaned_reason = cleaned_reason.rstrip(".")

    replacements = {
        "it matches both your selected genre and mood":
            "matches your selected genre and mood",
        "it matches your selected genre":
            "matches your selected genre",
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
        cleaned_reason = cleaned_reason.replace(original, replacement)

    cleaned_reason = " ".join(cleaned_reason.split())

    if len(cleaned_reason) <= maximum_length:
        return cleaned_reason[0].upper() + cleaned_reason[1:] + "."

    shortened = cleaned_reason[:maximum_length].rsplit(" ", 1)[0]
    return shortened.rstrip(",;:") + "…"



def render_recommendation(rec, position):
    track = safe_text(rec.get("track"), "Unknown track")
    artist = safe_text(rec.get("artist"), "Unknown artist")
    genre = safe_text(rec.get("genre"), "Unknown").title()
    mood = safe_text(rec.get("mood"), "Unknown").title()

    full_reason = safe_text(
        rec.get("reason"),
        "This track was selected based on your current preferences.",
    )

    short_reason = safe_text(
        shorten_reason(rec.get("reason")),
        "Selected using your current session preferences.",
    )

    match_percentage = safe_percentage(rec.get("score"))

    with st.container(border=True):
        information_column, actions_column = st.columns(
            [6.4, 1.5],
            vertical_alignment="top",
        )

        with information_column:
            st.markdown(
                f"""
                <div class="track-position">
                    Recommendation {position}
                </div>

                <div class="track-title">
                    {track}
                </div>

                <div class="track-artist">
                    {artist}
                </div>

                <div class="metadata-row">
                    <span class="metadata-pill">🎧 {genre}</span>
                    <span class="metadata-pill">✨ {mood}</span>
                </div>

                <div class="reason-box">
                    <span class="reason-label">Why selected:</span>
                    {short_reason}
                </div>

                <div class="match-row">
                    <span class="match-label">Session match</span>
                    <span class="match-value">
                        {match_percentage}/100
                    </span>
                </div>
                """,
                unsafe_allow_html=True,
            )

            st.progress(match_percentage)

            with st.expander("View track details", expanded=False):
                detail_column_1, detail_column_2 = st.columns(2)

                energy_percentage = safe_percentage(rec.get("energy"))
                danceability_percentage = safe_percentage(
                    rec.get("danceability")
                )
                valence_percentage = safe_percentage(rec.get("valence"))
                popularity = safe_number(rec.get("popularity"))
                tempo = safe_number(rec.get("tempo"))
                release_year = safe_text(
                    rec.get("release_year"),
                    "Unknown",
                )

                with detail_column_1:
                    st.write(f"**Tempo:** {tempo} BPM")
                    st.write(f"**Energy:** {energy_percentage}%")
                    st.write(f"**Popularity:** {popularity}/100")

                with detail_column_2:
                    st.write(
                        f"**Danceability:** "
                        f"{danceability_percentage}%"
                    )
                    st.write(
                        f"**Valence (positiveness):** "
                        f"{valence_percentage}%"
                    )
                    st.write(f"**Release year:** {release_year}")

                st.markdown("**Full recommendation explanation**")
                st.write(full_reason)

        with actions_column:
            st.markdown(
                '<div class="listen-heading">Listen</div>',
                unsafe_allow_html=True,
            )

            spotify_url = rec.get("spotify_url")
            youtube_url = rec.get("youtube_url")

            if spotify_url:
                st.markdown(
                    '<div class="spotify-button">',
                    unsafe_allow_html=True,
                )
                st.link_button(
                    "Spotify ↗",
                    spotify_url,
                    use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

            if youtube_url:
                st.markdown(
                    '<div class="youtube-button">',
                    unsafe_allow_html=True,
                )
                st.link_button(
                    "YouTube ↗",
                    youtube_url,
                    use_container_width=True,
                )
                st.markdown("</div>", unsafe_allow_html=True)

            if not spotify_url and not youtube_url:
                st.caption("No listening links are available.")


initialise_session_state()

st.markdown(
    """
<div class="hero">
    <div class="hero-badge">🎓 University final project</div>
    <h1 class="main-title">
        Discover your next
        <span class="main-title-accent">favourite track.</span>
    </h1>
    <p class="subtitle">
        Choose the genres and mood that fit your session.
        NextTrack will generate personalised recommendations without
        requiring an account or storing your listening history.
    </p>
</div>
""",
    unsafe_allow_html=True,
)

options = {}
generate = False
genres = st.session_state["genres"]
mood = st.session_state["mood"]
artist = st.session_state["artist"]

try:
    options = load_options()

    with st.container(border=True):
        st.subheader("Choose your session preferences")

        st.markdown(
            """
            <div class="section-description">
                Select at least one genre and one mood. Adding an artist is
                optional, but it can influence how the results are ranked.
            </div>
            """,
            unsafe_allow_html=True,
        )

        selection_column_1, selection_column_2 = st.columns([1.2, 1])

        with selection_column_1:
            genres = st.multiselect(
                "Genres",
                options.get("genres", []),
                placeholder="Select one or more genres",
                key="genres",
                help="You can choose multiple genres.",
            )

        with selection_column_2:
            mood = st.selectbox(
                "Mood",
                [""] + options.get("moods", []),
                format_func=lambda value: (
                    "Select a mood" if value == "" else value
                ),
                key="mood",
            )

        artist = st.selectbox(
            "Artist You Like (Optional)",
            [""] + options.get("artists", []),
            format_func=lambda value: (
                "No artist selected" if value == "" else value
            ),
            key="artist",
            help=(
                "The selected artist influences ranking but does not "
                "restrict every result to that artist."
            ),
        )

        button_spacer, generate_column, reset_column = st.columns(
            [2.7, 1.45, 0.9],
            vertical_alignment="bottom",
        )

        with generate_column:
            generate = st.button(
                "✨ Generate Recommendations",
                type="primary",
                use_container_width=True,
            )

        with reset_column:
            st.button(
                "Clear",
                on_click=reset_inputs,
                use_container_width=True,
            )

    if generate:
        st.session_state["feedback_submitted"] = False

        if not genres or not mood:
            st.session_state["recommendations"] = []

            st.warning(
                "Please select at least one genre and one mood before "
                "generating recommendations."
            )
        else:
            payload = {
                "genres": genres,
                "mood": mood,
                "seed_artists": [artist] if artist else [],
            }

            with st.spinner(
                "Analysing your preferences and selecting tracks..."
            ):
                response = requests.post(
                    f"{API_URL}/recommend",
                    json=payload,
                    timeout=REQUEST_TIMEOUT,
                )
                response.raise_for_status()

                recommendations = response.json().get(
                    "recommendations",
                    [],
                )

                st.session_state["recommendations"] = recommendations[
                    :MAX_RECOMMENDATIONS
                ]

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

    recommendations = st.session_state["recommendations"]

    if recommendations:
        st.markdown("## Your recommendations")

        st.markdown(
            """
            <div class="section-description">
                Results are ranked using your current genre, mood and optional
                artist preferences. Open track details to view the full
                explanation and audio metadata.
            </div>
            """,
            unsafe_allow_html=True,
        )

        for position, recommendation in enumerate(
            recommendations,
            start=1,
        ):
            render_recommendation(recommendation, position)

        st.divider()

        with st.container(border=True):
            st.subheader("Evaluation form")

            st.markdown(
                """
                <div class="section-description">
                    This anonymous form supports the user-testing section of
                    the final project. No user account or personal identity is
                    recorded.
                </div>
                """,
                unsafe_allow_html=True,
            )

            rating_column_1, rating_column_2 = st.columns(2)

            with rating_column_1:
                match_rating = st.slider(
                    "How well did the recommendations match your taste?",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Poor, 5 = Excellent",
                )

                diversity_rating = st.slider(
                    "How diverse were the recommendations?",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Not diverse, 5 = Very diverse",
                )

            with rating_column_2:
                usability_rating = st.slider(
                    "How easy was the interface to use?",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Difficult, 5 = Very easy",
                )

                overall_rating = st.slider(
                    "What is your overall satisfaction?",
                    min_value=1,
                    max_value=5,
                    value=3,
                    help="1 = Poor, 5 = Excellent",
                )

            comments = st.text_area(
                "Optional comments",
                placeholder=(
                    "What worked well, and what could be improved?"
                ),
                max_chars=1000,
            )

            submit_feedback = st.button(
                "Submit Anonymous Evaluation",
                type="primary",
                use_container_width=True,
                disabled=st.session_state["feedback_submitted"],
            )

            if submit_feedback:
                try:
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

                    st.session_state["feedback_submitted"] = True

                    st.success(
                        "Thank you. Your anonymous evaluation was saved "
                        "successfully."
                    )

                    st.toast(
                        "Evaluation submitted.",
                        icon="✅",
                    )

                except (OSError, ValueError) as error:
                    st.error(
                        "The evaluation could not be saved. "
                        "Please check that the feedback CSV file is writable."
                    )
                    st.exception(error)

            if st.session_state["feedback_submitted"]:
                st.info(
                    "This recommendation session has already been evaluated. "
                    "Generate a new session to submit another evaluation."
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
        f"The backend returned an error with status code {status_code}. "
        "Check the FastAPI terminal for more information."
    )

except (KeyError, TypeError, ValueError):
    st.error(
        "NextTrack received an unexpected response from the backend. "
        "Check that the frontend and backend are using compatible versions."
    )

st.divider()

st.markdown("## About NextTrack")

stats = options.get("stats", {})

statistics_column_1, statistics_column_2, statistics_column_3 = st.columns(3)

with statistics_column_1:
    st.metric(
        "Dataset size",
        f"{stats.get('track_count', 350)} tracks",
    )

with statistics_column_2:
    st.metric(
        "Music genres",
        stats.get("genre_count", "Available"),
    )

with statistics_column_3:
    st.metric(
        "Unique artists",
        stats.get("artist_count", "Available"),
    )

st.markdown(
    """
    <div class="about-box">
        <strong>NextTrack</strong> is a stateless, session-based music
        recommendation system. It uses only the genres, mood and optional
        artist selected for the current session. It does not create user
        accounts or store listening histories, playlists or long-term user
        profiles.
        <br><br>
        Spotify and YouTube search links are generated dynamically so users
        can explore recommended tracks. Anonymous evaluation feedback is
        stored locally for academic testing. The project does not host or
        distribute audio files.
    </div>
    """,
    unsafe_allow_html=True,
)

st.divider()

st.caption(
    "NextTrack · University of London Computer Science Final Project · "
    "Gil Katz"
)