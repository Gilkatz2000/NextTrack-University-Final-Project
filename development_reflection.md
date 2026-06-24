# Development Log

## 18/06/2026

* Added pytest to the project.
* Created 10 automated tests for the API, recommendation engine and evaluation functions.
* Fixed Python environment and package issues that were causing problems when running tests.
* Expanded the music dataset from 8 tracks to 48 tracks.
* Increased the number of evaluation sessions from 3 to 8.
* Updated the evaluation script to generate results in CSV format.
* Generated evaluation_results.csv for evaluation and analysis.
* Verified that all automated tests passed successfully.
* Confirmed that all evaluation sessions passed the response time, artist diversity and genre diversity checks.
* Created a simple baseline recommender based on genre matching and popularity.
* Added a comparison script to compare NextTrack against the baseline recommender.
* Generated comparison results showing differences between the two approaches.
* Added model_comparison_results.txt and model_comparison_metrics.csv as supporting evidence.
* Added recommendation relevance metrics including genre match rate and mood match rate.
* Extended the evaluation framework to measure recommendation relevance as well as performance and diversity.
* Added a reason field to recommendations so that the system can explain why a track was selected.
* Updated the automated tests to support the new recommendation format.
* Verified that all tests still passed after the new features were added.

## 21/06/2026

* Expanded the music dataset from 48 tracks to 250 real songs.
* Added additional track metadata including danceability, valence, release year and Spotify links.
* Created a dedicated data folder and introduced a reusable data loading component.
* Refactored the recommendation engine to use the new dataset structure.
* Updated the baseline recommender to use the expanded dataset.
* Updated the second recommendation model (NextTrack V2) to support the additional track features.
* Extended recommendation responses to include danceability, valence, release year and Spotify links.
* Added a new API endpoint (`/tracks/options`) to return available genres, moods and artists from the dataset.
* Verified that the new endpoint worked correctly through FastAPI and Swagger testing.
* Removed the original prototype dataset file and consolidated the project to use a single dataset source.
* Added additional automated tests for dataset loading, API endpoints and recommendation responses, increasing the total number of automated tests to 17.
* Verified that all automated tests passed successfully after the refactoring work.
* Reorganised project outputs into a dedicated results folder to improve project structure and maintainability.
* Re-ran recommendation model comparisons using the expanded dataset.
* Generated updated comparison metrics and evaluation results.
* Verified that recommendation generation remained fast despite increasing the dataset from 48 to 250 tracks.
* Confirmed that diversity filtering continued to reduce artist repetition in recommendation lists.
* Created a 1-page wireframe for frontend implementation.

## 22/06/2026

* Reorganised the project structure into dedicated backend and frontend folders.
* Moved all FastAPI backend components into the backend directory.
* Updated project imports, configuration and test setup to support the new structure.
* Installed and configured Streamlit as the frontend framework.
* Created a single-page Streamlit frontend based on the previously designed wireframe.
* Connected the frontend to the FastAPI backend using HTTP requests.
* Integrated the frontend with the `/tracks/options` endpoint to dynamically load available genres, moods and artists.
* Added support for selecting one or more genres.
* Added support for selecting a mood.
* Added support for selecting an optional preferred artist.
* Updated the interface label from "Seed Artist" to "Artist You Like (Optional)".
* Implemented recommendation generation through the `/recommend` endpoint.
* Added recommendation cards displaying track title, artist, genre, mood, recommendation score and recommendation explanation.
* Added direct Spotify integration through dynamically generated Spotify search links.
* Implemented "Open in Spotify" buttons for every recommendation.
* Added a dedicated About NextTrack section describing the recommendation approach and stateless recommendation model.
* Improved recommendation explanations to provide clearer and less repetitive reasoning.
* Increased the number of displayed recommendations from 5 to 10 tracks.
* Expanded the music dataset from 250 tracks to 350 tracks.
* Added additional artists, genres and moods to improve recommendation diversity and coverage.
* Removed the Spotify URL column from the dataset and replaced it with dynamic Spotify link generation.
* Fixed dataset quality issues and corrected invalid genre values.
* Removed duplicate dataset headers introduced during dataset expansion.
* Updated dataset validation tests to reflect the new dataset structure.
* Verified that the frontend and backend worked correctly together as a complete end-to-end system.
* Verified that recommendation generation continued to perform correctly after dataset expansion.
* Verified that all 17 automated tests passed successfully after the updates.
* Updated project documentation and prepared the system for user evaluation and final dissertation work.

## 24/06/2026

* Added dynamic YouTube search link generation for all recommendations.
* Extended recommendation responses to include both Spotify and YouTube external listening links.
* Updated the Streamlit frontend to display Spotify and YouTube search buttons for each recommendation.
* Renamed listening buttons to clearly indicate that they perform external searches rather than direct playback.
* Added expandable recommendation details showing tempo, energy, popularity, danceability, valence and release year.
* Implemented a reset feature allowing users to clear all selected preferences and start a new recommendation session.
* Improved frontend validation and user feedback messages.
* Added an evaluation form to support user testing and recommendation assessment.
* Implemented anonymous evaluation result collection using CSV storage.
* Created a dedicated feedback module to separate evaluation functionality from the main frontend application.
* Added automated tests for evaluation feedback generation and CSV output.
* Increased the automated test suite from 17 to 18 tests.
* Added dataset statistics to the frontend interface.
* Refactored recommendation helper functions into dedicated service modules.
* Created separate services for recommendation explanation generation and external link generation.
* Improved project modularity and reduced coupling between recommendation components.
* Verified that all 18 automated tests passed successfully after refactoring.
* Verified that the FastAPI backend and Streamlit frontend continued to operate correctly after all changes.

