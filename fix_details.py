import re

# Fix MovieDetailsScreen
with open("app/src/main/java/com/example/ui/screens/details/MovieDetailsScreen.kt", "r") as f:
    movie_content = f.read()

# Replace the "Movie not found" text with the Skeleton
target_movie_error = """        if (movie == null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(stringResource(R.string.movie_not_found), color = MaterialTheme.colorScheme.onBackground)
            }
            return
        }"""
replacement_movie_error = """        if (movie == null) {
            com.example.ui.components.MovieDetailsSkeleton()
            return
        }"""

movie_content = movie_content.replace(target_movie_error, replacement_movie_error)

with open("app/src/main/java/com/example/ui/screens/details/MovieDetailsScreen.kt", "w") as f:
    f.write(movie_content)


# Fix SeriesDetailsScreen
with open("app/src/main/java/com/example/ui/screens/details/SeriesDetailsScreen.kt", "r") as f:
    series_content = f.read()

# Replace the "Series not found" text with the Skeleton
target_series_error = """        if (series == null) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(stringResource(R.string.series_not_found), color = MaterialTheme.colorScheme.onBackground)
            }
            return
        }"""
replacement_series_error = """        if (series == null) {
            com.example.ui.components.MovieDetailsSkeleton() // Reuse movie skeleton since layout is similar
            return
        }"""
        
series_content = series_content.replace(target_series_error, replacement_series_error)

with open("app/src/main/java/com/example/ui/screens/details/SeriesDetailsScreen.kt", "w") as f:
    f.write(series_content)

