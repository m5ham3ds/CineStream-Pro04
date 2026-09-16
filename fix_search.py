import re

with open("app/src/main/java/com/example/ui/screens/search/SearchViewModel.kt", "r") as f:
    c = f.read()

# Remove import
c = c.replace("import com.example.domain.providers.ProviderManager\n", "")

# Remove ProviderManager usage in performSearch
target_search = """            // Fetch TMDB results
            val (tmdbMovies, tmdbSeries) = repository.searchMulti(query)
            
            // Fetch Provider results
            val providerSeries = ProviderManager.searchProviders(query)
            
            // Deduplicate: If TMDB already has this title, exclude from provider results
            val tmdbTitles = (tmdbMovies.map { it.title.lowercase() } + tmdbSeries.map { it.title.lowercase() }).toSet()
            
            // Deduplicate within providers as well
            val uniqueProviderSeries = mutableListOf<Series>()
            val seenProviderTitles = mutableSetOf<String>()
            
            for (ps in providerSeries) {
                val titleLow = ps.title.lowercase()
                if (!tmdbTitles.contains(titleLow) && !seenProviderTitles.contains(titleLow)) {
                    uniqueProviderSeries.add(ps)
                    seenProviderTitles.add(titleLow)
                }
            }
            
            // Merge TMDB series and the unique Provider series
            val finalSeries = tmdbSeries + uniqueProviderSeries
            
            _uiState.update { it.copy(movieResults = tmdbMovies, seriesResults = finalSeries, isSearching = false) }"""

replacement_search = """            // Fetch TMDB results
            val (tmdbMovies, tmdbSeries) = repository.searchMulti(query)
            
            _uiState.update { it.copy(movieResults = tmdbMovies, seriesResults = tmdbSeries, isSearching = false) }"""

c = c.replace(target_search, replacement_search)

with open("app/src/main/java/com/example/ui/screens/search/SearchViewModel.kt", "w") as f:
    f.write(c)

