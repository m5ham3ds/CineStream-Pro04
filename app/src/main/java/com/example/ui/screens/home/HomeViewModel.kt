package com.example.ui.screens.home

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Movie
import com.example.domain.models.Series
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.async
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.firstOrNull
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class HomeUiState(
    val isLoading: Boolean = true,
    val trendingMovies: List<Movie> = emptyList(),
    val trendingSeries: List<Series> = emptyList(),
    val actionMovies: List<Movie> = emptyList(),
    val allMovies: List<Movie> = emptyList(),
    val allSeries: List<Series> = emptyList(),
    val animeSeries: List<Series> = emptyList(),
    val upcomingMovies: List<Movie> = emptyList(),
    val newReleasesMovies: List<Movie> = emptyList(),
    val newReleasesSeries: List<Series> = emptyList(),
    val error: String? = null
)

class HomeViewModel(
    private val repository: MediaRepository
) : ViewModel() {

    private val _uiState = MutableStateFlow(HomeUiState())
    val uiState: StateFlow<HomeUiState> = _uiState.asStateFlow()

    init {
        loadData()
    }

    fun loadData() {
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            kotlinx.coroutines.delay(400) // Ensure shimmer effect is visible for a moment even if loading from cache
            
            try {
                val trendingMoviesDeferred = async { repository.getTrendingMovies().firstOrNull() ?: emptyList() }
                val animeSeriesDeferred = async { repository.getAnimeSeries().firstOrNull() ?: emptyList() }
                val upcomingMoviesDeferred = async { repository.getUpcomingMovies().firstOrNull() ?: emptyList() }
                val newReleasesMoviesDeferred = async { repository.getNewReleasesMovies().firstOrNull() ?: emptyList() }
                val newReleasesSeriesDeferred = async { repository.getNewReleasesSeries().firstOrNull() ?: emptyList() }
                val trendingSeriesDeferred = async { repository.getTrendingSeries().firstOrNull() ?: emptyList() }
                val allMoviesDeferred = async { repository.getMovies().firstOrNull() ?: emptyList() }
                val allSeriesDeferred = async { repository.getSeries().firstOrNull() ?: emptyList() }
                
                val trendingMovies = trendingMoviesDeferred.await()
                val animeSeries = animeSeriesDeferred.await()
                val upcomingMovies = upcomingMoviesDeferred.await()
                val newReleasesMovies = newReleasesMoviesDeferred.await()
                val newReleasesSeries = newReleasesSeriesDeferred.await()
                val trendingSeries = trendingSeriesDeferred.await()
                val allMovies = allMoviesDeferred.await()
                val allSeries = allSeriesDeferred.await()
                
                val actionMovies = allMovies.filter { m -> m.genres.contains("Action") }
                
                val hasData = trendingMovies.isNotEmpty() || animeSeries.isNotEmpty() || trendingSeries.isNotEmpty() || actionMovies.isNotEmpty()
                
                _uiState.update {
                    it.copy(
                        trendingMovies = trendingMovies,
                        animeSeries = animeSeries,
                        upcomingMovies = upcomingMovies,
                        newReleasesMovies = newReleasesMovies,
                        newReleasesSeries = newReleasesSeries,
                        trendingSeries = trendingSeries,
                        actionMovies = actionMovies,
                        allMovies = allMovies,
                        allSeries = allSeries,
                        isLoading = !hasData
                    )
                }
            } catch (e: Exception) {
                _uiState.update { state -> 
                    val hasData = state.trendingMovies.isNotEmpty() || state.animeSeries.isNotEmpty() || state.trendingSeries.isNotEmpty() || state.actionMovies.isNotEmpty()
                    state.copy(error = e.message, isLoading = !hasData)
                }
            }
        }
    }
}
