# NextTrack

## Preliminary Prototype

NextTrack is a privacy-focused music recommendation API developed as part of a final-year Computer Science project.

The project explores whether useful music recommendations can be generated using temporary session-based input without storing long-term user profiles or behavioural history.

This repository currently contains the preliminary prototype implementation of the recommendation engine.

## Current Features

* FastAPI backend
* RESTful API endpoints
* Session-based recommendation processing
* Music metadata dataset
* Cosine similarity recommendation scoring
* Diversity filtering
* JSON recommendation responses
* Basic evaluation scripts

## Technologies Used

* Python
* FastAPI
* Pandas
* NumPy
* scikit-learn

## API Endpoints

| Endpoint          | Description              |
| ----------------- | ------------------------ |
| `GET /`           | Root endpoint            |
| `POST /recommend` | Generate recommendations |
| `GET /health`     | API health check         |

## Running the Prototype

Install dependencies:

```bash
pip install -r requirements.txt
```

Run the API:

```bash
uvicorn app.main:app --reload
```

Open Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

## Academic Context

This prototype was developed for the preliminary submission of the NextTrack final-year project and is intended to demonstrate the feasibility of stateless session-based music recommendations.
