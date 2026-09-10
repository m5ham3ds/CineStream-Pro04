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
            repository.getSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = it.series.isEmpty()) } }
                .collect { series ->
                    _uiState.update { it.copy(series = series, isLoading = series.isEmpty()) }
                }
        }
    }
}
