package com.example.source

import okhttp3.Request
import org.jsoup.nodes.Document
import org.jsoup.nodes.Element

/**
 * Example implementation of a source using Jsoup.
 * You can replace this with your actual scraping logic for the websites you provided.
 */
class ExampleAnimeSource : ParsedHttpSource() {
    override val name: String = "Example Source"
    override val lang: String = "ar"
    override val baseUrl: String = "https://example.com"

    override fun popularAnimeRequest(page: Int): Request {
        return Request.Builder().url("$baseUrl/popular?page=$page").build()
    }

    override fun popularAnimeSelector(document: Document): List<Element> {
        return document.select("div.anime-item")
    }

    override fun popularAnimeFromElement(element: Element): Anime {
        return Anime(
            title = element.select("h3").text(),
            url = element.select("a").attr("href"),
            thumbnailUrl = element.select("img").attr("src")
        )
    }

    override fun searchAnimeRequest(query: String, page: Int): Request {
        return Request.Builder().url("$baseUrl/search?q=$query&page=$page").build()
    }

    override fun searchAnimeSelector(document: Document): List<Element> = popularAnimeSelector(document)

    override fun searchAnimeFromElement(element: Element): Anime = popularAnimeFromElement(element)

    override fun animeDetailsParse(document: Document, anime: Anime): Anime {
        return anime.copy(
            description = document.select("div.description").text(),
            genre = document.select("div.genres").text()
        )
    }

    override fun episodeListSelector(document: Document): List<Element> {
        return document.select("ul.episodes li")
    }

    override fun episodeFromElement(element: Element): Episode {
        return Episode(
            name = element.select("a").text(),
            url = element.select("a").attr("href")
        )
    }

    override fun videoListParse(document: Document): List<Video> {
        // This is where you would extract the actual MP4/M3U8 link from the episode page
        return listOf(
            Video(
                quality = "720p",
                // This is a REAL mp4 link that works in ExoPlayer, used for testing:
                videoUrl = "https://commondatastorage.googleapis.com/gtv-videos-bucket/sample/BigBuckBunny.mp4"
            )
        )
    }
}
