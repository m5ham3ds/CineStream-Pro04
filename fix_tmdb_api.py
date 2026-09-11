import re

with open('app/src/main/java/com/example/data/remote/TmdbApiService.kt', 'r') as f:
    text = f.read()

inject_point = "    // Search"
new_endpoints = """
    @GET("discover/tv")
    suspend fun getUpcomingSeriesDiscover(
        @Query("api_key") apiKey: String,
        @Query("without_genres") withoutGenres: String = "16",
        @Query("sort_by") sortBy: String = "popularity.desc",
        @Query("first_air_date.gte") minDate: String
    ): TmdbResponse<TmdbSeries>

    @GET("discover/tv")
    suspend fun getUpcomingAnimeDiscover(
        @Query("api_key") apiKey: String,
        @Query("with_genres") withGenres: String = "16",
        @Query("with_original_language") withOriginalLanguage: String = "ja",
        @Query("sort_by") sortBy: String = "popularity.desc",
        @Query("first_air_date.gte") minDate: String
    ): TmdbResponse<TmdbSeries>

    @GET("discover/tv")
    suspend fun getAiringTodayAnime(
        @Query("api_key") apiKey: String,
        @Query("with_genres") withGenres: String = "16",
        @Query("with_original_language") withOriginalLanguage: String = "ja",
        @Query("sort_by") sortBy: String = "popularity.desc",
        @Query("air_date.gte") minDate: String,
        @Query("air_date.lte") maxDate: String
    ): TmdbResponse<TmdbSeries>

"""

if inject_point in text:
    text = text.replace(inject_point, new_endpoints + inject_point)
    with open('app/src/main/java/com/example/data/remote/TmdbApiService.kt', 'w') as f:
        f.write(text)
    print("Added Upcoming endpoints to API Service!")
else:
    print("Could not find inject point.")
