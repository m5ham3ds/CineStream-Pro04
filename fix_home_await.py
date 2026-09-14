import re
with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    text = f.read()

# Add missing awaits
missing_awaits = """                val trendingAnime = trendingAnimeDeferred.await()
                val popularMoviesRaw = popularMoviesDeferred.await()
                val popularSeriesRaw = popularSeriesDeferred.await()
                val popularAnime = popularAnimeDeferred.await()
                val upcomingSeriesRaw = upcomingSeriesDeferred.await()
                val upcomingAnime = upcomingAnimeDeferred.await()
                val newReleasesAnime = newReleasesAnimeDeferred.await()
"""
text = text.replace('val arabicSeriesRaw = arabicSeriesDeferred.await()', 'val arabicSeriesRaw = arabicSeriesDeferred.await()\n' + missing_awaits)

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(text)
