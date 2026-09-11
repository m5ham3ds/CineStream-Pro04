with open('app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt', 'r') as f:
    text = f.read()

broken = "val series: List<Series> = emptyList(),"
fixed = "val series: List<Series> = emptyList(),\n    val upcomingSeries: List<Series> = emptyList(),\n    val newEpisodes: List<Series> = emptyList(),"

if broken in text:
    text = text.replace(broken, fixed)
    
    old_load = """    fun loadSeries() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            repository.getSeries()
                .catch { e -> _uiState.update { it.copy(error = e.message, isLoading = it.series.isEmpty()) } }
                .collect { series ->
                    _uiState.update { it.copy(series = series, isLoading = series.isEmpty()) }
                }
        }
    }"""
    
    new_load = """    fun loadSeries() {
        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            
            launch {
                repository.getSeries()
                    .catch { e -> _uiState.update { it.copy(error = e.message) } }
                    .collect { series ->
                        _uiState.update { it.copy(series = series, isLoading = false) }
                    }
            }
            
            launch {
                repository.getUpcomingSeries()
                    .catch { e -> }
                    .collect { upcoming ->
                        _uiState.update { it.copy(upcomingSeries = upcoming) }
                    }
            }
            
            launch {
                repository.getNewReleasesSeries()
                    .catch { e -> }
                    .collect { newEps ->
                        _uiState.update { it.copy(newEpisodes = newEps) }
                    }
            }
        }
    }"""
    text = text.replace(old_load, new_load)
    
    with open('app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt', 'w') as f:
        f.write(text)
    print("Fixed SeriesViewModel")
else:
    print("Not found in SeriesViewModel")
