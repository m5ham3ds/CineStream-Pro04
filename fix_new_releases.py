import re
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

# Filter New Releases Movies
text = text.replace(
    'override fun getNewReleasesMovies(): Flow<List<Movie>> = flow {\n        val response = RetrofitClient.tmdbApi.getNewReleasesMovies(apiKey)\n        emit(response.results.map { it.toDomain() })\n    }',
    'override fun getNewReleasesMovies(): Flow<List<Movie>> = flow {\n        val response = RetrofitClient.tmdbApi.getNewReleasesMovies(apiKey)\n        val limitDate = LocalDate.now().minusMonths(3).toString()\n        emit(response.results.filter { (it.releaseDate ?: "") >= limitDate }.map { it.toDomain() })\n    }'
)

# Filter New Releases Series
text = text.replace(
    'override fun getNewReleasesSeries(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)\n        emit(response.results.filter { it.genreIds?.contains(16) != true || it.originCountry?.contains("JP") != true }.map { it.toDomain() })\n    }',
    'override fun getNewReleasesSeries(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)\n        val limitDate = LocalDate.now().minusMonths(6).toString()\n        emit(response.results.filter { (it.genreIds?.contains(16) != true || it.originCountry?.contains("JP") != true) && (it.firstAirDate ?: "") >= limitDate }.map { it.toDomain() })\n    }'
)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

