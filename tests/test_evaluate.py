from app.evaluate import evaluate_session, run_evaluation
from app.test_sessions import TEST_SESSIONS


def test_evaluate_session_returns_expected_metrics():
    result = evaluate_session(TEST_SESSIONS[0])

    assert result["session_name"] == TEST_SESSIONS[0]["name"]
    assert result["recommendation_count"] > 0
    assert result["response_time_seconds"] >= 0
    assert result["max_artist_repetition"] <= 2
    assert result["max_genre_repetition"] <= 3
    assert result["passed_response_time"] is True
    assert result["passed_artist_diversity"] is True
    assert result["passed_genre_diversity"] is True


def test_run_evaluation_returns_one_result_per_test_session():
    results = run_evaluation()

    assert len(results) == len(TEST_SESSIONS)
    assert all("session_name" in result for result in results)

def test_genre_match_rate_is_valid():
    result = evaluate_session(TEST_SESSIONS[0])

    assert 0 <= result["genre_match_rate"] <= 1

def test_mood_match_rate_is_valid():
    result = evaluate_session(TEST_SESSIONS[0])

    assert 0 <= result["mood_match_rate"] <= 1