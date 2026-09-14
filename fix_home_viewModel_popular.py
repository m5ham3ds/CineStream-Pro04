import re
with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    text = f.read()

text = text.replace('val popularMoviesDeferred = async { repository.getPopularMovies().firstOrNull() ?: emptyList() }', 'val popularMoviesDeferred = async { repository.getMovies().firstOrNull() ?: emptyList() }')
text = text.replace('val popularSeriesDeferred = async { repository.getPopularSeries().firstOrNull() ?: emptyList() }', 'val popularSeriesDeferred = async { repository.getSeries().firstOrNull() ?: emptyList() }')
text = text.replace('val popularAnimeDeferred = async { repository.getPopularAnime().firstOrNull() ?: emptyList() }', 'val popularAnimeDeferred = async { repository.getAnimeSeries().firstOrNull() ?: emptyList() }')

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(text)
