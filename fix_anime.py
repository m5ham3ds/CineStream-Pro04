import re

with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "r") as f:
    content = f.read()

# Find the start of "// Coming Soon Anime"
start_idx = content.find("            // Coming Soon Anime")
# Find the start of "if (showBottomSheet) {"
end_idx = content.find("if (showBottomSheet) {")

if start_idx != -1 and end_idx != -1:
    replacement = """            // Coming Soon Anime
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
        } else {
            val displayItems = when (selectedCategory) {
                stringResource(R.string.new_releases) -> uiState.series.reversed()
                "Top Rated" -> uiState.series.sortedByDescending { it.rating }
                "Genres" -> uiState.series.shuffled()
                else -> uiState.series
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { series ->
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
    }
    }
"""
    new_content = content[:start_idx] + replacement + content[end_idx:]
    with open("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "w") as f:
        f.write(new_content)
    print("Fixed AnimeScreen.kt")
else:
    print("Could not find boundaries in AnimeScreen.kt")
