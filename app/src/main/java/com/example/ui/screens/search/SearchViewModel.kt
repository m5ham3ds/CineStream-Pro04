package com.example.ui.screens.search

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.providers.ProviderManager
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
    val seriesResults: List<Series> = emptyList()
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
    }

    fun onQueryChange(query: String) {
        _uiState.update { it.copy(query = query, isSearching = true) }
        queryFlow.value = query
    }

    private fun performSearch(query: String) {
        viewModelScope.launch {
            // Fetch TMDB results
            val (tmdbMovies, tmdbSeries) = repository.searchMulti(query)
            
            // Fetch Provider results
            val providerSeries = ProviderManager.searchProviders(query)
            
            // Deduplicate: If TMDB already has this title, exclude from provider results
            val tmdbTitles = (tmdbMovies.map { it.title.lowercase() } + tmdbSeries.map { it.title.lowercase() }).toSet()
            
            // Deduplicate within providers as well
            val uniqueProviderSeries = mutableListOf<Series>()
            val seenProviderTitles = mutableSetOf<String>()
            
            for (ps in providerSeries) {
                val titleLow = ps.title.lowercase()
                if (!tmdbTitles.contains(titleLow) && !seenProviderTitles.contains(titleLow)) {
                    uniqueProviderSeries.add(ps)
                    seenProviderTitles.add(titleLow)
                }
            }
            
            // Merge TMDB series and the unique Provider series
            val finalSeries = tmdbSeries + uniqueProviderSeries
            
            _uiState.update { it.copy(movieResults = tmdbMovies, seriesResults = finalSeries, isSearching = false) }
        }
    }
}
