import re

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "r") as f:
    content = f.read()

new_api = """
    @GET("discover/movie")
    suspend fun getUpcomingMoviesDiscover(
        @Query("api_key") apiKey: String,
        @Query("sort_by") sortBy: String = "popularity.desc",
        @Query("primary_release_date.gte") minDate: String
    ): TmdbResponse<TmdbMovie>
"""
content = content.replace('@GET("movie/upcoming")\n    suspend fun getUpcomingMovies(\n        @Query("api_key") apiKey: String\n    ): TmdbResponse<TmdbMovie>', new_api.strip())

with open("app/src/main/java/com/example/data/remote/TmdbApiService.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "r") as f:
    repo_content = f.read()

old_repo = """    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)
        val today = LocalDate.now().toString()
        emit(response.results.filter { (it.releaseDate ?: "") > today }.map { it.toDomain() })
    }.catch {
        emit(emptyList())
    }"""
new_repo = """    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingMoviesDiscover(apiKey, minDate = LocalDate.now().toString())
        val today = LocalDate.now().toString()
        emit(response.results.filter { (it.releaseDate ?: "") > today }.map { it.toDomain() })
    }.catch {
        emit(emptyList())
    }"""
repo_content = repo_content.replace(old_repo, new_repo)

with open("app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt", "w") as f:
    f.write(repo_content)

