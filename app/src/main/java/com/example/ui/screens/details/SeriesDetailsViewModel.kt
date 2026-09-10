package com.example.ui.screens.details

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Episode
import com.example.domain.models.Season
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
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
    val isEpisodesLoading: Boolean = false
)

class SeriesDetailsViewModel(
    private val repository: MediaRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(SeriesDetailsUiState())
    val uiState: StateFlow<SeriesDetailsUiState> = _uiState.asStateFlow()

    fun loadSeries(seriesId: String) {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val series = repository.getSeriesById(seriesId)
                if (series != null) {
                    val initialSeason = series.seasons.firstOrNull { it.seasonNumber > 0 } ?: series.seasons.firstOrNull()
                    _uiState.update { it.copy(series = series, isLoading = false, selectedSeason = initialSeason) }
                    initialSeason?.let { loadEpisodes(series.id, it.seasonNumber) }
                } else {
                    _uiState.update { it.copy(error = "Series not found", isLoading = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }

    fun selectSeason(season: Season) {
        val currentSeries = _uiState.value.series ?: return
        _uiState.update { it.copy(selectedSeason = season) }
        loadEpisodes(currentSeries.id, season.seasonNumber)
    }

    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            _uiState.update { it.copy(isEpisodesLoading = true) }
            try {
                val episodes = repository.getSeasonEpisodes(seriesId, seasonNumber)
                _uiState.update { it.copy(episodes = episodes, isEpisodesLoading = false) }
            } catch (e: Exception) {
                _uiState.update { it.copy(isEpisodesLoading = false) }
            }
        }
    }
}
