package com.example.ui.screens.series
import kotlinx.coroutines.flow.map

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.combine
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SeriesUiState(
    val isLoading: Boolean = true,
    val trendingSeries: List<Series> = emptyList(),
    val newEpisodes: List<Series> = emptyList(),
    val series: List<Series> = emptyList(),
    val upcomingSeries: List<Series> = emptyList(),
    val error: String? = null
)


class SeriesViewModel(private val repository: MediaRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(SeriesUiState())
    val uiState: StateFlow<SeriesUiState> = _uiState.asStateFlow()

    init {
        loadSeries()
    }

    fun loadSeries() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            launch {
                repository.getTrendingSeries().combine(repository.getArabicSeries()) { trending, arabic ->
                    (trending.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { trending ->
                    _uiState.update { it.copy(trendingSeries = trending) }
                }
            }
            
            launch {
                repository.getNewReleasesSeries().combine(repository.getArabicSeries()) { newEps, arabic ->
                    (newEps.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { newEps ->
                    _uiState.update { it.copy(newEpisodes = newEps) }
                }
            }

            launch {
                repository.getSeries().combine(repository.getArabicSeries()) { series, arabic ->
                    (series.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { series ->
                    _uiState.update { it.copy(series = series, isLoading = false) }
                }
            }
            
            launch {
                repository.getUpcomingSeries().map { upcoming ->
                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingSeries = upcoming) }
                }
            }
        }
    }
}