import re
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

target = """        // 6. Trending Anime
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
        }"""

replacement = """        // 6. Trending Anime
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

        // 7. Coming Soon
        if (uiState.upcomingMovies.isNotEmpty() || uiState.upcomingSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.coming_soon), onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.upcomingMovies.take(10) + uiState.upcomingSeries.map { 
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
        }"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
