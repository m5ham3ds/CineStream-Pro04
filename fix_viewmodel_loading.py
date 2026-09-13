import re

filepath = 'app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add isLoadingMore to state
content = content.replace('val visibleEpisodesCount: Int = 10', 'val visibleEpisodesCount: Int = 10,\n    val isLoadingMore: Boolean = false')

# Modify loadMoreEpisodes to simulate loading
new_load_more = '''
    fun loadMoreEpisodes() {
        val currentSeries = _uiState.value.series ?: return
        if (_uiState.value.isLoadingMore) return
        viewModelScope.launch {
            updateAndCache(currentSeries.id) { it.copy(isLoadingMore = true) }
            kotlinx.coroutines.delay(800) // Simulate network delay for UI feedback
            updateAndCache(currentSeries.id) { it.copy(visibleEpisodesCount = it.visibleEpisodesCount + 10, isLoadingMore = false) }
        }
    }
'''

content = re.sub(r'fun loadMoreEpisodes\(\) \{.*?\n    \}', new_load_more.strip(), content, flags=re.DOTALL)

with open(filepath, 'w') as f:
    f.write(content)

