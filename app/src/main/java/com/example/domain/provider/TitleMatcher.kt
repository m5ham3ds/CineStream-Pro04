package com.example.domain.provider

object TitleMatcher {
    /**
     * Cleans up titles for comparison across different databases and servers.
     * Handles differences like "Demon Slayer: Kimetsu no Yaiba" vs "Kimetsu no Yaiba".
     */
    fun normalize(title: String): String {
        return title.lowercase()
            .replace(Regex("[^a-z0-9\\s]"), "") // Remove all non-alphanumeric except spaces
            .replace(Regex("\\s+"), " ") // Compress multiple spaces
            .trim()
    }

    /**
     * Checks if a server title matches the expected TMDB title using various strategies.
     */
    fun matches(serverTitle: String, tmdbTitle: String, tmdbOriginalTitle: String?): Boolean {
        val serverNorm = normalize(serverTitle)
        val titleNorm = normalize(tmdbTitle)
        val originalNorm = tmdbOriginalTitle?.let { normalize(it) }

        if (serverNorm.contains(titleNorm) || titleNorm.contains(serverNorm)) return true
        if (originalNorm != null && (serverNorm.contains(originalNorm) || originalNorm.contains(serverNorm))) return true

        return false
    }
}
