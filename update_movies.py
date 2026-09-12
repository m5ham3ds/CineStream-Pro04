import re
with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
    content = f.read()

target = """        if (selectedCategory == "Movies") {if (movieHistoryItems.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(movieHistoryItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        onMovieClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
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
        // Popular Movies
        SectionTitleShared(stringResource(R.string.popular_movies), onSeeAllClick = onNavigateToPopular)
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
        // New Releases
        SectionTitleShared(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.movies.reversed()) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = null, // No rank for new releases
                    rating = 8.5,
                    year = "2024",
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
        }"""

replacement = """        if (selectedCategory == "Movies") {
            if (movieHistoryItems.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(movieHistoryItems) { item ->
                        ContinueWatchingCardShared(item = item) {
                            onMovieClick(item.id)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Trending Movies
            if (uiState.trendingMovies.isNotEmpty()) {
                SectionTitleShared("Trending Movies", onSeeAllClick = onNavigateToTrending)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.trendingMovies) { movie ->
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

            // New Releases
            if (uiState.newReleasesMovies.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.newReleasesMovies) { movie ->
                        MediaCard(
                            title = movie.title,
                            posterUrl = movie.posterUrl,
                            rank = null,
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

            // Popular Movies
            SectionTitleShared(stringResource(R.string.popular_movies), onSeeAllClick = onNavigateToPopular)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.movies) { index, movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        rank = index + 1,
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
"""

with open("temp_movies.txt", "r") as f:
    target = f.read()

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "w") as f:
    f.write(content)
