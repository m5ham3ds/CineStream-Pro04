import re

filepath = 'app/src/main/java/com/example/ui/screens/details/SeriesDetailsViewModel.kt'
with open(filepath, 'r') as f:
    content = f.read()

# Add Cache companion object
cache_code = '''
    companion object {
        private val cache = mutableMapOf<String, SeriesDetailsUiState>()
        fun getCachedState(seriesId: String) = cache[seriesId]
        fun saveState(seriesId: String, state: SeriesDetailsUiState) {
            cache[seriesId] = state
        }
    }
'''

if 'companion object' not in content:
    content = content.replace('class SeriesDetailsViewModel(', cache_code + '\nclass SeriesDetailsViewModel(')

# In loadSeries
# When loading, check cache first. If cache exists, emit it. But we also need to trigger loadEpisodes if it's not loaded?
# Actually, if we just cache the state, we can restore it.

