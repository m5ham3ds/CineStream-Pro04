import re

with open('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt', 'r') as f:
    text = f.read()

# Extract from if (selectedCategory == "Home") { to } else {
start_marker = '        if (selectedCategory == "Home") {'
end_marker = '} else {'

start_idx = text.find(start_marker)
end_idx = text.find(end_marker, start_idx)

if start_idx != -1 and end_idx != -1:
    new_sections = """        if (selectedCategory == "Home") {
        // 1. Continue Watching
        if (historyItems.isNotEmpty()) {
            SectionTitle(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(historyItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        if (item.isMovie) onMovieClick(item.id) else onSeriesClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // 2. Trending Now
        if (uiState.trendingMovies.isNotEmpty() || uiState.trendingSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.trending_now), onSeeAllClick = onNavigateToTrending)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.trendingMovies.take(5) + uiState.trendingSeries.map { 
                    Movie(id = it.id, title = it.title, overview = it.overview, posterUrl = it.posterUrl, backdropUrl = it.backdropUrl, year = it.year, rating = it.rating, genres = it.genres, runtime = 0)
                }.take(5)).shuffled()
                itemsIndexed(mix) { index, item ->
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = index + 1,
                        rating = item.rating,
                        year = item.year.toString(),
                        mediaId = item.id,
                        onClick = { onMovieClick(item.id) }, // Assuming fallback to movie click for mix, or we could just use movie/series distinction if we saved it. To keep it simple:
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // 3. New Releases
        if (uiState.newReleasesMovies.isNotEmpty() || uiState.newReleasesSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.newReleasesMovies.take(10) + uiState.newReleasesSeries.map { 
                    Movie(id = it.id, title = it.title, overview = it.overview, posterUrl = it.posterUrl, backdropUrl = it.backdropUrl, year = it.year, rating = it.rating, genres = it.genres, runtime = 0)
                }.take(10)).shuffled()
                itemsIndexed(mix) { index, item ->
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = 0,
                        rating = item.rating,
                        year = item.year.toString(),
                        onClick = { onMovieClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // 4. Trending Movies
        if (uiState.trendingMovies.isNotEmpty()) {
            SectionTitle(stringResource(R.string.trending_movies), onSeeAllClick = onNavigateToTrending)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.trendingMovies) { index, movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        rank = 0,
                        rating = movie.rating,
                        year = movie.year.toString(),
                        mediaId = movie.id,
                        onClick = { onMovieClick(movie.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
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

        // 5. Trending Series
        if (uiState.trendingSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.trending_series), onSeeAllClick = onNavigateToTrending)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.trendingSeries) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = 0,
                        rating = series.rating,
                        year = "${series.seasons.size} Seasons",
                        isMovie = false,
                        mediaId = series.id,
                        onClick = { onSeriesClick(series.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // 6. Trending Anime
        if (uiState.animeSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.trending_anime), onSeeAllClick = onNavigateToAnime)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.animeSeries) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = 0,
                        rating = series.rating,
                        year = series.year.toString(),
                        isMovie = false,
                        mediaId = series.id,
                        onClick = { onSeriesClick(series.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

"""
    text = text[:start_idx] + new_sections + text[end_idx:]
    with open('app/src/main/java/com/example/ui/screens/home/HomeScreen.kt', 'w') as f:
        f.write(text)
    print("Rewrote home sections successfully!")
else:
    print("Could not find start or end marker.")
