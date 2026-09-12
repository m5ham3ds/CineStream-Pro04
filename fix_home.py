with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()

target = """        // 7. Coming Soon
        if (uiState.upcomingMovies.isNotEmpty() || uiState.upcomingSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.coming_soon), onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.upcomingMovies.take(10) + uiState.upcomingSeries.map { 
                    Movie(id = it.id, title = it.title, overview = it.overview, posterUrl = it.posterUrl, backdropUrl = it.backdropUrl, year = it.year, rating = it.rating, genres = it.genres, runtime = 0)
                }.take(10)).shuffled()"""

replacement = """        // 7. Coming Soon
        if (uiState.upcomingMovies.isNotEmpty()) {
            SectionTitle(stringResource(R.string.coming_soon), onSeeAllClick = {})
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = uiState.upcomingMovies.take(10).shuffled()"""

content = content.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write(content)
