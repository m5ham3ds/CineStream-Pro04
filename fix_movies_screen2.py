import re
with open('app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt', 'r') as f:
    text = f.read()

text = text.replace("uiState.movies.take(5)", "uiState.movies.take(10)")

popular_section = """        // Popular Movies"""

upcoming_section = """
        // Coming Soon Movies
        if (uiState.upcomingMovies.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.coming_soon), onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(uiState.upcomingMovies) { movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        rating = movie.rating,
                        year = movie.releaseDate?.take(4) ?: "2024",
                        mediaId = movie.id,
                        onClick = { onMovieClick(movie.id) },
                        onLongClick = { 
                            selectedMediaId = movie.id
                            selectedMediaTitle = movie.title
                            selectedMediaPoster = movie.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // Popular Movies"""

text = text.replace(popular_section, upcoming_section)
with open('app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt', 'w') as f:
    f.write(text)
print("Fixed MoviesScreen!")
