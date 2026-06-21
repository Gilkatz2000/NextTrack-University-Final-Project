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

# Development Reflection

## What Worked Well

### Automated Testing

One of the most useful improvements during development was introducing automated testing with pytest. Before this, changes had to be checked manually. The project now contains 17 automated tests covering API endpoints, recommendation functionality, dataset validation and evaluation components. The tests made it much easier to verify that new features and refactoring work did not introduce regressions.

### Dataset Expansion

The original prototype contained only a very small number of tracks, which limited recommendation quality and evaluation. Expanding the dataset first to 48 tracks and later to 250 real songs significantly improved recommendation variety and allowed more realistic testing scenarios. The larger dataset also provided a wider range of genres, moods and artists.

### Recommendation Performance

Despite increasing the dataset size substantially, the recommendation engine remained very fast. Evaluation results showed that recommendations could still be generated in a fraction of a second, indicating that the cosine similarity approach is efficient for the current project scale.

### Diversity Filtering

The diversity filtering mechanism continued to perform well throughout development. Recommendation lists contained a wider range of artists and genres while avoiding excessive repetition. This supports one of the key objectives of the project, which is to reduce repetitive recommendation behaviour.

### Baseline Comparison

Adding a baseline recommender provided a useful point of comparison. The baseline used only genre matching and popularity ranking, while NextTrack used cosine similarity and diversity filtering. The comparison results showed that NextTrack generally produced recommendations from more unique artists and reduced artist repetition compared to the baseline approach.

### Recommendation Explainability

A recommendation explanation feature was added to improve transparency. Each recommendation now includes a short explanation describing why it was selected. Although the explanations are relatively simple, they help users understand the reasoning behind recommendations and improve the interpretability of the system.

### API Improvements

The API evolved significantly during development. In addition to the recommendation endpoint, a new endpoint was added to provide available genres, moods and artists directly from the dataset. This functionality will support the planned frontend by allowing dropdown menus and other interface components to be populated dynamically.

### Project Organisation

The project structure improved considerably during development. A dedicated data folder, reusable data loading component and results folder were introduced. Consolidating the project around a single dataset source reduced duplication and made the codebase easier to maintain.

### Evaluation Framework

The evaluation framework became much stronger than the original prototype implementation. Additional evaluation sessions, comparison metrics, relevance metrics and CSV result generation were added. This provided a more comprehensive understanding of recommendation performance and system behaviour.

### Interface Design and Planning

As the backend implementation approached completion, attention shifted towards frontend planning. A low-fidelity single-page wireframe was created to visualise how users would interact with the recommendation system. The wireframe focused on the core workflow of selecting preferences, generating recommendations and opening tracks in Spotify. Creating the wireframe helped identify opportunities to simplify the interface and ensure that the planned frontend remained aligned with the actual project requirements. The wireframe will also serve as a design artefact for the final dissertation and as a guide during frontend implementation.

## Challenges and Limitations

### Dataset Size

Although the dataset was expanded to 250 tracks, it remains very small compared to commercial music recommendation systems that operate on millions of tracks. This limits recommendation variety and makes large-scale evaluation impossible within the scope of the project.

### Measuring Recommendation Quality

Technical metrics such as response time, diversity and recommendation relevance can be measured relatively easily. However, determining whether recommendations are genuinely enjoyable or useful remains difficult because music preferences are highly subjective and vary significantly between users.

### Refactoring Complexity

Expanding the dataset required changes across multiple components of the system. Recommendation models, evaluation scripts, API responses and automated tests all needed to be updated. Although the refactoring was successful, it increased development effort and required careful validation.

### Limited User Evaluation

Current evaluation has focused primarily on automated testing and predefined test sessions. While this provides useful technical evidence, it does not fully represent how real users would interact with the system. User evaluation will be an important part of the next development stage.

### Simple Recommendation Approach

The cosine similarity recommendation approach was chosen because it is relatively simple to implement, explain and evaluate. While suitable for the project scope, it is significantly less sophisticated than recommendation systems used by commercial music platforms, which typically make use of much larger datasets and advanced machine learning techniques.

## Remaining Work

The backend implementation is now largely complete and considered feature complete for the current project scope. The next major development stage will focus on creating a frontend interface, conducting user evaluations and updating the final dissertation to reflect the completed implementation.
