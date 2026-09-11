with open('app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt', 'r') as f:
    text = f.read()

broken = "val movies: List<Movie> = emptyList(),"
fixed = "val movies: List<Movie> = emptyList(),\n    val upcomingMovies: List<Movie> = emptyList(),"

if broken in text:
    text = text.replace(broken, fixed)
    
    # replace loadMovies
    old_load = """    fun loadMovies() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            repository.getMovies()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = it.movies.isEmpty()) } }
                .collect { movies ->
                    _uiState.update { it.copy(movies = movies, isLoading = movies.isEmpty()) }
                }
        }
    }"""
    
    new_load = """    fun loadMovies() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
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
    }"""
    text = text.replace(old_load, new_load)
    
    with open('app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt', 'w') as f:
        f.write(text)
    print("Fixed MoviesViewModel")
else:
    print("Not found in MoviesViewModel")
