package com.example.source

/**
 * Base interface for an Aniyomi-style Source.
 */
interface AnimeSource {
    val name: String
    val lang: String
    val supportsLatest: Boolean

    suspend fun getPopularAnime(page: Int): List<Anime>
    suspend fun searchAnime(query: String, page: Int): List<Anime>
    suspend fun getAnimeDetails(anime: Anime): Anime
    suspend fun getEpisodeList(anime: Anime): List<Episode>
    suspend fun getVideoList(episode: Episode): List<Video>
}

data class Anime(
    val id: String = "",
    val title: String = "",
    val url: String = "",
    val thumbnailUrl: String? = null,
    val description: String? = null,
    val genre: String? = null,
    val status: Int = 0 // 0 = Unknown, 1 = Ongoing, 2 = Completed
)

data class Episode(
    val url: String = "",
    val name: String = "",
    val dateUpload: Long = 0L,
    val episodeNumber: Float = -1f
)

data class Video(
    val url: String = "",
    val quality: String = "",
    val videoUrl: String? = null // This would be the actual mp4/m3u8 stream
)
