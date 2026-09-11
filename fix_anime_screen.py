import re
with open('app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt', 'r') as f:
    text = f.read()

# Fix Banner
text = text.replace("uiState.series.take(5)", "uiState.newEpisodes.take(10)")

popular_section = """        // Popular Anime"""

upcoming_section = """
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

        // Popular Anime"""

text = text.replace(popular_section, upcoming_section)
with open('app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt', 'w') as f:
    f.write(text)
print("Fixed AnimeScreen!")
