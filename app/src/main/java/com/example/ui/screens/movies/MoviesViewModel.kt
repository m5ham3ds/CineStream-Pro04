package com.example.ui.screens.movies
import kotlinx.coroutines.flow.map

import androidx.lifecycle.ViewModel
import kotlinx.coroutines.flow.combine
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
                repository.getTrendingMovies().combine(repository.getArabicMovies()) { trending, arabic ->
                    (trending.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { trending ->
                    _uiState.update { it.copy(trendingMovies = trending) }
                }
            }
            
            launch {
                repository.getNewReleasesMovies().combine(repository.getArabicMovies()) { newReleases, arabic ->
                    (newReleases.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { newReleases ->
                    _uiState.update { it.copy(newReleasesMovies = newReleases) }
                }
            }

            launch {
                repository.getMovies().combine(repository.getArabicMovies()) { movies, arabic ->
                    (movies.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { movies ->
                    _uiState.update { it.copy(movies = movies, isLoading = false) }
                }
            }
            
            launch {
                repository.getUpcomingMovies().map { upcoming ->
                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingMovies = upcoming) }
                }
            }
        }
    }
}