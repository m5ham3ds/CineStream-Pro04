package com.example.ui.screens.movies

import androidx.lifecycle.ViewModel
import androidx.lifecycle.viewModelScope
import com.example.domain.models.Movie
import com.example.domain.repository.MediaRepository
import kotlinx.coroutines.flow.MutableStateFlow
import kotlinx.coroutines.flow.StateFlow
import kotlinx.coroutines.flow.asStateFlow
import kotlinx.coroutines.flow.catch
import kotlinx.coroutines.flow.update
import kotlinx.coroutines.launch

data class MoviesUiState(
    val isLoading: Boolean = true,
    val trendingMovies: List<Movie> = emptyList(),
    val newReleasesMovies: List<Movie> = emptyList(),
    val movies: List<Movie> = emptyList(),
    val upcomingMovies: List<Movie> = emptyList(),
    val error: String? = null
)

class MoviesViewModel(private val repository: MediaRepository) : ViewModel() {
    private val _uiState = MutableStateFlow(MoviesUiState())
    val uiState: StateFlow<MoviesUiState> = _uiState.asStateFlow()

    init {
        loadMovies()
    }

    fun loadMovies() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            launch {
                repository.getTrendingMovies()
                    .catch { }
                    .collect { trending ->
                        _uiState.update { it.copy(trendingMovies = trending) }
                    }
            }
            
            launch {
                repository.getNewReleasesMovies()
                    .catch { }
                    .collect { newReleases ->
                        _uiState.update { it.copy(newReleasesMovies = newReleases) }
                    }
            }

            launch {
                repository.getMovies()
                    .catch { e -> _uiState.update { it.copy(error = e.message) } }
                    .collect { movies ->
                        _uiState.update { it.copy(movies = movies, isLoading = false) }
                    }
            }
            
            launch {
                repository.getUpcomingMovies()
                    .catch { e -> }
                    .collect { upcoming ->
                        _uiState.update { it.copy(upcomingMovies = upcoming) }
                    }
            }
        }
    }
}