# Development Reflection

## What Worked Well

### Automated Testing

One of the most useful improvements during development was introducing automated testing with pytest. Before this, changes had to be checked manually. The project now contains 18 automated tests covering API endpoints, recommendation functionality, dataset validation and evaluation components. The tests made it much easier to verify that new features and refactoring work did not introduce regressions.

### Dataset Expansion

The original prototype contained only a very small number of tracks, which limited recommendation quality and evaluation. Expanding the dataset first to 48 tracks, then to 250 real songs and finally to 350 tracks significantly improved recommendation variety and allowed more realistic testing scenarios. The larger dataset also provided a wider range of genres, moods and artists.

### Recommendation Performance

Despite increasing the dataset size substantially, the recommendation engine remained very fast. Evaluation results showed that recommendations could still be generated in a fraction of a second, indicating that the cosine similarity approach is efficient for the current project scale.

### Diversity Filtering

The diversity filtering mechanism continued to perform well throughout development. Recommendation lists contained a wider range of artists and genres while avoiding excessive repetition. This supports one of the key objectives of the project, which is to reduce repetitive recommendation behaviour.

### Baseline Comparison

Adding a baseline recommender provided a useful point of comparison. The baseline used only genre matching and popularity ranking, while NextTrack used cosine similarity and diversity filtering. The comparison results showed that NextTrack generally produced recommendations from more unique artists and reduced artist repetition compared to the baseline approach.

### API Improvements

The API evolved significantly during development. In addition to the recommendation endpoint, a new endpoint was added to provide available genres, moods and artists directly from the dataset. This functionality supports the frontend by allowing dropdown menus and other interface components to be populated dynamically.

### Evaluation Framework

The evaluation framework became much stronger than the original prototype implementation. Additional evaluation sessions, comparison metrics, relevance metrics and CSV result generation were added. This provided a more comprehensive understanding of recommendation performance and system behaviour.

### Interface Design and Planning

A low-fidelity wireframe was created before frontend development began. This helped visualise the recommendation workflow, simplify the user interface and ensure that the frontend remained aligned with the project requirements.

### Frontend Development

A Streamlit frontend was added to provide a simple user interface for the recommendation system. Users can select genres, moods and an optional artist before generating recommendations. The interface focuses on the core recommendation workflow and intentionally excludes user accounts, playlists and authentication.

### Full System Integration

The project evolved from a standalone backend API into a complete application. The frontend communicates with the FastAPI backend, retrieves available options from the dataset and displays recommendations through a user-friendly interface.

### User Evaluation Infrastructure

An evaluation form was added to collect anonymous user feedback on recommendation quality, diversity, usability and overall satisfaction. Feedback is stored in CSV format, providing evaluation data without requiring databases or user accounts.

### Frontend Usability Improvements

Several usability improvements were added to the Streamlit frontend. Users can now reset recommendation inputs, view additional track metadata through expandable detail panels and access external Spotify and YouTube search links directly from recommendation results. These additions improved the overall user experience while maintaining the simplicity of the interface.

### Software Engineering Improvements

The project structure was further improved through refactoring and modularisation. Recommendation explanation generation and external link generation were moved into dedicated service modules, reducing coupling within the recommendation engine and improving maintainability. Separating frontend feedback functionality into its own module also improved code organisation and readability. Automated testing confirmed that these structural improvements did not introduce regressions.

## Challenges and Limitations

### Dataset Size

Although the dataset was expanded to 350 tracks, it remains very small compared to commercial music recommendation systems that operate on millions of tracks. This limits recommendation variety and makes large-scale evaluation impossible within the scope of the project.

### Measuring Recommendation Quality

Technical metrics such as response time, diversity and recommendation relevance can be measured relatively easily. However, determining whether recommendations are genuinely enjoyable or useful remains difficult because music preferences are highly subjective and vary significantly between users.

### Limited User Evaluation

Current evaluation has focused primarily on automated testing and predefined test sessions. While this provides useful technical evidence, it does not fully represent how real users would interact with the system. User evaluation will be an important part of the next development stage.

### Simple Recommendation Approach

The cosine similarity recommendation approach was chosen because it is relatively simple to implement, explain and evaluate. While suitable for the project scope, it is significantly less sophisticated than recommendation systems used by commercial music platforms, which typically make use of much larger datasets and advanced machine learning techniques.

### Recommendation Explainability

Although recommendation explanations improve transparency, the explanations remain relatively simple. They are generated using predefined rules rather than deeper analysis of recommendation decisions. As a result, different recommendations may occasionally receive similar explanations despite being selected for different reasons.

### Stateless Design Trade-offs

A key design objective of NextTrack was to remain completely stateless. This reduces complexity, improves privacy and simplifies implementation. However, it also means that the system cannot learn from previous user interactions or adapt recommendations over time. Recommendations are generated solely from the current session inputs and therefore provide less personalisation than systems that maintain long-term user profiles.

### External Music Access Limitations

Providing direct music playback proved challenging because the project intentionally avoids storing copyrighted audio files and does not use authenticated third-party music APIs. As a result, Spotify and YouTube integration was implemented using dynamically generated search links rather than direct playback functionality. While this approach allows users to easily locate recommended tracks, it does not provide a fully integrated listening experience.

## Remaining Work

The remaining work will focus on expanding user evaluation, analysing evaluation results, collecting dissertation evidence and screenshots, and updating the final dissertation to reflect the completed implementation and findings.