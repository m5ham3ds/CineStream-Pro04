import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    c = f.read()

# Series Details navigation update
target1 = """onPlayEpisode = { episode, url, server, website ->
                                val encodedTitle = URLEncoder.encode("${series.title} - ${episode.title}", "UTF-8")
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = URLEncoder.encode(server, "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website, "UTF-8")
                                val encodedPoster = URLEncoder.encode(series.posterUrl ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }"""

replace1 = """onPlayEpisode = { episode, url, server, website ->
                                val encodedTitle = URLEncoder.encode("${series.title} - ${episode.title}", "UTF-8")
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = URLEncoder.encode(server, "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website, "UTF-8")
                                val encodedPoster = URLEncoder.encode(series.posterUrl ?: "", "UTF-8")
                                val epId = episode.id.toString()
                                navController.navigate("player?mediaId=$seriesId&episodeId=$epId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }"""
c = c.replace(target1, replace1)

# Movie Details navigation update
target2 = """onPlay = { url, server, website ->
                                val encodedTitle = URLEncoder.encode(movie.title, "UTF-8")
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = URLEncoder.encode(server, "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website, "UTF-8")
                                val encodedPoster = URLEncoder.encode(movie.posterUrl ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }"""

replace2 = """onPlay = { url, server, website ->
                                val encodedTitle = URLEncoder.encode(movie.title, "UTF-8")
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = URLEncoder.encode(server, "UTF-8")
                                val encodedWebsite = URLEncoder.encode(website, "UTF-8")
                                val encodedPoster = URLEncoder.encode(movie.posterUrl ?: "", "UTF-8")
                                navController.navigate("player?mediaId=$movieId&episodeId=&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }"""
c = c.replace(target2, replace2)

# Route definition
target3 = """composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}&poster={poster}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()"""

replace3 = """composable("player?mediaId={mediaId}&episodeId={episodeId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}&poster={poster}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val episodeId = backStackEntry.arguments?.getString("episodeId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()"""
c = c.replace(target3, replace3)

# PlayerScreen call
target4 = """com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,"""

replace4 = """com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        episodeId = episodeId,
                        isMovie = isMovie,
                        title = decodedTitle,"""
c = c.replace(target4, replace4)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(c)
