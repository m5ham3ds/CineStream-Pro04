package com.example.ui.screens.player

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.data.repository.TmdbMediaRepositoryImpl
import com.example.domain.models.Episode
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.launch
import kotlinx.coroutines.delay

data class PlayerUiState(
    val isLoading: Boolean = true,
    val mediaId: String = "",
    val isMovie: Boolean = true,
    val isAnime: Boolean = false,
    val title: String = "",

    // Website (Provider)
    val availableWebsites: List<String> = emptyList(),
    val currentWebsite: String = "",
    val fallbackWebsites: List<String> = emptyList(),

    // Server
    val availableServers: List<String> = emptyList(),
    val currentServer: String = "",
    val availableServerLinks: Map<String, String> = emptyMap(),
    val availableServerIds: Map<String, String> = emptyMap(),
    val serverIdToChange: String? = null,

    // Quality
    val availableQualities: List<String> = listOf("Auto", "1080p", "720p"),
    val currentQuality: String = "Auto",

    // Episodes
    val episodes: List<Episode> = emptyList(),
    val currentEpisodeId: String = "",
    val currentSeasonNumber: Int = 1,
    val currentEpisodeNumber: Int = 1,

    // Extracted URL
    val currentVideoUrl: String? = null,
    val extractionUrl: String? = null // The URL to feed to the hidden WebView
)

class PlayerViewModel : ViewModel() {
    private val tmdbRepo = TmdbMediaRepositoryImpl()

    private val _uiState = MutableStateFlow(PlayerUiState())
    val uiState: StateFlow<PlayerUiState> = _uiState.asStateFlow()

    private var extractionTimeoutJob: kotlinx.coroutines.Job? = null

