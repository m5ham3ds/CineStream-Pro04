import re
with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

target = """        if (selectedCategory == animeStr) {
            if (animeHistoryItems.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(animeHistoryItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        onAnimeClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
        // Coming Soon Anime
        if (uiState.upcomingAnime.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.coming_soon), onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(uiState.upcomingAnime) { series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rating = series.rating,
                        year = series.firstAirDate?.take(4) ?: "2024",
                        isMovie = false,
                        mediaId = series.id,
                        onClick = { onAnimeClick(series.id) },
                        onLongClick = { 
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        },
                        modifier = Modifier.width(140.dp)
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }
        // Popular Anime
        SectionTitleShared(stringResource(R.string.popular_anime), onSeeAllClick = onNavigateToPopular)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.series) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = index + 1,
                    rating = 8.7 - (index * 0.1),
                    year = "2024",
                    isMovie = false,
                    mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                    onLongClick = { 
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
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
            itemsIndexed(uiState.series.reversed()) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = null, // No rank for new releases
                    rating = 8.5,
                    year = "2024",
                    isMovie = false,
                    mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                    onLongClick = { 
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }
"""

replacement = """        if (selectedCategory == animeStr) {
            if (animeHistoryItems.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(animeHistoryItems) { item ->
                        ContinueWatchingCardShared(item = item) {
                            onAnimeClick(item.id)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Trending Anime
            if (uiState.trendingAnime.isNotEmpty()) {
                SectionTitleShared("Trending Anime", onSeeAllClick = onNavigateToTrending)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.trendingAnime) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
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

            // New Releases
            if (uiState.newEpisodes.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.newEpisodes) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rank = null,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
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

            // Popular Anime
            SectionTitleShared(stringResource(R.string.popular_anime), onSeeAllClick = onNavigateToPopular)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.series) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = index + 1,
                        rating = series.rating,
                        year = "2024",
                        isMovie = false,
                        mediaId = series.id,
                        onClick = { onAnimeClick(series.id) },
                        onLongClick = { 
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))

            // Coming Soon Anime
            if (uiState.upcomingAnime.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.coming_soon), onSeeAllClick = {})
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.upcomingAnime) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
                                selectedMediaId = series.id
                                selectedMediaTitle = series.title
                                selectedMediaPoster = series.posterUrl
                                showBottomSheet = true
                            },
                            modifier = Modifier.width(140.dp)
                        )
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
"""

with open("temp_anime.txt", "r") as f:
    target = f.read()
    
target = target.split("}} else {")[0]

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
    f.write(content)
