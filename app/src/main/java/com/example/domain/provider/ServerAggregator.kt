package com.example.domain.provider

import com.example.domain.models.VideoStream
import kotlinx.coroutines.flow.Flow
import kotlinx.coroutines.flow.flow
import kotlinx.coroutines.flow.merge
import kotlinx.coroutines.flow.map

class ServerAggregator {
    // List of providers you implement based on your SERVER-OF-CONTENT repository
    private val providers = mutableListOf<ContentProvider>()

    fun registerProvider(provider: ContentProvider) {
        providers.add(provider)
    }

    /**
     * Aggregates movie streams from all registered providers and sorts them by quality.
     */
    suspend fun getAggregatedMovieStreams(
        title: String,
        originalTitle: String,
        year: Int,
        tmdbId: String
    ): Flow<List<VideoStream>> {
        val flows = providers.map { provider ->
            provider.getMovieStreams(title, originalTitle, year, tmdbId)
        }
        
        return aggregateAndSort(flows)
    }

    /**
     * Aggregates episode streams from all registered providers and sorts them by quality.
     */
    suspend fun getAggregatedEpisodeStreams(
        title: String,
        originalTitle: String,
        season: Int,
        episode: Int
    ): Flow<List<VideoStream>> {
        val flows = providers.map { provider ->
            provider.getEpisodeStreams(title, originalTitle, season, episode)
        }
        
        return aggregateAndSort(flows)
    }

    private fun aggregateAndSort(flows: List<Flow<List<VideoStream>>>): Flow<List<VideoStream>> = flow {
        // In a real implementation, you'd collect concurrently and emit updates.
        // For simplicity, we merge all flows and emit the sorted accumulated list.
        val accumulated = mutableListOf<VideoStream>()
        
        kotlinx.coroutines.coroutineScope {
            flows.merge().collect { streams ->
                accumulated.addAll(streams)
                
                // Sort by quality (highest resolution first)
                val sorted = accumulated.distinctBy { it.url }.sortedByDescending { it.quality.resolution }
                emit(sorted)
            }
        }
    }
}
