package com.example.source

import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.Response
import org.jsoup.Jsoup
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element
import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext

/**
 * A base class for HTTP sources that parse HTML using Jsoup.
 * Mimics the Aniyomi extension architecture.
 */
abstract class ParsedHttpSource : AnimeSource {
    protected val client = OkHttpClient()
    protected abstract val baseUrl: String

    override val supportsLatest: Boolean = true

    override suspend fun getPopularAnime(page: Int): List<Anime> = withContext(Dispatchers.IO) {
        val request = popularAnimeRequest(page)
        val response = client.newCall(request).execute()
        val document = Jsoup.parse(response.body?.string() ?: "")
        popularAnimeSelector(document).map { popularAnimeFromElement(it) }
    }

    protected abstract fun popularAnimeRequest(page: Int): Request
    protected abstract fun popularAnimeSelector(document: Document): List<Element>
    protected abstract fun popularAnimeFromElement(element: Element): Anime

    override suspend fun searchAnime(query: String, page: Int): List<Anime> = withContext(Dispatchers.IO) {
        val request = searchAnimeRequest(query, page)
        val response = client.newCall(request).execute()
        val document = Jsoup.parse(response.body?.string() ?: "")
        searchAnimeSelector(document).map { searchAnimeFromElement(it) }
    }

    protected abstract fun searchAnimeRequest(query: String, page: Int): Request
    protected abstract fun searchAnimeSelector(document: Document): List<Element>
    protected abstract fun searchAnimeFromElement(element: Element): Anime

    override suspend fun getAnimeDetails(anime: Anime): Anime = withContext(Dispatchers.IO) {
        val request = Request.Builder().url(baseUrl + anime.url).build()
        val response = client.newCall(request).execute()
        val document = Jsoup.parse(response.body?.string() ?: "")
        animeDetailsParse(document, anime)
    }

    protected abstract fun animeDetailsParse(document: Document, anime: Anime): Anime

    override suspend fun getEpisodeList(anime: Anime): List<Episode> = withContext(Dispatchers.IO) {
        val request = Request.Builder().url(baseUrl + anime.url).build()
        val response = client.newCall(request).execute()
        val document = Jsoup.parse(response.body?.string() ?: "")
        episodeListSelector(document).map { episodeFromElement(it) }
    }

    protected abstract fun episodeListSelector(document: Document): List<Element>
    protected abstract fun episodeFromElement(element: Element): Episode

    override suspend fun getVideoList(episode: Episode): List<Video> = withContext(Dispatchers.IO) {
        val request = Request.Builder().url(baseUrl + episode.url).build()
        val response = client.newCall(request).execute()
        val document = Jsoup.parse(response.body?.string() ?: "")
        videoListParse(document)
    }

    protected abstract fun videoListParse(document: Document): List<Video>
}
