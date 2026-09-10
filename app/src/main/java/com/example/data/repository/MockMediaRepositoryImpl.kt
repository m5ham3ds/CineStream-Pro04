package com.example.data.repository

import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.models.Episode
import com.example.domain.models.PersonDetails
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow

class MockMediaRepositoryImpl : MediaRepository {
    override fun getMovies(): Flow<List<Movie>> = flow {
        emit(emptyList())
    }
    override fun getSeries(): Flow<List<Series>> = flow {
        emit(emptyList())
    }
    override fun getTrendingMovies(): Flow<List<Movie>> = flow {
        emit(emptyList())
    }
    override fun getTrendingSeries(): Flow<List<Series>> = flow {
        emit(emptyList())
    }
    override suspend fun getMovieById(id: String): Movie? = null
    override suspend fun getSeriesById(id: String): Series? = null

    override fun getUpcomingMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getAnimeSeries(): Flow<List<Series>> = flow { emit(emptyList()) }
    override fun getAnimeMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getNewReleasesMovies(): Flow<List<Movie>> = flow { emit(emptyList()) }
    override fun getNewReleasesSeries(): Flow<List<Series>> = flow { emit(emptyList()) }

    override suspend fun searchMulti(query: String): Pair<List<Movie>, List<Series>> = Pair(emptyList(), emptyList())
    override suspend fun getSeasonEpisodes(seriesId: String, seasonNumber: Int): List<Episode> = emptyList()
    override suspend fun getPersonDetails(personId: String): PersonDetails? = null
}
