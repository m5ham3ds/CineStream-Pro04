package com.example.extensions

interface ProviderExtension {
    val id: String
    val name: String
    val baseUrl: String
    val isAnime: Boolean
    val isMovie: Boolean
    val isSeries: Boolean
    val lang: String
    val iconUrl: String

    /**
     * JS Script to execute to extract servers or links on the site
     */
    fun getExtractionScript(isMovie: Boolean, episode: Int, title: String): String

    /**
     * JS Script to execute on the video iframe to extract qualities
     */
    fun getVideoExtractorScript(): String? = null

    /**
     * Get search URL for the given title
     */
    fun getSearchUrl(titleOriginal: String, titleClean: String): String
}
