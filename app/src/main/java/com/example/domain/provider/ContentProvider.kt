package com.example.domain.provider

import com.example.domain.models.VideoStream
import kotlinx.coroutines.flow.Flow

/**
 * Interface that each server scraper/API from the SERVER-OF-CONTENT repo should implement.
 */
interface ContentProvider {
    val name: String

    /**
     * Search for movie streams.
     * @param title The normalized or localized title.
     * @param originalTitle The original (e.g. English/Japanese) title.
     * @param year The release year for disambiguation.
     * @param tmdbId The TMDB ID if the provider supports ID-based lookup.
     */
    suspend fun getMovieStreams(
        title: String,
        originalTitle: String,
        year: Int,
        tmdbId: String
    ): Flow<List<VideoStream>>

    /**
     * Search for episode streams.
     * @param title The show's title.
     * @param originalTitle The show's original title.
     * @param season The season number.
     * @param episode The episode number.
     */
    suspend fun getEpisodeStreams(
        title: String,
        originalTitle: String,
        season: Int,
        episode: Int
    ): Flow<List<VideoStream>>
}
