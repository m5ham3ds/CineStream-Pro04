import re

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    text = f.read()

# Add missing fields to HomeUiState
state_additions = """    val trendingAnime: List<Series> = emptyList(),
    val popularMovies: List<Movie> = emptyList(),
    val popularSeries: List<Series> = emptyList(),
    val popularAnime: List<Series> = emptyList(),
    val upcomingSeries: List<Series> = emptyList(),
    val upcomingAnime: List<Series> = emptyList(),
    val newReleasesAnime: List<Series> = emptyList(),"""

text = text.replace(
    'val animeSeries: List<Series> = emptyList(),',
    'val animeSeries: List<Series> = emptyList(),\n' + state_additions
)

# Update loadData in HomeViewModel
load_data_additions = """
                val trendingAnimeDeferred = async { repository.getTrendingAnime().firstOrNull() ?: emptyList() }
                val popularMoviesDeferred = async { repository.getPopularMovies().firstOrNull() ?: emptyList() }
                val popularSeriesDeferred = async { repository.getPopularSeries().firstOrNull() ?: emptyList() }
                val popularAnimeDeferred = async { repository.getPopularAnime().firstOrNull() ?: emptyList() }
                val upcomingSeriesDeferred = async { repository.getUpcomingSeries().firstOrNull() ?: emptyList() }
                val upcomingAnimeDeferred = async { repository.getUpcomingAnime().firstOrNull() ?: emptyList() }
                val newReleasesAnimeDeferred = async { repository.getNewReleasesAnime().firstOrNull() ?: emptyList() }
"""
text = text.replace('val allMoviesDeferred = async { repository.getMovies().firstOrNull() ?: emptyList() }', load_data_additions.strip() + '\n                val allMoviesDeferred = async { repository.getMovies().firstOrNull() ?: emptyList() }')

await_additions = """
                val trendingAnime = trendingAnimeDeferred.await()
                val popularMoviesRaw = popularMoviesDeferred.await()
                val popularSeriesRaw = popularSeriesDeferred.await()
                val popularAnime = popularAnimeDeferred.await()
                val upcomingSeriesRaw = upcomingSeriesDeferred.await()
                val upcomingAnime = upcomingAnimeDeferred.await()
                val newReleasesAnime = newReleasesAnimeDeferred.await()
"""
text = text.replace('val allMoviesRaw = allMoviesDeferred.await()', await_additions.strip() + '\n                val allMoviesRaw = allMoviesDeferred.await()')

copy_additions = """
                    trendingAnime = trendingAnime,
                    popularMovies = popularMoviesRaw,
                    popularSeries = popularSeriesRaw,
                    popularAnime = popularAnime,
                    upcomingSeries = upcomingSeriesRaw,
                    upcomingAnime = upcomingAnime,
                    newReleasesAnime = newReleasesAnime,
"""
text = text.replace('animeSeries = animeSeries,', 'animeSeries = animeSeries,\n' + copy_additions.strip() + ',')

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(text)
