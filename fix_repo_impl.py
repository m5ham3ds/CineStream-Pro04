import re
with open('app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt', 'r') as f:
    text = f.read()

# Filter Anime from getSeries
old_getSeries = """    override fun getSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getPopularSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {"""
new_getSeries = """    override fun getSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getPopularSeries(apiKey)
            emit(response.results.filter { it.genreIds?.contains(16) != true || it.originCountry?.contains("JP") != true }.map { it.toDomain() })
    }.catch {"""
text = text.replace(old_getSeries, new_getSeries)

# Filter Anime from getTrendingSeries
old_getTrendingSeries = """    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getTrendingSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {"""
new_getTrendingSeries = """    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getTrendingSeries(apiKey)
            emit(response.results.filter { it.genreIds?.contains(16) != true || it.originCountry?.contains("JP") != true }.map { it.toDomain() })
    }.catch {"""
text = text.replace(old_getTrendingSeries, new_getTrendingSeries)

# Filter Anime from getNewReleasesSeries
old_getNewReleasesSeries = """    override fun getNewReleasesSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {"""
new_getNewReleasesSeries = """    override fun getNewReleasesSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)
            emit(response.results.filter { it.genreIds?.contains(16) != true || it.originCountry?.contains("JP") != true }.map { it.toDomain() })
    }.catch {"""
text = text.replace(old_getNewReleasesSeries, new_getNewReleasesSeries)

# Add new methods
import datetime
now = datetime.datetime.now()
next_month = now + datetime.timedelta(days=30)
min_date = now.strftime("%Y-%m-%d")
max_date = next_month.strftime("%Y-%m-%d")

new_methods = f"""
    override fun getUpcomingSeries(): Flow<List<Series>> = flow {{
        val response = RetrofitClient.tmdbApi.getUpcomingSeriesDiscover(apiKey, minDate = "{min_date}")
        emit(response.results.map {{ it.toDomain() }})
    }}.catch {{
        emit(emptyList())
    }}

    override fun getUpcomingAnime(): Flow<List<Series>> = flow {{
        val response = RetrofitClient.tmdbApi.getUpcomingAnimeDiscover(apiKey, minDate = "{min_date}")
        emit(response.results.map {{ it.toDomain() }})
    }}.catch {{
        emit(emptyList())
    }}

    override fun getNewReleasesAnime(): Flow<List<Series>> = flow {{
        val response = RetrofitClient.tmdbApi.getAiringTodayAnime(apiKey, minDate = "{min_date}", maxDate = "{max_date}")
        emit(response.results.map {{ it.toDomain() }})
    }}.catch {{
        emit(emptyList())
    }}
"""

inject_point = "    override fun getTrendingSeries()"
text = text.replace(inject_point, new_methods + "\n" + inject_point)

with open('app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt', 'w') as f:
    f.write(text)
print("Updated TmdbMediaRepositoryImpl!")
