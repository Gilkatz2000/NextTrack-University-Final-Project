import requests
import streamlit as st

API_URL = "http://127.0.0.1:8000"
REQUEST_TIMEOUT = 10


@st.cache_data(ttl=300)
def load_options():
    response = requests.get(
        f"{API_URL}/tracks/options",
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()
    return response.json()


def get_recommendations(payload):
    response = requests.post(
        f"{API_URL}/recommend",
        json=payload,
        timeout=REQUEST_TIMEOUT,
    )
    response.raise_for_status()

    return response.json().get("recommendations", [])