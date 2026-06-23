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

# Development Reflection

## What Worked Well

### Automated Testing

One of the most useful improvements during development was introducing automated testing with pytest. Before this, changes had to be checked manually. The project now contains 17 automated tests covering API endpoints, recommendation functionality, dataset validation and evaluation components. The tests made it much easier to verify that new features and refactoring work did not introduce regressions.

### Dataset Expansion

The original prototype contained only a very small number of tracks, which limited recommendation quality and evaluation. Expanding the dataset first to 48 tracks, then to 250 real songs and finally to 350 tracks significantly improved recommendation variety and allowed more realistic testing scenarios. The larger dataset also provided a wider range of genres, moods and artists.

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

### Frontend Development

A major milestone during this development stage was the implementation of a Streamlit frontend. Previous versions of the project could only be accessed through Swagger or direct API requests. The frontend provides a simple interface that allows users to select genres, moods and a preferred artist before generating recommendations. The interface intentionally focuses on the core recommendation workflow and avoids unnecessary features such as user accounts, playlists or authentication.

### Full System Integration

The project evolved from an isolated backend service into a complete working application. The frontend communicates with the FastAPI backend through HTTP requests, dynamically retrieves available options from the dataset and displays recommendation results in a user-friendly format. This demonstrated that the overall system architecture functions correctly as an integrated solution.

### Dynamic Spotify Integration

Spotify integration was simplified by dynamically generating Spotify search links directly from track and artist information. This approach removed the need to maintain Spotify URLs within the dataset while ensuring that every recommendation can still be opened easily in Spotify.

### Project Structure Improvements

Separating backend and frontend components into dedicated directories improved the organisation of the project. The resulting structure is easier to understand, maintain and extend. This separation also better reflects common web application development practices and improves overall codebase clarity.
## Challenges and Limitations

### Dataset Size

Although the dataset was expanded to 350 tracks, it remains very small compared to commercial music recommendation systems that operate on millions of tracks. This limits recommendation variety and makes large-scale evaluation impossible within the scope of the project.

### Measuring Recommendation Quality

Technical metrics such as response time, diversity and recommendation relevance can be measured relatively easily. However, determining whether recommendations are genuinely enjoyable or useful remains difficult because music preferences are highly subjective and vary significantly between users.

### Refactoring Complexity

Expanding the dataset and reorganising the project structure required changes across multiple components of the system. Recommendation models, evaluation scripts, API responses, automated tests and frontend integration all needed to be updated. Although the refactoring was successful, it increased development effort and required careful validation.

### Limited User Evaluation

Current evaluation has focused primarily on automated testing and predefined test sessions. While this provides useful technical evidence, it does not fully represent how real users would interact with the system. User evaluation will be an important part of the next development stage.

### Simple Recommendation Approach

The cosine similarity recommendation approach was chosen because it is relatively simple to implement, explain and evaluate. While suitable for the project scope, it is significantly less sophisticated than recommendation systems used by commercial music platforms, which typically make use of much larger datasets and advanced machine learning techniques.

### Frontend Simplicity

The frontend was intentionally designed to be simple and focused on demonstrating the recommendation system. While this approach aligns with the project scope, it also means that the user interface lacks many features commonly found in modern music applications. Features such as playlists, listening history, social functionality and personalised user profiles were intentionally excluded to keep the project manageable.

### Dataset Preparation Effort

Expanding the dataset required a significant amount of manual work. Track metadata needed to be collected, validated and formatted consistently across all records. Several data quality issues were encountered during development, including inconsistent values and duplicate headers introduced during dataset expansion. Maintaining data quality became increasingly important as the dataset grew.

### Recommendation Explainability

Although recommendation explanations improve transparency, the explanations remain relatively simple. They are generated using predefined rules rather than deeper analysis of recommendation decisions. As a result, different recommendations may occasionally receive similar explanations despite being selected for different reasons.

### Stateless Design Trade-offs

A key design objective of NextTrack was to remain completely stateless. This reduces complexity, improves privacy and simplifies implementation. However, it also means that the system cannot learn from previous user interactions or adapt recommendations over time. Recommendations are generated solely from the current session inputs and therefore provide less personalisation than systems that maintain long-term user profiles.

### Limited Scale Testing

The project was tested extensively using automated tests and predefined evaluation sessions. However, testing was conducted on a relatively small scale compared to commercial recommendation systems. The application has not been evaluated under large user populations, heavy concurrent traffic or substantially larger datasets. Therefore, performance at larger scales remains uncertain.

### Recommendation Diversity Trade-offs

The diversity filtering mechanism improves recommendation variety by reducing artist repetition and encouraging broader genre coverage. However, increasing diversity can sometimes reduce recommendation relevance because highly similar tracks may be excluded from the final recommendation list. Balancing recommendation relevance and recommendation diversity remains a challenging aspect of recommendation system design.


## Remaining Work

The backend and frontend implementations are now largely complete and considered feature complete for the current project scope. The remaining work will focus on conducting user evaluations, analysing evaluation results, collecting dissertation evidence and screenshots, and updating the final dissertation to reflect the completed implementation and findings.

Future work beyond the project scope could include larger datasets, more advanced recommendation algorithms, user profile support and additional recommendation evaluation techniques. However, these enhancements are not required for the objectives of the current project.
