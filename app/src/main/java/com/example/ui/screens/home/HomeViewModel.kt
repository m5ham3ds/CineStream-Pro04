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
    val trendingAnime: List<Series> = emptyList(),
    val popularMovies: List<Movie> = emptyList(),
    val popularSeries: List<Series> = emptyList(),
    val popularAnime: List<Series> = emptyList(),
    val upcomingSeries: List<Series> = emptyList(),
    val upcomingAnime: List<Series> = emptyList(),
    val newReleasesAnime: List<Series> = emptyList(),
    val upcomingMovies: List<Movie> = emptyList(),
    val newReleasesMovies: List<Movie> = emptyList(),
    val newReleasesSeries: List<Series> = emptyList(),
    val arabicMovies: List<Movie> = emptyList(),
    val arabicSeries: List<Series> = emptyList(),
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
            try {
                val trendingMovies = repository.getTrendingMovies().firstOrNull() ?: emptyList()
                val animeSeries = repository.getAnimeSeries().firstOrNull() ?: emptyList()
                val trendingSeries = repository.getTrendingSeries().firstOrNull() ?: emptyList()
                val allMovies = repository.getMovies().firstOrNull() ?: emptyList()
                val actionMovies = allMovies.filter { m -> m.genres.contains("Action") }
                
                val hasData = trendingMovies.isNotEmpty() || animeSeries.isNotEmpty() || trendingSeries.isNotEmpty() || actionMovies.isNotEmpty()
                
                _uiState.update {
                    it.copy(
                        trendingMovies = trendingMovies.take(15),
                        animeSeries = animeSeries.take(15),
                        trendingSeries = trendingSeries.take(15),
                        actionMovies = actionMovies.take(15),
                        allMovies = allMovies.take(15),
                        isLoading = !hasData
                    )
                }

                val upcomingMovies = repository.getUpcomingMovies().firstOrNull() ?: emptyList()
                val newReleasesMovies = repository.getNewReleasesMovies().firstOrNull() ?: emptyList()
                val newReleasesSeries = repository.getNewReleasesSeries().firstOrNull() ?: emptyList()
                
                _uiState.update {
                    it.copy(
                        upcomingMovies = upcomingMovies.take(15),
                        newReleasesMovies = newReleasesMovies.take(15),
                        newReleasesSeries = newReleasesSeries.take(15)
                    )
                }

                val trendingAnime = repository.getTrendingAnime().firstOrNull() ?: emptyList()
                val allSeries = repository.getSeries().firstOrNull() ?: emptyList()
                val popularMovies = repository.getMovies().firstOrNull() ?: emptyList()
                
                _uiState.update {
                    it.copy(
                        trendingAnime = trendingAnime.take(15),
                        allSeries = allSeries.take(15),
                        popularMovies = popularMovies.take(15)
                    )
                }
                
                val upcomingSeries = repository.getUpcomingSeries().firstOrNull() ?: emptyList()
                val upcomingAnime = repository.getUpcomingAnime().firstOrNull() ?: emptyList()
                val newReleasesAnime = repository.getNewReleasesAnime().firstOrNull() ?: emptyList()
                
                _uiState.update {
                    it.copy(
                        upcomingSeries = upcomingSeries.take(15),
                        upcomingAnime = upcomingAnime.take(15),
                        newReleasesAnime = newReleasesAnime.take(15)
                    )
                }
                
            } catch (e: Exception) {
                _uiState.update { state -> 
                     val hasData = state.trendingMovies.isNotEmpty() || state.animeSeries.isNotEmpty()
                     state.copy(error = e.message, isLoading = !hasData)
                }
            }
        }
    }
}