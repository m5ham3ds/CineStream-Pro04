import re

# HomeViewModel
with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "r") as f:
    home_vm = f.read()
    
new_load_data = """    fun loadData() {
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
    }"""

home_vm = re.sub(r'fun loadData\(\)\s*\{[\s\S]*\}\s*\}', new_load_data + "\n}", home_vm)
with open("app/src/main/java/com/example/ui/screens/home/HomeViewModel.kt", "w") as f:
    f.write(home_vm)


# MoviesViewModel
with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "r") as f:
    movies_vm = f.read()

new_movies_load = """    fun loadMovies() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            try {
                repository.getTrendingMovies().combine(repository.getArabicMovies()) { trending, arabic ->
                    (trending.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { trending ->
                    _uiState.update { it.copy(trendingMovies = trending, isLoading = false) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getNewReleasesMovies().combine(repository.getArabicMovies()) { newReleases, arabic ->
                    (newReleases.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { newReleases ->
                    _uiState.update { it.copy(newReleasesMovies = newReleases) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getMovies().combine(repository.getArabicMovies()) { movies, arabic ->
                    (movies.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { movies ->
                    _uiState.update { it.copy(movies = movies) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getUpcomingMovies().map { upcoming ->
                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingMovies = upcoming) }
                }
            } catch(e: Exception) {}
        }
    }"""

movies_vm = re.sub(r'fun loadMovies\(\)\s*\{[\s\S]*\}\s*\}', new_movies_load + "\n}", movies_vm)
with open("app/src/main/java/com/example/ui/screens/movies/MoviesViewModel.kt", "w") as f:
    f.write(movies_vm)


# SeriesViewModel
with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "r") as f:
    series_vm = f.read()

new_series_load = """    fun loadSeries() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            try {
                repository.getTrendingSeries().combine(repository.getArabicSeries()) { trending, arabic ->
                    (trending.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { trending ->
                    _uiState.update { it.copy(trendingSeries = trending, isLoading = false) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getNewReleasesSeries().combine(repository.getArabicSeries()) { newReleases, arabic ->
                    (newReleases.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { newReleases ->
                    _uiState.update { it.copy(newReleasesSeries = newReleases) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getSeries().combine(repository.getArabicSeries()) { series, arabic ->
                    (series.take(20) + arabic.take(20)).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { series ->
                    _uiState.update { it.copy(series = series) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getUpcomingSeries().map { upcoming ->
                    upcoming.sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingSeries = upcoming) }
                }
            } catch(e: Exception) {}
        }
    }"""

series_vm = re.sub(r'fun loadSeries\(\)\s*\{[\s\S]*\}\s*\}', new_series_load + "\n}", series_vm)
with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "w") as f:
    f.write(series_vm)


# AnimeViewModel
with open("app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt", "r") as f:
    anime_vm = f.read()
    
new_anime_load = """    fun loadAnime() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            try {
                repository.getTrendingAnime().map { trending ->
                    trending.take(20).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { trending ->
                    _uiState.update { it.copy(trendingAnime = trending, isLoading = false) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getNewReleasesAnime().map { newReleases ->
                    newReleases.take(20).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { }
                .collect { newReleases ->
                    _uiState.update { it.copy(newReleasesAnime = newReleases) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getAnimeSeries().map { anime ->
                    anime.take(20).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> _uiState.update { it.copy(error = e.message) } }
                .collect { anime ->
                    _uiState.update { it.copy(anime = anime) }
                }
            } catch(e: Exception) {}
        }
        
        viewModelScope.launch {
            try {
                repository.getUpcomingAnime().map { upcoming ->
                    upcoming.take(20).sortedByDescending { it.rating }.distinctBy { it.id }
                }
                .catch { e -> }
                .collect { upcoming ->
                    _uiState.update { it.copy(upcomingAnime = upcoming) }
                }
            } catch(e: Exception) {}
        }
    }"""

anime_vm = re.sub(r'fun loadAnime\(\)\s*\{[\s\S]*\}\s*\}', new_anime_load + "\n}", anime_vm)
with open("app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt", "w") as f:
    f.write(anime_vm)

