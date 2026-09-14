import re
with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    text = f.read()

# Add java.time.LocalDate at the top if not present
if "import java.time.LocalDate" not in text:
    text = text.replace("import com.example.domain.models.PersonDetails", "import com.example.domain.models.PersonDetails\nimport java.time.LocalDate")

# We have hardcoded dates like minDate = "2026-09-11" and maxDate = "2026-10-11"
# Let's replace them with dynamic dates.
# val today = LocalDate.now().toString()
# val nextMonth = LocalDate.now().plusMonths(1).toString()

text = re.sub(r'minDate\s*=\s*"2026-09-11"', r'minDate = LocalDate.now().toString()', text)
text = re.sub(r'maxDate\s*=\s*"2026-10-11"', r'maxDate = LocalDate.now().plusMonths(1).toString()', text)

# For upcoming movies, we should also filter out movies that are already released, 
# because TMDB's movie/upcoming sometimes includes recently released movies.
# Actually, the user says "اجد فيها اعمال تم عرضها بل فعل و لكنها لا تزال موجودة داخل قسم ستعرض قريبآ".
# So let's add a filter for upcoming movies: filter { (it.releaseDate ?: "") > LocalDate.now().toString() }
# Replace `emit(response.results.map { it.toDomain() })` in getUpcomingMovies
text = text.replace(
    'override fun getUpcomingMovies(): Flow<List<Movie>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)\n        emit(response.results.map { it.toDomain() })\n    }',
    'override fun getUpcomingMovies(): Flow<List<Movie>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)\n        val today = LocalDate.now().toString()\n        emit(response.results.filter { (it.releaseDate ?: "") > today }.map { it.toDomain() })\n    }'
)

# Also apply filter for getUpcomingSeries and getUpcomingAnime
text = text.replace(
    'override fun getUpcomingSeries(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = LocalDate.now().toString())\n        emit(response.results.map { it.toDomain() })\n    }',
    'override fun getUpcomingSeries(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = LocalDate.now().toString())\n        val today = LocalDate.now().toString()\n        emit(response.results.filter { (it.firstAirDate ?: "") > today }.map { it.toDomain() })\n    }'
)

text = text.replace(
    'override fun getUpcomingAnime(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = LocalDate.now().toString())\n        emit(response.results.map { it.toDomain() })\n    }',
    'override fun getUpcomingAnime(): Flow<List<Series>> = flow {\n        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = LocalDate.now().toString())\n        val today = LocalDate.now().toString()\n        emit(response.results.filter { (it.firstAirDate ?: "") > today }.map { it.toDomain() })\n    }'
)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(text)

