import re

with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "val upcomingMovies = (upcomingMoviesRaw.take(10) + arabicMoviesRaw.take(10)).sortedByDescending { it.rating }.distinctBy { it.id }",
    "val upcomingMovies = upcomingMoviesRaw.sortedByDescending { it.rating }.distinctBy { it.id }"
)
with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "repository.getUpcomingMovies().combine(repository.getArabicMovies()) { upcoming, arabic ->\n                    (upcoming.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }\n                }",
    "repository.getUpcomingMovies().map { upcoming ->\n                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }\n                }"
)
with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "r") as f:
    content = f.read()

content = content.replace(
    "repository.getUpcomingSeries().combine(repository.getArabicSeries()) { upcoming, arabic ->\n                    (upcoming.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }\n                }",
    "repository.getUpcomingSeries().map { upcoming ->\n                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }\n                }"
)
with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "w") as f:
    f.write(content)

