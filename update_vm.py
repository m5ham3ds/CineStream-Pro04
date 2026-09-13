import os

filepath = 'app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Replace the body of loadSeries to use cache
new_load_series = '''
    fun loadSeries(seriesId: String) {
        val cached = getCachedState(seriesId)
        if (cached != null) {
            _uiState.value = cached
            return
        }

        viewModelScope.launch {
            _uiState.update { it.copy(isLoading = true, error = null) }
            try {
                val series = repository.getSeriesById(seriesId)
                if (series != null) {
                    val initialSeason = series.seasons.firstOrNull { it.seasonNumber > 0 } ?: series.seasons.firstOrNull()
                    val newState = _uiState.value.copy(series = series, isLoading = false, selectedSeason = initialSeason)
                    _uiState.value = newState
                    saveState(seriesId, newState)
                    
                    // Don't load episodes initially. Wait for trigger.
                } else {
                    _uiState.update { it.copy(error = "Series not found", isLoading = false) }
                }
            } catch (e: Exception) {
                _uiState.update { it.copy(error = e.message, isLoading = false) }
            }
        }
    }
'''

import re
content = re.sub(r'fun loadSeries\(seriesId: String\) \{.*?\n    \}', new_load_series.strip(), content, flags=re.DOTALL)

# Add triggerInitialEpisodesLoad function
new_funcs = '''
    fun triggerInitialEpisodesLoad() {
        val currentSeries = _uiState.value.series ?: return
        val currentSeason = _uiState.value.selectedSeason ?: return
        if (_uiState.value.episodes.isEmpty() && !_uiState.value.isEpisodesLoading) {
            loadEpisodes(currentSeries.id, currentSeason.seasonNumber)
        }
    }

    private fun updateAndCache(seriesId: String, transform: (SeriesDetailsUiState) -> SeriesDetailsUiState) {
        _uiState.update { transform(it) }
        saveState(seriesId, _uiState.value)
    }
'''
content = content.replace('fun selectSeason(season: Season) {', new_funcs + '\n    fun selectSeason(season: Season) {')

# Modify selectSeason to use updateAndCache
new_select_season = '''
    fun selectSeason(season: Season) {
        val currentSeries = _uiState.value.series ?: return
        updateAndCache(currentSeries.id) { it.copy(selectedSeason = season, visibleEpisodesCount = 10, episodes = emptyList()) }
        loadEpisodes(currentSeries.id, season.seasonNumber)
    }
'''
content = re.sub(r'fun selectSeason\(season: Season\) \{.*?\n    \}', new_select_season.strip(), content, flags=re.DOTALL)

# Modify loadMoreEpisodes
new_load_more = '''
    fun loadMoreEpisodes() {
        val currentSeries = _uiState.value.series ?: return
        updateAndCache(currentSeries.id) { it.copy(visibleEpisodesCount = it.visibleEpisodesCount + 10) }
    }
'''
content = re.sub(r'fun loadMoreEpisodes\(\) \{.*?\n    \}', new_load_more.strip(), content, flags=re.DOTALL)

# Modify loadEpisodes
new_load_episodes = '''
    private fun loadEpisodes(seriesId: String, seasonNumber: Int) {
        viewModelScope.launch {
            updateAndCache(seriesId) { it.copy(isEpisodesLoading = true, visibleEpisodesCount = 10) }
            try {
                val episodes = repository.getSeasonEpisodes(seriesId, seasonNumber)
                updateAndCache(seriesId) { it.copy(episodes = episodes, isEpisodesLoading = false) }
            } catch (e: Exception) {
                updateAndCache(seriesId) { it.copy(isEpisodesLoading = false) }
            }
        }
    }
'''
content = re.sub(r'private fun loadEpisodes\(seriesId: String, seasonNumber: Int\) \{.*?\}\n    \}', new_load_episodes.strip(), content, flags=re.DOTALL)


with open(filepath, 'w') as f:
    f.write(content)
