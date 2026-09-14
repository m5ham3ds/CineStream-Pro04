import re

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

# Make sure LocalDate is imported
if "import java.time.LocalDate" not in text:
    text = text.replace("import com.example.domain.models.PersonDetails", "import com.example.domain.models.PersonDetails\nimport java.time.LocalDate")

# Upcoming Movies filter
upcoming_movies_old = """    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)
        emit(response.results.map { it.toDomain() })
    }"""
upcoming_movies_new = """    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)
        val today = LocalDate.now().toString()
        emit(response.results.filter { (it.releaseDate ?: "") > today }.map { it.toDomain() })
    }"""
text = text.replace(upcoming_movies_old, upcoming_movies_new)

# Upcoming Series filter
upcoming_series_old = """    override fun getUpcomingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = "2026-09-11")
        emit(response.results.map { it.toDomain() })
    }"""
upcoming_series_old2 = """    override fun getUpcomingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = LocalDate.now().toString())
        emit(response.results.map { it.toDomain() })
    }"""
upcoming_series_new = """    override fun getUpcomingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = LocalDate.now().toString())
        val today = LocalDate.now().toString()
        emit(response.results.filter { (it.firstAirDate ?: "") > today }.map { it.toDomain() })
    }"""
text = text.replace(upcoming_series_old, upcoming_series_new)
text = text.replace(upcoming_series_old2, upcoming_series_new)

# Upcoming Anime filter
upcoming_anime_old = """    override fun getUpcomingAnime(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = "2026-09-11")
        emit(response.results.map { it.toDomain() })
    }"""
upcoming_anime_old2 = """    override fun getUpcomingAnime(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = LocalDate.now().toString())
        emit(response.results.map { it.toDomain() })
    }"""
upcoming_anime_new = """    override fun getUpcomingAnime(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = LocalDate.now().toString())
        val today = LocalDate.now().toString()
        emit(response.results.filter { (it.firstAirDate ?: "") > today }.map { it.toDomain() })
    }"""
text = text.replace(upcoming_anime_old, upcoming_anime_new)
text = text.replace(upcoming_anime_old2, upcoming_anime_new)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

