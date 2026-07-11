from textwrap import dedent
import streamlit as st

from feedback import save_feedback
from helpers import (
    reset_inputs,
    safe_number,
    safe_percentage,
    safe_text,
    shorten_reason,
)

def render_hero():
    hero_html = (
        '<div class="hero">'
        '<h1 class="main-title">🎵 NextTrack</h1>'
        '<h2 class="hero-heading">'
        'Discover your next '
        '<span class="main-title-accent">favourite track.</span>'
        '</h2>'
        '<p class="subtitle">'
        'Choose genres, mood and an optional artist to receive personalised '
        'music recommendations based only on your current session. '
        'No account or listening history is required.'
        '</p>'
        '</div>'
    )

    st.markdown(
        hero_html,
        unsafe_allow_html=True,
    )

def render_preferences(options):
    with st.container(border=True):
        st.subheader("Start a recommendation session")

        st.markdown(
            dedent(
                """
                <div class="section-description">
                    Select at least one genre and one mood. Adding an artist
                    is optional, but it can influence how the results are
                    ranked.
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        genre_column, mood_column = st.columns([1.2, 1])

        with genre_column:
            genres = st.multiselect(
                "Genres",
                options.get("genres", []),
                placeholder="Select one or more genres",
                key="genres",
                help="You can choose multiple genres.",
            )

        with mood_column:
            mood = st.selectbox(
                "Mood",
                [""] + options.get("moods", []),
                format_func=lambda value: (
                    "Select a mood"
                    if value == ""
                    else value
                ),
                key="mood",
            )

        artist = st.selectbox(
            "Artist You Like (Optional)",
            [""] + options.get("artists", []),
            format_func=lambda value: (
                "No artist selected"
                if value == ""
                else value
            ),
            key="artist",
            help=(
                "The selected artist influences ranking but does not "
                "restrict every result to that artist."
            ),
        )

        _, generate_column, reset_column = st.columns(
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

    return genres, mood, artist, generate

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

    ranking_score = safe_percentage(rec.get("score"))

    with st.container(border=True):
        information_column, actions_column = st.columns(
            [6.4, 1.5],
            vertical_alignment="top",
        )

        with information_column:
            card_html = (
                f'<div class="track-position">'
                f'Recommendation {position}'
                f'</div>'
                f'<div class="track-title">{track}</div>'
                f'<div class="track-artist">{artist}</div>'
                f'<div class="metadata-row">'
                f'<span class="metadata-pill">🎧 {genre}</span>'
                f'<span class="metadata-pill">✨ {mood}</span>'
                f'</div>'
                f'<div class="reason-box">'
                f'<span class="reason-label">Why selected:</span> '
                f'{short_reason}'
                f'</div>'
                f'<div class="match-row">'
                f'<span class="match-label">Ranking score</span>'
                f'<span class="match-value">{ranking_score}/100</span>'
                f'</div>'
            )

            st.markdown(
                card_html,
                unsafe_allow_html=True,
            )

            st.progress(ranking_score)

            render_track_details(
                rec,
                full_reason,
            )

        with actions_column:
            render_search_buttons(rec)

def render_track_details(rec, full_reason):
    with st.expander(
        "View track details",
        expanded=False,
    ):
        detail_column_1, detail_column_2 = st.columns(2)

        energy = safe_percentage(rec.get("energy"))

        danceability = safe_percentage(
            rec.get("danceability")
        )

        valence = safe_percentage(
            rec.get("valence")
        )

        popularity = safe_number(
            rec.get("popularity")
        )

        tempo = safe_number(
            rec.get("tempo")
        )

        release_year = safe_text(
            rec.get("release_year"),
            "Unknown",
        )

        with detail_column_1:
            st.write(f"**Tempo:** {tempo} BPM")
            st.write(f"**Energy:** {energy}%")
            st.write(
                f"**Popularity:** {popularity}/100"
            )

        with detail_column_2:
            st.write(
                f"**Danceability:** {danceability}%"
            )
            st.write(
                f"**Valence (positiveness):** {valence}%"
            )
            st.write(
                f"**Release year:** {release_year}"
            )

        st.markdown(
            "**Full recommendation explanation**"
        )

        st.write(full_reason)


def render_search_buttons(rec):
    spotify_url = rec.get("spotify_url")
    youtube_url = rec.get("youtube_url")

    if spotify_url:
        st.markdown(
            '<div class="spotify-button">',
            unsafe_allow_html=True,
        )

        st.link_button(
            "Search on Spotify",
            spotify_url,
            use_container_width=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if youtube_url:
        st.markdown(
            '<div class="youtube-button">',
            unsafe_allow_html=True,
        )

        st.link_button(
            "Search on YouTube",
            youtube_url,
            use_container_width=True,
        )

        st.markdown(
            "</div>",
            unsafe_allow_html=True,
        )

    if not spotify_url and not youtube_url:
        st.caption(
            "No search links are available."
        )


def render_recommendations(recommendations):
    st.markdown("## Your recommendations")

    st.markdown(
        dedent(
            """
            <div class="section-description">
                Results are ranked using your current genre, mood and
                optional artist preferences. Open track details to view
                the full explanation and audio metadata.
            </div>
            """
        ),
        unsafe_allow_html=True,
    )

    for position, recommendation in enumerate(
        recommendations,
        start=1,
    ):
        render_recommendation(
            recommendation,
            position,
        )


def render_evaluation_form(
    genres,
    mood,
    artist,
):
    st.divider()

    with st.container(border=True):
        st.subheader("Evaluation form")

        st.markdown(
            dedent(
                """
                <div class="section-description">
                    This anonymous form supports the user-testing section
                    of the final project. No user account or personal
                    identity is recorded.
                </div>
                """
            ),
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
            disabled=st.session_state[
                "feedback_submitted"
            ],
        )

        if submit_feedback:
            submit_evaluation(
                genres=genres,
                mood=mood,
                artist=artist,
                match_rating=match_rating,
                diversity_rating=diversity_rating,
                usability_rating=usability_rating,
                overall_rating=overall_rating,
                comments=comments,
            )

        if st.session_state["feedback_submitted"]:
            st.info(
                "This recommendation session has already been evaluated. "
                "Generate a new session to submit another evaluation."
            )


def submit_evaluation(
    genres,
    mood,
    artist,
    match_rating,
    diversity_rating,
    usability_rating,
    overall_rating,
    comments,
):
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
            "Thank you. Your anonymous evaluation was saved successfully."
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

def render_about(options):
    st.divider()
    st.markdown("## About NextTrack")

    stats = options.get("stats", {})

    track_count = stats.get("track_count", 350)
    genre_count = stats.get("genre_count", "Available")
    artist_count = stats.get("artist_count", "Available")

    metric_column_1, metric_column_2, metric_column_3 = st.columns(3)

    with metric_column_1:
        st.metric(
            "Dataset size",
            f"{track_count} tracks",
        )

    with metric_column_2:
        st.metric(
            "Music genres",
            genre_count,
        )

    with metric_column_3:
        st.metric(
            "Unique artists",
            artist_count,
        )

    about_html = (
        '<div class="about-box">'
        '<strong>NextTrack</strong> is a stateless, session-based music '
        'recommendation system. It uses only the genres, mood and optional '
        'artist selected for the current session. It does not create user '
        'accounts or store listening histories, playlists or long-term '
        'user profiles.'
        '<br><br>'
        'Spotify and YouTube search links are generated dynamically so users '
        'can explore recommended tracks. Anonymous evaluation feedback is '
        'stored locally for academic testing. The project does not host or '
        'distribute audio files.'
        '</div>'
    )

    st.markdown(
        about_html,
        unsafe_allow_html=True,
    )

    st.divider()

    st.caption(
        "NextTrack · University of London Computer Science Final Project · "
        "Gil Katz"
    )