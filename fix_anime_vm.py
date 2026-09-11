with open('app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt', 'r') as f:
    text = f.read()

broken = "val series: List<Series> = emptyList(),"
fixed = "val series: List<Series> = emptyList(),\n    val upcomingAnime: List<Series> = emptyList(),\n    val newEpisodes: List<Series> = emptyList(),"

if broken in text:
    text = text.replace(broken, fixed)
    
    old_load = """    fun loadData() {
        _uiState.update { it.copy(isLoading = true, error = null) }
        viewModelScope.launch {
            repository.getAnimeSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = it.series.isEmpty()) } }
                .collect { list ->
                    _uiState.update { it.copy(series = list, isLoading = list.isEmpty()) }
                }
        }
    }"""
    
    new_load = """    fun loadData() {
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
    }"""
    text = text.replace(old_load, new_load)
    
    with open('app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt', 'w') as f:
        f.write(text)
    print("Fixed AnimeViewModel")
else:
    print("Not found in AnimeViewModel")
