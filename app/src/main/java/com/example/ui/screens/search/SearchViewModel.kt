package com.example.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.FlowPreview
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.collect
import kotlinx.coroutines.flow.combine
import kotlinx.coroutines.flow.debounce
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class SearchUiState(
    val query: String = "",
    val isSearching: Boolean = false,
    val movieResults: List<Movie> = emptyList(),
    val seriesResults: List<Series> = emptyList(),
    val trendingNow: List<Movie> = emptyList()
)

@OptIn(FlowPreview::class)
class SearchViewModel(private val repository: MediaRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(SearchUiState())
    val uiState: StateFlow<SearchUiState> = _uiState.asStateFlow()

    private val queryFlow = MutableStateFlow("")

    init {
        viewModelScope.launch {
            queryFlow
                .debounce(500)
                .collect { q ->
                    if (q.isBlank()) {
                        _uiState.update { it.copy(movieResults = emptyList(), seriesResults = emptyList(), isSearching = false) }
                    } else {
                        performSearch(q)
                    }
                }
        }
        
        loadTrending()
    }
    
    private fun loadTrending() {
        viewModelScope.launch {
            repository.getTrendingMovies()
                .collect { movies ->
                    _uiState.update { it.copy(trendingNow = movies.take(10)) }
                }
        }
    }

    fun onQueryChange(query: String) {
        _uiState.update { it.copy(query = query, isSearching = true) }
        queryFlow.value = query
    }

    private fun performSearch(query: String) {
        viewModelScope.launch {
            // Fetch TMDB results
            val (tmdbMovies, tmdbSeries) = repository.searchMulti(query)
            
            _uiState.update { it.copy(movieResults = tmdbMovies, seriesResults = tmdbSeries, isSearching = false) }
        }
    }
}