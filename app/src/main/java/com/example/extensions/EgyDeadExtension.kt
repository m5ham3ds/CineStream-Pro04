package com.example.extensions

import java.net.URLEncoder

object EgyDeadExtension : ProviderExtension {

    override val id: String = "egydead"
    override val name: String = "ايجي ديد"
    override val baseUrl: String = "https://tv10.egydead.live"
    override val isAnime: Boolean = true
    override val isMovie: Boolean = true
    override val isSeries: Boolean = true
    override val lang: String = "ar"
    override val iconUrl: String = "https://tv10.egydead.live/wp-content/uploads/2019/01/cropped-yXYdE2f-192x192.png"

    override fun getSearchUrl(titleOriginal: String, titleClean: String): String {
        return "$baseUrl?s=${URLEncoder.encode(titleClean, "UTF-8")}"
    }

    override fun getExtractionScript(isMovie: Boolean, episode: Int, title: String): String {
        return """
            (function() {
                window.targetTitle = "$title";
                window.targetEpisode = $episode;
                window.isMovie = $isMovie;

                function getQueryParam(param) {
                    let urlParams = new URLSearchParams(window.location.search);
                    return urlParams.get(param);
                }

                function handleSearch() {
                    let searchTitle = window.targetTitle;
                    if (!searchTitle) return false;

                    let interval = setInterval(function() {
                        let items = document.querySelectorAll('.movieItem a');
                        let found = false;
                        for (let el of items) {
                            let titleEl = el.querySelector('h1.BottomTitle');
                            if (!titleEl) continue;
                            let titleText = titleEl.innerText.trim();
                            if (titleText.toLowerCase() === searchTitle.toLowerCase()) {
                                found = true;
                                clearInterval(interval);
                                el.click();
                                break;
                            }
                        }
                    }, 500);

                    setTimeout(function() {
                        clearInterval(interval);
                    }, 15000);

                    return true;
                }

                function handleDetails() {
                    if (!document.querySelector('.single-header')) return false;

                    let episodeLinks = document.querySelectorAll('.EpsList li a');

                    if (window.isMovie || episodeLinks.length === 0) {
                        let watchBtn = document.querySelector('.BtnsGroup .watchNow button');
                        if (watchBtn) {
                            watchBtn.click();
                        }
                        return true;
                    }

                    let targetEp = window.targetEpisode;
                    if (targetEp > 0) {
                        let found = false;
                        for (let link of episodeLinks) {
                            let epText = link.innerText.trim();
                            let match = epText.match(/\d+/);
                            let epNum = match ? parseInt(match[0], 10) : null;
                            if (epNum === targetEp) {
                                found = true;
                                link.click();
                                break;
                            }
                        }
                        if (!found && episodeLinks.length > 0) {
                            episodeLinks[0].click();
                        }
                    } else {
                        if (episodeLinks.length > 0) {
                            episodeLinks[0].click();
                        }
                    }
                    return true;
                }

                function handleWatchPage() {
                    let serverSelector = '.mob-servers ul li';
                    if (!document.querySelector(serverSelector)) {
                        serverSelector = '.serversList li';
                    }

                    let serverItems = [];
                    let interval = setInterval(function() {
                        let items = document.querySelectorAll(serverSelector);
                        if (items.length > 0) {
                            clearInterval(interval);
                            for (let el of items) {
                                let nameEl = el.querySelector('span p') || el.querySelector('span');
                                let name = nameEl ? nameEl.innerText.trim() : 'سيرفر';
                                let url = el.getAttribute('data-link');
                                if (url) {
                                    serverItems.push({ name: name, url: url });
                                }
                            }

                            // ايضا استخراج سيرفرات التحميل
                            let dlItems = document.querySelectorAll('.donwload-servers-list li');
                            for (let dl of dlItems) {
                                let nameEl = dl.querySelector('.ser-name');
                                let qualityEl = dl.querySelector('.server-info em');
                                let linkEl = dl.querySelector('a.ser-link');
                                if (linkEl && linkEl.href) {
                                    let name = nameEl ? nameEl.innerText.trim() : 'تحميل';
                                    if (qualityEl) name += ' (' + qualityEl.innerText.trim() + ')';
                                    serverItems.push({ name: name, url: linkEl.href });
                                }
                            }

                            if (typeof AndroidBridge !== 'undefined' && serverItems.length > 0) {
                                AndroidBridge.sendServersV2(JSON.stringify(serverItems), window.location.href);
                            } else if (serverItems.length === 0 && typeof AndroidBridge !== 'undefined') {
                                AndroidBridge.sendFailed();
                            }
                        }
                    }, 500);

                    setTimeout(function() {
                        clearInterval(interval);
                        if (serverItems.length === 0 && typeof AndroidBridge !== 'undefined') {
                            AndroidBridge.sendFailed();
                        }
                    }, 20000);

                    return true;
                }

                if (document.querySelector('.posts-list') || document.querySelector('.pin-posts-list')) {
                    handleSearch();
                    return;
                }

                if (document.querySelector('.single-header')) {
                    handleDetails();
                    return;
                }

                if (document.querySelector('.mob-servers') || document.querySelector('.serversList') || document.querySelector('.watchAreaMaster')) {
                    handleWatchPage();
                    return;
                }

                if (typeof AndroidBridge !== 'undefined') {
                    AndroidBridge.sendFailed();
                }
            })();
        """.trimIndent()
    }
}
