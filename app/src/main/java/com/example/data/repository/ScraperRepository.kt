package com.example.data.repository

import kotlinx.coroutines.Dispatchers
import kotlinx.coroutines.withContext
import org.jsoup.Jsoup
import java.net.URLEncoder

object ScraperRepository {

    suspend fun getWatchUrl(website: String, query: String, isMovie: Boolean, season: Int, episode: Int): String? = withContext(Dispatchers.IO) {
        val encodedQuery = URLEncoder.encode(query, "UTF-8")
        
        fun connect(url: String) = Jsoup.connect(url)
            .userAgent("Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36")
            .header("Accept-Language", "ar,en-US;q=0.9,en;q=0.8")
            .referrer("https://google.com/")
            .timeout(10000)
            
        try {
                        when (website) {
                "tv10.egydead.live" -> {
                    val doc = connect("https://tv10.egydead.live/page/1/?s=$encodedQuery").get()
                    val link = doc.select("section.main-section ul.posts-list li.movieItem a, div.pin-posts-list ul li.movieItem a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val seasonItems = seriesDoc.select("div.seasons-list ul li.movieItem a")
                    val seasonLink = if (seasonItems.size >= season) seasonItems[season - 1].attr("href") else link
                    val episodesDoc = if (seasonLink != link) connect(seasonLink).get() else seriesDoc
                    val episodeLinks = episodesDoc.select("div.EpsList li a")
                    for (epLink in episodeLinks) {
                        if (epLink.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext epLink.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "a.qfilm.tv" -> {
                    val doc = connect("https://a.qfilm.tv/search.php?keywords=$encodedQuery").get()
                    return@withContext doc.select("ul.pm-ul-browse-videos li a[href*='watch.php']").first()?.attr("href")
                }
                "animeat.net" -> {
                    return@withContext "https://animeat.net/?search=$encodedQuery"
                }
                "arabanime.net" -> {
                    return@withContext "https://www.arabanime.net/?s=$encodedQuery"
                }
                "arabseed-tv.com" -> {
                    val doc = connect("https://arabseed-tv.com/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        if (ep.select("div.epi__num b, div.episode__title em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "arabseed.wine" -> {
                    val doc = connect("https://www.arabseed.wine/page/1/?s=$encodedQuery").get()
                    val link = doc.select("ul.movie__blocks__ul li a.movie__block, ul.series__ul li a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes__list li a, ul.episodes__blocks__holder a.episode__item")
                    for (ep in episodeLinks) {
                        if (ep.select("div.epi__num b, div.episode__title em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "det.animerco.org" -> {
                    val doc = connect("https://det.animerco.org/?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes-list li a")
                    for (ep in episodeLinks) {
                        if (ep.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "e.cimalight.co" -> {
                    val doc = connect("https://e.cimalight.co/search.php?keywords=$encodedQuery").get()
                    return@withContext doc.select("ul.row.pm-ul-browse-videos li a[href*='watch.php?vid=']").first()?.attr("href")
                }
                "egybests.live" -> {
                    val doc = connect("https://egybests.live/?s=$encodedQuery&page=1").get()
                    val link = doc.select("a.postBlock").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.all-episodes a, div.EpisodesList a")
                    for (ep in episodeLinks) {
                        if (ep.text().filter { it.isDigit() } == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "stardima.com" -> {
                    val doc = connect("https://www.stardima.com/search?query=$encodedQuery&page=1").get()
                    val link = doc.select("div.embla__slide a[href^='/tvshow/']").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    val fullLink = if (link.startsWith("/")) "https://www.stardima.com$link" else link
                    if (isMovie) return@withContext fullLink
                    val seriesDoc = connect(fullLink).get()
                    val episodeLinks = seriesDoc.select("ul#episodes-list-container li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "uo.brstej.com" -> {
                    val doc = connect("https://uo.brstej.com/search.php?keywords=$encodedQuery").get()
                    val link = doc.select("ul.pm-ul-browse-videos li div.pm-video-thumb a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("div.SeasonsEpisodes a")
                    for (ep in episodeLinks) {
                        if (ep.select("em").text() == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "vip.animeluxe.org" -> {
                    val doc = connect("https://vip.animeluxe.org/anime?s=$encodedQuery&page=1").get()
                    val link = doc.select("div.media-section div.row div.box-5x1.media-block a.image").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.episodes-lists li a[href*='/episodes/']")
                    for (ep in episodeLinks) {
                        val numText = (ep.selectFirst("h3")?.text() ?: ep.ownText()).replace("\\D+".toRegex(), "")
                        if (numText == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "watch.stardima.com" -> {
                    val doc = connect("https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1").get()
                    val link = doc.select("article.item div.data h3 a, article.item div.poster a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li.episode-list-item a")
                    for (ep in episodeLinks) {
                        if (ep.text().contains(episode.toString())) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "witanime.you", "w1.anime4up.rest", "animeblkom.net" -> {
                    val domain = website
                    val doc = connect("https://$domain/?search_param=animes&s=$encodedQuery").get()
                    val link = doc.select("div.owl-animes .anime-card-container a.overlay, div.episodes-card-container a.overlay, .anime-card-themex .hover a, .anime-card a").first()?.attr("href")
                    if (link == null) return@withContext getSearchUrl(website, query)
                    if (isMovie) return@withContext link
                    val seriesDoc = connect(link).get()
                    val episodeLinks = seriesDoc.select("ul.all-episodes-list li a, .episodes-list-content .episodes-card-title a, .episodes-links li a")
                    for (ep in episodeLinks) {
                        if (ep.text().replace("\\D+".toRegex(), "") == episode.toString()) return@withContext ep.attr("href")
                    }
                    return@withContext episodeLinks.first()?.attr("href")
                }
                "topcinema.io", "laaroza.space", "z1.almeshkah.net" -> {
                    return@withContext "https://$website/search.php?keywords=$encodedQuery"
                }
            }
        } catch (e: Exception) {
            e.printStackTrace()
        }
        return@withContext getSearchUrl(website, query)
    }

    private fun getSearchUrl(website: String, query: String): String {
        val encodedQuery = java.net.URLEncoder.encode(query, "UTF-8")
        return when (website) {
            "animeat.net" -> "https://animeat.net/?s=$encodedQuery"
            "arabseed-tv.com" -> "https://arabseed-tv.com/page/1/?s=$encodedQuery"
            "arabseed.wine" -> "https://www.arabseed.wine/page/1/?s=$encodedQuery"
            "det.animerco.org" -> "https://det.animerco.org/?s=$encodedQuery&page=1"
            "e.cimalight.co" -> "https://e.cimalight.co/search.php?keywords=$encodedQuery"
            "egybests.live" -> "https://egybests.live/?s=$encodedQuery&page=1"
            "stardima.com" -> "https://www.stardima.com/search?query=$encodedQuery&page=1"
            "uo.brstej.com" -> "https://uo.brstej.com/search.php?keywords=$encodedQuery"
            "vip.animeluxe.org" -> "https://vip.animeluxe.org/anime?s=$encodedQuery&page=1"
            "watch.stardima.com" -> "https://watch.stardima.com/watch/search_gcse-2/?s=$encodedQuery&page=1"
            "witanime.you", "w1.anime4up.rest", "animeblkom.net" -> "https://$website/?search_param=animes&s=$encodedQuery"
            "topcinema.io", "laaroza.space", "z1.almeshkah.net" -> "https://$website/search.php?keywords=$encodedQuery"
            else -> "https://$website/?s=$encodedQuery"
        }
    }
}

