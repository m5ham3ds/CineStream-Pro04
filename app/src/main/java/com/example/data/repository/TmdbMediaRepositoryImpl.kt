package com.example.data.repository

import com.example.BuildConfig
import com.example.data.remote.RetrofitClient
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import com.example.domain.models.CastMember
import com.example.domain.models.VideoTrailer
import com.example.domain.models.Season
import com.example.domain.models.Episode
import com.example.domain.models.PersonDetails

class TmdbMediaRepositoryImpl : MediaRepository {
    
    // Fallback to empty string if missing
    private val apiKey = BuildConfig.TMDB_API_KEY


    override fun getUpcomingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getUpcomingMovies(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getAnimeSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getAnimeSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getAnimeMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getAnimeMovies(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getNewReleasesMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getNewReleasesMovies(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getNewReleasesSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getNewReleasesSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getPopularMovies(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getPopularSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getTrendingMovies(): Flow<List<Movie>> = flow {
        val response = RetrofitClient.tmdbApi.getTrendingMovies(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        val response = RetrofitClient.tmdbApi.getTrendingSeries(apiKey)
            emit(response.results.map { it.toDomain() })

    }.catch {
        emit(emptyList())
    }

override suspend fun getMovieById(id: String): Movie? = withContext(Dispatchers.IO) {
        if (id.startsWith("provider|")) {
            val parts = id.split("|")
            val title = parts.getOrNull(2) ?: "Unknown"
            val thumb = parts.getOrNull(3) ?: ""
            return@withContext Movie(
                id = id,
                title = title,
                originalTitle = title,
                overview = "Content from provider ${parts.getOrNull(1)}",
                posterUrl = thumb,
                backdropUrl = thumb,
                year = 2024,
                releaseDate = "2024",
                rating = 0.0,
                genres = emptyList(),
                runtime = 0,
                language = "en",
                cast = emptyList(),
                trailers = emptyList()
            )
        }
        try {
            val response = RetrofitClient.tmdbApi.getMovieDetails(id.toInt(), apiKey)
            response.toDomainDetails()
        } catch (e: Exception) {
            null
        }
    }

override suspend fun getSeriesById(id: String): Series? = withContext(Dispatchers.IO) {
        if (id.startsWith("provider|")) {
            val parts = id.split("|")
            val title = parts.getOrNull(2) ?: "Unknown"
            val thumb = parts.getOrNull(3) ?: ""
            return@withContext Series(
                id = id,
                title = title,
                overview = "Content from provider ${parts.getOrNull(1)}",
                posterUrl = thumb,
                backdropUrl = thumb,
                year = 2024,
                firstAirDate = "2024",
                rating = 0.0,
                genres = emptyList(),
                cast = emptyList(),
                trailers = emptyList(),
                seasons = emptyList(),
                creator = parts.getOrNull(1),
                status = "Unknown"
            )
        }
        try {
            val response = RetrofitClient.tmdbApi.getSeriesDetails(id.toInt(), apiKey)
            response.toDomainDetails()
        } catch (e: Exception) {
            null
        }
    }
    
    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.searchMulti(apiKey, query)
            val movies = mutableListOf<Movie>()
            val series = mutableListOf<Series>()
            
            response.results.forEach { item ->
                if (item.mediaType == "movie") {
                    val yearInt = item.releaseDate?.take(4)?.toIntOrNull() ?: 2024
                    movies.add(Movie(
                        id = item.id.toString(),
                        title = item.title ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        releaseDate = item.releaseDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        runtime = 120
                    ))
                } else if (item.mediaType == "tv") {
                    val yearInt = item.firstAirDate?.take(4)?.toIntOrNull() ?: 2024
                    series.add(Series(
                        id = item.id.toString(),
                        title = item.name ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        firstAirDate = item.firstAirDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        seasons = emptyList()
                    ))
                }
            }
            Pair(movies, series)
        } catch (e: Exception) {
            Pair(emptyList(), emptyList())
        }
    }
    
    // Add extension functions to map from TMDB models to Domain models
    private fun com.example.data.remote.TmdbMovie.toDomain(): Movie {
        val yearInt = releaseDate?.take(4)?.toIntOrNull() ?: 2024
        return Movie(
            id = id.toString(),
            title = title ?: "Unknown",
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            releaseDate = releaseDate,
            rating = voteAverage ?: 0.0,
            genres = emptyList(),
            runtime = 120
        )
    }
    
    private fun com.example.data.remote.TmdbSeries.toDomain(): Series {
        val yearInt = firstAirDate?.take(4)?.toIntOrNull() ?: 2024
        return Series(
            id = id.toString(),
            title = name ?: "Unknown",
            originalTitle = originalName ?: name,
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            firstAirDate = firstAirDate,
            rating = voteAverage ?: 0.0,
            genres = emptyList(),
            seasons = emptyList()
        )
    }

    
    override suspend fun getPersonDetails(personId: String): PersonDetails? = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getPersonDetails(personId.toInt(), apiKey)
            val movies = mutableListOf<Movie>()
            val series = mutableListOf<Series>()
            response.combinedCredits?.cast?.forEach { item ->
                if (item.mediaType == "movie") {
                    val yearInt = item.releaseDate?.take(4)?.toIntOrNull() ?: 2024
                    movies.add(Movie(
                        id = item.id.toString(),
                        title = item.title ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        releaseDate = item.releaseDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        runtime = 120
                    ))
                } else if (item.mediaType == "tv") {
                    val yearInt = item.firstAirDate?.take(4)?.toIntOrNull() ?: 2024
                    series.add(Series(
                        id = item.id.toString(),
                        title = item.name ?: "Unknown",
                        overview = "",
                        posterUrl = item.fullPosterUrl,
                        backdropUrl = item.fullBackdropUrl,
                        year = yearInt,
                        firstAirDate = item.firstAirDate,
                        rating = item.voteAverage ?: 0.0,
                        genres = emptyList(),
                        seasons = emptyList()
                    ))
                }
            }
            
            movies.sortByDescending { it.rating }
            series.sortByDescending { it.rating }

            PersonDetails(
                id = response.id.toString(),
                name = response.name ?: "Unknown",
                biography = response.biography ?: "",
                profileUrl = response.fullProfileUrl,
                birthday = response.birthday,
                placeOfBirth = response.placeOfBirth,
                knownFor = response.knownForDepartment,
                movies = movies,
                series = series
            )
        } catch (e: Exception) {
            null
        }
    }

    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<Episode> = withContext(Dispatchers.IO) {
        try {
            val response = RetrofitClient.tmdbApi.getSeasonDetails(seriesId.toInt(), seasonNumber, apiKey)
            response.episodes?.map {
                Episode(
                    id = it.id.toString(),
                    episodeNumber = it.episodeNumber,
                    title = it.name ?: "Unknown",
                    overview = it.overview ?: "",
                    thumbnailUrl = it.fullStillUrl ?: "",
                    duration = it.runtime ?: 45,
                    rating = it.voteAverage ?: 0.0
                )
            } ?: emptyList()
        } catch (e: Exception) {
            emptyList()
        }
    }

    private fun com.example.data.remote.TmdbMovieDetails.toDomainDetails(): Movie {
        val yearInt = releaseDate?.take(4)?.toIntOrNull() ?: 2024
        return Movie(
            id = id.toString(),
            title = title ?: "Unknown",
            originalTitle = originalTitle,
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            releaseDate = releaseDate,
            rating = voteAverage ?: 0.0,
            genres = genres?.map { it.name } ?: emptyList(),
            runtime = runtime ?: 120,
            language = originalLanguage ?: "en",
            cast = credits?.cast?.take(15)?.map { CastMember(it.id.toString(), it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList(),
            trailers = videos?.results?.filter { it.site == "YouTube" && it.type == "Trailer" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList()
        )
    }

    private fun com.example.data.remote.TmdbSeriesDetails.toDomainDetails(): Series {
        val yearInt = firstAirDate?.take(4)?.toIntOrNull() ?: 2024
        return Series(
            id = id.toString(),
            title = name ?: "Unknown",
            originalTitle = originalName ?: name,
            overview = overview ?: "",
            posterUrl = fullPosterUrl,
            backdropUrl = fullBackdropUrl,
            year = yearInt,
            firstAirDate = firstAirDate,
            rating = voteAverage ?: 0.0,
            genres = genres?.map { it.name } ?: emptyList(),
            cast = credits?.cast?.take(15)?.map { CastMember(it.id.toString(), it.name, it.character ?: "", it.fullProfileUrl) } ?: emptyList(),
            trailers = videos?.results?.filter { it.site == "YouTube" && it.type == "Trailer" }?.map { VideoTrailer(it.name, it.key, it.type) } ?: emptyList(),
            seasons = seasons?.map { 
                Season(
                    id = it.id.toString(),
                    seriesId = this.id.toString(),
                    seasonNumber = it.seasonNumber,
                    title = it.name,
                    posterUrl = it.fullPosterUrl ?: fullPosterUrl,
                    episodeCount = it.episodeCount
                ) 
            } ?: emptyList(),
            creator = createdBy?.firstOrNull()?.name,
            status = status
        )
    }
}