    fun initialize(mediaId: String, isMovie: Boolean, initialTitle: String, directUrl: String? = null, targetServer: String? = null, website: String? = null) {
        val hasArabic = initialTitle.any { it in '؀'..'ۿ' }
        val isAnime = initialTitle.contains("anime", ignoreCase = true) || initialTitle.contains("أنمي", ignoreCase = true)
        
        val allAnimeSites = listOf(
            "witanime.you", "w1.anime4up.rest", "animeblkom.net", "animeat.net", 
            "arabanime.net", "det.animerco.org", "vip.animeluxe.org"
        )
        val allMovieSeriesSites = listOf(
            "tv10.egydead.live", "a.qfilm.tv", "egybests.live", "arabseed.wine", 
            "topcinema.io", "z1.almeshkah.net", "arabseed-tv.com", "e.cimalight.co", 
            "stardima.com", "watch.stardima.com", "uo.brstej.com", "laaroza.space"
        )

        val fallbackList = when {
            isAnime -> listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net") + allAnimeSites.filter { it !in listOf("witanime.you", "w1.anime4up.rest", "animeblkom.net") }
            isMovie -> listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") + allMovieSeriesSites.filter { it !in listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") }
            else -> listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") + allMovieSeriesSites.filter { it !in listOf("tv10.egydead.live", "a.qfilm.tv", "egybests.live") }
        }
        
        val availableList = if (isAnime) allAnimeSites else allMovieSeriesSites
        
        val bestWebsite = website ?: fallbackList.first()
        val remainingFallbacks = if (website == null) fallbackList.drop(1) else emptyList()

        _uiState.value = _uiState.value.copy(
            mediaId = mediaId,
            isMovie = isMovie,
            isAnime = isAnime,
            title = initialTitle,
            availableWebsites = availableList,
            currentWebsite = bestWebsite,
            fallbackWebsites = remainingFallbacks,
            currentServer = targetServer ?: "",
            availableServers = com.example.ui.screens.player.ServerStateStore.extractedServers,
            availableServerLinks = com.example.ui.screens.player.ServerStateStore.extractedServerLinks,
            availableServerIds = com.example.ui.screens.player.ServerStateStore.extractedServerIds
        )

        if (!directUrl.isNullOrEmpty() && (directUrl.contains(".mp4") || directUrl.contains(".m3u8") || directUrl.startsWith("local_offline_file"))) {
            _uiState.value = _uiState.value.copy(currentVideoUrl = directUrl, isLoading = false)
        } else if (!directUrl.isNullOrEmpty()) {
            // It's a watch url (webpage), we need to extract from it
            _uiState.value = _uiState.value.copy(extractionUrl = directUrl, isLoading = true)
            startExtractionTimeout()
        } else if (!isMovie) {
            loadEpisodes(mediaId, 1) // Default to season 1
        } else {
            generateExtractionUrl()
        }
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            try {
                // Fetch full series details to get episodes for the season
                val series = tmdbRepo.getSeriesById(seriesId)
                val season = series?.seasons?.find { it.seasonNumber == seasonNumber }
                if (season != null) {
                    val fullSeason = tmdbRepo.getSeasonEpisodes(seriesId, seasonNumber)
                    _uiState.value = _uiState.value.copy(
                        episodes = fullSeason,
                        currentEpisodeId = fullSeason.firstOrNull()?.id ?: "",
                        currentSeasonNumber = seasonNumber,
                        currentEpisodeNumber = fullSeason.firstOrNull()?.episodeNumber ?: 1
                    )
                }
                generateExtractionUrl()
            } catch (e: Exception) {
                e.printStackTrace()
            }
        }
    }

    fun selectWebsite(website: String) {
        com.example.ui.screens.player.ServerStateStore.clear()
        _uiState.value = _uiState.value.copy(
            currentWebsite = website, 
            isLoading = true, 
            currentVideoUrl = null, 
            fallbackWebsites = emptyList(),
            availableServers = emptyList(),
            availableServerLinks = emptyMap(),
            availableServerIds = emptyMap(),
            currentServer = ""
        )
        generateExtractionUrl()
    }

    fun selectServer(server: String) {
        val link = _uiState.value.availableServerLinks[server]
        val id = _uiState.value.availableServerIds[server]
        
        var nextExtractionUrl = _uiState.value.extractionUrl
        if (link != null && link.isNotEmpty()) {
            nextExtractionUrl = link
        }
        
        _uiState.value = _uiState.value.copy(
            currentServer = server,
            isLoading = true,
            currentVideoUrl = null,
            extractionUrl = nextExtractionUrl,
            serverIdToChange = id
        )
        
        if (nextExtractionUrl != null) {
            startExtractionTimeout()
        } else {
            generateExtractionUrl()
        }
    }

    fun selectEpisode(episode: com.example.domain.models.Episode) {
        _uiState.value = _uiState.value.copy(
            currentEpisodeId = episode.id,
            currentEpisodeNumber = episode.episodeNumber,
            title = episode.title,
            isLoading = true,
            currentVideoUrl = null
        )
        generateExtractionUrl()
    }

    fun setFinalVideoUrl(url: String) {
        extractionTimeoutJob?.cancel()
        if (_uiState.value.currentVideoUrl != url) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = url,
                isLoading = false
            )
        }
    }

    fun setIframeUrl(url: String) {
        extractionTimeoutJob?.cancel()
        _uiState.value = _uiState.value.copy(
            extractionUrl = url,
            isLoading = true,
            currentVideoUrl = null
        )
        // Only wait 3 seconds to see if a direct video can be extracted from this iframe
        extractionTimeoutJob = viewModelScope.launch {
            kotlinx.coroutines.delay(3000)
            if (_uiState.value.currentVideoUrl == null) {
                // If no direct video found, just use the iframe as the final video URL
                setFinalVideoUrl(url)
            }
        }
    }

    fun updateServers(servers: List<String>) {
        if (_uiState.value.availableServers != servers && servers.isNotEmpty()) {
            val firstServer = servers.first()
            val link = com.example.ui.screens.player.ServerStateStore.extractedServerLinks[firstServer]
            val id = com.example.ui.screens.player.ServerStateStore.extractedServerIds[firstServer]
            
            var nextExtractionUrl = _uiState.value.extractionUrl
            if (link != null && link.isNotEmpty()) {
                nextExtractionUrl = link
            }
            
            _uiState.value = _uiState.value.copy(
                availableServers = servers,
                currentServer = firstServer,
                extractionUrl = nextExtractionUrl,
                serverIdToChange = id
            )
            
            if (nextExtractionUrl != null) {
                startExtractionTimeout()
            }
        }
    }

    private fun startExtractionTimeout() {
        extractionTimeoutJob?.cancel()
        extractionTimeoutJob = viewModelScope.launch {
            delay(300000) // 5 minutes timeout to allow for manual Cloudflare bypass
            if (_uiState.value.currentVideoUrl == null) {
                tryNextFallback()
            }
        }
    }
    
    fun tryNextFallback() {
        val fallbacks = _uiState.value.fallbackWebsites
        if (fallbacks.isNotEmpty()) {
            val nextSite = fallbacks.first()
            _uiState.value = _uiState.value.copy(
                currentWebsite = nextSite,
                fallbackWebsites = fallbacks.drop(1),
                isLoading = true,
                currentVideoUrl = null
            )
            generateExtractionUrl()
        } else {
            _uiState.value = _uiState.value.copy(isLoading = false)
        }
    }

    private fun generateExtractionUrl() {
        val state = _uiState.value
        
        viewModelScope.launch {
            _uiState.value = _uiState.value.copy(isLoading = true, extractionUrl = null)
            val watchUrl = com.example.data.repository.ScraperRepository.getWatchUrl(
                website = state.currentWebsite,
                query = state.title,
                isMovie = state.isMovie,
                season = state.currentSeasonNumber,
                episode = state.currentEpisodeNumber
            )
            
            if (watchUrl != null) {
                _uiState.value = _uiState.value.copy(extractionUrl = watchUrl, isLoading = true)
                startExtractionTimeout()
            } else {
                tryNextFallback()
            }
        }
    }
}
