# NextTrack

## Project Overview

NextTrack is a music recommendation API developed as part of my University of London CM3070 Computer Science Final Project.

The aim of the project is to investigate whether useful music recommendations can be generated using temporary session information without storing user accounts, listening history or long-term user profiles.

The system uses music metadata together with a cosine similarity recommendation algorithm to generate recommendations based on the user's current preferences.

## Current Features

* FastAPI backend
* Session-based recommendation generation
* Music metadata dataset
* Cosine similarity recommendation algorithm
* Artist and genre diversity filtering
* Recommendation explanations
* JSON API responses
* Automated testing using pytest
* Evaluation framework
* Baseline recommender for comparison
* CSV evaluation reports

## Technologies Used

* Python
* FastAPI
* Pandas
* NumPy
* Scikit-learn
* Pytest

## API Endpoints

| Endpoint          | Description              |
| ----------------- | ------------------------ |
| `GET /`           | Root endpoint            |
| `GET /health`     | Health check             |
| `POST /recommend` | Generate recommendations |

## Running the Project

Install the required packages:

```bash
pip install -r requirements.txt
```

Start the API:

```bash
uvicorn app.main:app --reload
```

Open the Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Running Tests

Run all automated tests:

```bash
python -m pytest
```

## Running the Evaluation

Run the evaluation framework:

```bash
PYTHONPATH=NextTrack python NextTrack/app/evaluate.py
```

Results will be saved to:

```text
evaluation_results.csv
```

The evaluation currently measures:

* Response time
* Artist diversity
* Genre diversity
* Genre match rate
* Mood match rate

## Baseline Comparison

A simple baseline recommender was created for comparison purposes. The baseline uses genre matching and popularity ranking only.

Run the comparison:

```bash
PYTHONPATH=NextTrack python NextTrack/app/compare_models.py
```

Results will be saved to:

```text
model_comparison_metrics.csv
```

## Project Structure

```text
NextTrack/
├── app/
│   ├── main.py
│   ├── recommender.py
│   ├── evaluate.py
│   ├── baseline.py
│   ├── compare_models.py
│   ├── dataset.csv
│   └── test_sessions.py
│
├── tests/
│   ├── test_api.py
│   ├── test_evaluate.py
│   └── test_recommender.py
│
├── evaluation_results.csv
├── model_comparison_metrics.csv
├── development_reflection.md
├── requirements.txt
└── README.md
```

## Project Status

The project has progressed beyond the preliminary prototype stage. Recent work has focused on expanding the dataset, introducing automated testing, improving evaluation methods, adding recommendation explanations and comparing the recommendation engine against a baseline approach.
