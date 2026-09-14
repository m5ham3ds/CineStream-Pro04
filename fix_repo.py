import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    repo_content = f.read()

repo_content = re.sub(
    r"val response = RetrofitClient\.tmdbApi\.getUpcomingMovies\(apiKey\)",
    "val response = RetrofitClient.tmdbApi.getUpcomingMoviesDiscover(apiKey, minDate = LocalDate.now().toString())",
    repo_content
)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(repo_content)

