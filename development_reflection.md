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

# Development Reflection

## What Worked Well

### Automated Testing

One of the most useful improvements was adding automated testing with pytest. Before this, changes had to be checked manually. Creating 10 automated tests made it easier to verify that the API and recommendation engine were still working correctly after modifications. All tests passed after the new features were implemented.

### Dataset Expansion

The original prototype only contained 8 tracks, which limited the variety of recommendations that could be generated. Expanding the dataset to 48 tracks improved recommendation variety and made evaluation more meaningful. The larger dataset also allowed more realistic testing scenarios.

### Recommendation Performance

Even after increasing the dataset size, the recommendation engine remained very fast. Response times across the evaluation sessions were all well below one second, showing that the system can generate recommendations efficiently.

### Diversity Filtering

The diversity filtering mechanism worked as expected during testing. Recommendation lists contained a wider range of artists and genres and avoided excessive repetition. This supports one of the main goals of the project, which is to reduce repetitive recommendations.

### Baseline Comparison

Adding a simple baseline recommender was useful because it provided something to compare NextTrack against. The baseline used only genre matching and popularity ranking, while NextTrack used cosine similarity and diversity filtering. The comparison showed that NextTrack produced recommendations from more unique artists and reduced repetition compared to the baseline approach.

### Recommendation Relevance

The evaluation framework was extended to measure recommendation relevance. The results showed a mood match rate of 1.0 and a genre match rate of 0.6 across the evaluation sessions. This suggests that recommendations generally matched the requested mood while still allowing some variation in genre to improve diversity.

### Recommendation Explainability

A recommendation explanation feature was added to make the system more transparent. Each recommendation now includes a short explanation describing why it was selected. Although the explanations are simple, they make it easier to understand how recommendations are generated.

### Evaluation Framework

The evaluation framework became much stronger than the one used in the prototype. The number of evaluation sessions increased from three to eight, additional metrics were added, and results could be exported to CSV files for further analysis.

## Challenges and Limitations

### Small Dataset

Although the dataset was expanded, it is still very small compared to real-world music recommendation systems. This limits the variety of recommendations that can be generated and makes it difficult to evaluate behaviour at a larger scale.

### Measuring Recommendation Quality

Technical metrics such as response time, diversity and relevance can be measured relatively easily. However, determining whether recommendations are genuinely good is much more difficult because music preferences are highly subjective.

### Project Structure Issues

Some time was spent fixing Python environment and import path issues while setting up testing and evaluation scripts. These problems were eventually resolved, but they slowed down development and highlighted weaknesses in the project structure.

### Limited Evaluation Scope

The evaluation mainly focused on predefined test sessions and automated testing. While this provided useful technical evidence, it does not fully represent how a wider group of users might interact with the system.

### Simple Recommendation Algorithm

The cosine similarity approach was suitable for the scope of this project because it is relatively simple to implement and explain. However, it is much less sophisticated than recommendation systems used by commercial music platforms, which typically make use of very large datasets and advanced machine learning techniques.
