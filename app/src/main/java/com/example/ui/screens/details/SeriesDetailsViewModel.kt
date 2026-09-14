package com.example.ui.screens.details

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Episode
import com.example.domain.models.Season
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import com.example.utils.NetworkUtils
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SeriesDetailsUiState(
    val isLoading: Boolean = false,
    val series: Series? = null,
    val error: String? = null,
    val selectedSeason: Season? = null,
    val episodes: List<Episode> = emptyList(),
    val isEpisodesLoading: Boolean = false,
    val visibleEpisodesCount: Int = 10,
    val isLoadingMore: Boolean = false
)

class SeriesDetailsViewModel(
    private val repository: MediaRepository
) : ViewModel() {
    companion object {
        private val cache = mutableMapOf<String, SeriesDetailsUiState>()
        fun getCachedState(seriesId: String): SeriesDetailsUiState? = cache[seriesId]
        fun saveState(seriesId: String, state: SeriesDetailsUiState) {
            cache[seriesId] = state
        }
    }

    private val _uiState = MutableStateFlow(SeriesDetailsUiState())
    val uiState: StateFlow<SeriesDetailsUiState> = _uiState.asStateFlow()

    fun loadSeries(seriesId: String) {
        val cached = getCachedState(seriesId)
        if (cached != null) {
            _uiState.value = cached
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val series = repository.getSeriesById(seriesId)
                if (series != null) {
                    val initialSeason = series.seasons.firstOrNull { it.seasonNumber > 0 } ?: series.seasons.firstOrNull()
                    val newState = _uiState.value.copy(series = series, isLoading = false, selectedSeason = initialSeason)
                    _uiState.value = newState
                    saveState(seriesId, newState)
                    
                    // Don't load episodes initially. Wait for trigger.
                } else {
                    _uiState.update { it.copy(error = "Series not found", isLoading = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }

    
    fun triggerInitialEpisodesLoad() {
        val currentSeries = _uiState.value.series ?: return
        val currentSeason = _uiState.value.selectedSeason ?: return
        if (_uiState.value.episodes.isEmpty() && !_uiState.value.isEpisodesLoading) {
            loadEpisodes(currentSeries.id, currentSeason.seasonNumber)
        }
    }

    private fun updateAndCache(seriesId: String, transform: (SeriesDetailsUiState) -> SeriesDetailsUiState) {
        _uiState.update { transform(it) }
        saveState(seriesId, _uiState.value)
    }

    fun selectSeason(season: Season) {
        val currentSeries = _uiState.value.series ?: return
        updateAndCache(currentSeries.id) { it.copy(selectedSeason = season, visibleEpisodesCount = 10, episodes = emptyList()) }
        loadEpisodes(currentSeries.id, season.seasonNumber)
    }

    fun loadMoreEpisodes(context: android.content.Context) {
        val currentSeries = _uiState.value.series ?: return
        if (_uiState.value.isLoadingMore) return
        
        viewModelScope.launch {
            updateAndCache(currentSeries.id) { it.copy(isLoadingMore = true) }
            
            // Check internet connection to ensure we only load if online
            if (!NetworkUtils.isInternetAvailable(context)) {
                kotlinx.coroutines.delay(300)
                updateAndCache(currentSeries.id) { it.copy(isLoadingMore = false, error = "No internet connection to load more episodes") }
                return@launch
            }
            
            kotlinx.coroutines.delay(800) // Simulate network delay for UI feedback
            updateAndCache(currentSeries.id) { it.copy(visibleEpisodesCount = it.visibleEpisodesCount + 10, isLoadingMore = false) }
        }
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            updateAndCache(seriesId) { it.copy(isEpisodesLoading = true, visibleEpisodesCount = 10) }
            try {
                val episodes = repository.getSeasonEpisodes(seriesId, seasonNumber)
                updateAndCache(seriesId) { it.copy(episodes = episodes, isEpisodesLoading = false) }
            } catch (e: Exception) {
                updateAndCache(seriesId) { it.copy(isEpisodesLoading = false) }
            }
        }
    }
}