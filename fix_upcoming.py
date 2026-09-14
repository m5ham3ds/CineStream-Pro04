import re
with open("app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt", "r") as f:
    text = f.read()

text = text.replace('seriesStr -> uiState.trendingSeries.map { it to false }', 'seriesStr -> uiState.upcomingSeries.map { it to false }')
text = text.replace('animeStr -> uiState.animeSeries.map { it to false }', 'animeStr -> uiState.upcomingAnime.map { it to false }')
text = text.replace('else -> (uiState.upcomingMovies.map { it to true } + uiState.trendingSeries.map { it to false } + uiState.animeSeries.map { it to false })', 'else -> (uiState.upcomingMovies.map { it to true } + uiState.upcomingSeries.map { it to false } + uiState.upcomingAnime.map { it to false })')

with open("app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt", "w") as f:
    f.write(text)
