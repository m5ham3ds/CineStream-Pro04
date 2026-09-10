package com.example.domain.providers

import com.example.source.AnimeSource
import com.example.source.ExampleAnimeSource
import com.example.source.Video
import com.example.source.Episode
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

data class Provider(
    val name: String,
    val type: ProviderType,
    val language: String,
    val logoUrl: String? = null
)

enum class ProviderType {
    ANIME, MOVIE, SERIES
}

data class VideoSource(
    val quality: String,
    val url: String, // Actual MP4/M3U8 link
    val providerName: String
)

object ProviderManager {
    // List of Aniyomi-style extensions (Sources)
    private val sources: List<AnimeSource> = listOf(
        ExampleAnimeSource()
        // Add your parsed HTTP sources here!
    )

    fun getActiveProviders(type: ProviderType): List<Provider> {
        return sources.map { source ->
            Provider(
                name = source.name,
                type = ProviderType.ANIME, // For demo
                language = source.lang
            )
        }
    }

    
suspend fun searchProviders(query: String): List<com.example.domain.models.Series> = withContext(Dispatchers.IO) {
        val results = mutableListOf<com.example.domain.models.Series>()
        for (source in sources) {
            try {
                val animeList = source.searchAnime(query, 1)
                animeList.forEach { anime ->
                    val safeTitle = anime.title.replace("|", "")
                    val safeThumb = anime.thumbnailUrl?.replace("|", "") ?: "" ?: ""
                    results.add(
com.example.domain.models.Series(
                            id = "provider|${source.name}|$safeTitle|$safeThumb|${anime.id.replace("|", "")}",
                            title = anime.title,
                            overview = anime.description ?: "",
                            posterUrl = safeThumb,
                            backdropUrl = safeThumb,
                            year = 2024,
                            firstAirDate = "2024",
                            rating = 0.0,
                            genres = emptyList(),
                            seasons = emptyList()
                        )
                    )
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        return@withContext results
    }

suspend fun extractVideoLinks(mediaId: String, isMovie: Boolean, episodeId: String? = null): List<VideoSource> = withContext(Dispatchers.IO) {
        val allVideos = mutableListOf<VideoSource>()
        
        // Check if mediaId is from a provider
        var targetProviderName: String? = null
        var realMediaId = mediaId
        if (mediaId.startsWith("provider|")) {
            val parts = mediaId.split("|")
            targetProviderName = parts.getOrNull(1)
            realMediaId = parts.getOrNull(4) ?: mediaId
        }
        
        // Loop through all sources to find video links
        for (source in sources) {
            if (targetProviderName != null && source.name != targetProviderName) continue
            
            try {
                // In a real scenario, you'd pass the actual Episode object that was parsed.
                // For this structure, we simulate passing an episode to get the video list.
                val dummyEpisode = Episode(url = "/episode/${episodeId ?: realMediaId}")
                val videos = source.getVideoList(dummyEpisode)
                
                videos.forEach { video ->
                    if (video.videoUrl != null) {
                        allVideos.add(
                            VideoSource(
                                quality = video.quality,
                                url = video.videoUrl, // Real direct video URL
                                providerName = source.name
                            )
                        )
                    }
                }
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
        
        // If no sources are implemented yet, we return a real working MP4 for testing
        // to prove the ExoPlayer and Offline Download systems work.
        if (allVideos.isEmpty()) {
            allVideos.add(
                VideoSource(
                    quality = "720p (Test Video)",
                    url = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/ForBiggerBlazes.mp4",
                    providerName = "System"
                )
            )
        }
        
        return@withContext allVideos
    }
}
