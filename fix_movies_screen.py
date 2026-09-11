import re
with open('app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt', 'r') as f:
    text = f.read()

# Update banner to take 10
text = text.replace("uiState.movies.take(5)", "uiState.movies.take(10)")

# Add Upcoming Movies section after Popular Movies
popular_section = """        SectionTitleShared(stringResource(R.string.popular_movies), onSeeAllClick = onNavigateToPopular)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.movies) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = index + 1,
                    rating = 8.7 - (index * 0.1),
                    year = "2024",
                    mediaId = movie.id,
                            onClick = { onMovieClick(movie.id) },
                    modifier = Modifier.width(140.dp)
                )
            }
        }"""

upcoming_section = """
        Spacer(modifier = Modifier.height(24.dp))
        
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
                        modifier = Modifier.width(140.dp)
                    )
                }
            }
        }
"""

if popular_section in text:
    text = text.replace(popular_section, popular_section + upcoming_section)
    with open('app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt', 'w') as f:
        f.write(text)
    print("Fixed MoviesScreen!")
else:
    print("Could not find popular section in MoviesScreen")
