# NextTrack

## University of London CM3070 Final Project

NextTrack is a stateless session-based music recommendation system developed as part of the University of London Computer Science Final Project.

The project investigates whether useful music recommendations can be generated using only the user's current session preferences without storing user accounts, listening history or long-term user profiles.

The system uses cosine similarity together with weighted ranking, diversity filtering and recommendation explanations to generate personalised music recommendations.

---

# Features

- FastAPI REST backend
- Streamlit frontend
- Stateless session-based recommendations
- Cosine similarity recommendation engine
- Weighted genre, mood and artist ranking
- Artist and genre diversity filtering
- Human-readable recommendation explanations
- Spotify search links
- YouTube search links
- Recommendation details (tempo, energy, popularity, danceability, valence and release year)
- Anonymous CSV-based user evaluation
- Automated testing with pytest
- Model comparison framework
- Evaluation framework

---

# Dataset

The recommendation engine currently uses approximately **1,000 curated songs**.

Each track contains:

- Track name
- Artist
- Genre
- Mood
- Tempo
- Energy
- Popularity
- Danceability
- Valence
- Release year
- Spotify Track ID (optional)

The dataset was created by transforming a public Spotify-derived music dataset into the NextTrack schema. The data were cleaned, filtered, balanced and enriched to improve recommendation quality while maintaining a lightweight recommendation system suitable for evaluation.

---

# Technologies

- Python
- FastAPI
- Streamlit
- Pandas
- NumPy
- Scikit-learn
- Pytest

---

# Requirements

- Python 3.12
- pip

---

# Project Structure

```text
Code/
├── backend/
│   ├── app/
│   │   ├── services/
│   │   ├── main.py
│   │   ├── recommender.py
│   │   ├── data_loader.py
│   │   ├── models.py
│   │   ├── evaluate.py
│   │   └── compare_models.py
│   └── data/
│
├── frontend/
│   ├── app.py
│   ├── api.py
│   ├── components.py
│   ├── feedback.py
│   ├── helpers.py
│   └── styles/
│
├── tests/
├── evaluation/
├── evidence/
├── results/
├── development_reflection.md
├── requirements.txt
└── README.md
```

---

# Running the Project

## 1. Install dependencies

```bash
pip install -r requirements.txt
```

---

## 2. Start the backend

```bash
PYTHONPATH=backend python -m uvicorn app.main:app --reload
```

Swagger documentation:

```
http://127.0.0.1:8000/docs
```

---

## 3. Start the frontend

Run the frontend in a separate terminal window.

```bash
streamlit run frontend/app.py
```

Frontend:

```
http://localhost:8501
```

---

# Running Tests

Run all automated tests from the project root:

```bash
python -m pytest
```

Current status:

- **30 automated tests**
- All tests passing

---

# Evaluation

The project includes:

- Recommendation evaluation framework
- Model comparison framework
- Anonymous user evaluation
- CSV feedback collection

Recommendation sessions are stateless and are not stored. Anonymous evaluation responses are saved locally to:

```text
evaluation/user_feedback.csv
```

---

# Recommendation Method

NextTrack combines several techniques:

1. Cosine similarity
2. Genre weighting
3. Mood weighting
4. Optional artist preference weighting
5. Artist diversity filtering
6. Genre diversity filtering

This produces recommendations that remain relevant while avoiding excessive repetition.

---

# Project Status

Current implementation includes:

- FastAPI backend
- Streamlit frontend
- Approximately 1,000-song dataset
- Recommendation explanations
- Spotify and YouTube search links
- Anonymous user evaluation
- Automated testing
- Model comparison
- Evaluation framework

The project was developed for educational purposes as part of the University of London CM3070 Computer Science Final Project.

---

**Author:** Gil Katz