package com.example.ui.screens.series

import androidx.lifecycle.ViewModel
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
    val series: List<Series> = emptyList(),
    val upcomingSeries: List<Series> = emptyList(),
    val newEpisodes: List<Series> = emptyList(),
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
                repository.getSeries()
                    .catch { e -> _uiState.update { it.copy(error = e.message) } }
                    .collect { series ->
                        _uiState.update { it.copy(series = series, isLoading = false) }
                    }
            }
            
            launch {
                repository.getUpcomingSeries()
                    .catch { e -> }
                    .collect { upcoming ->
                        _uiState.update { it.copy(upcomingSeries = upcoming) }
                    }
            }
            
            launch {
                repository.getNewReleasesSeries()
                    .catch { e -> }
                    .collect { newEps ->
                        _uiState.update { it.copy(newEpisodes = newEps) }
                    }
            }
        }
    }
}
