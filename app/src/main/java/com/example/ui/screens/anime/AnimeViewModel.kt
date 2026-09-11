package com.example.ui.screens.anime

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

data class AnimeUiState(
    val isLoading: Boolean = true,
    val series: List<Series> = emptyList(),
    val upcomingAnime: List<Series> = emptyList(),
    val newEpisodes: List<Series> = emptyList(),
    val error: String? = null
)

class AnimeViewModel(
    private val repository: MediaRepository
) : ViewModel() {
    private val _uiState = MutableStateFlow(AnimeUiState())
    val uiState: StateFlow<AnimeUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    fun loadData() {
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            launch {
                repository.getAnimeSeries()
                    .catch { e -> _uiState.update { it.copy(error = e.message) } }
                    .collect { list ->
                        _uiState.update { it.copy(series = list, isLoading = false) }
                    }
            }
            launch {
                repository.getUpcomingAnime()
                    .catch { e -> }
                    .collect { upcoming ->
                        _uiState.update { it.copy(upcomingAnime = upcoming) }
                    }
            }
            launch {
                repository.getNewReleasesAnime()
                    .catch { e -> }
                    .collect { newEps ->
                        _uiState.update { it.copy(newEpisodes = newEps) }
                    }
            }
        }
    }
}
