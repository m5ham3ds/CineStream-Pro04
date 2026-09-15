import re
with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_route = """                composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val url = backStackEntry.arguments?.getString("url") ?: ""
                    val server = backStackEntry.arguments?.getString("server") ?: ""
                    val website = backStackEntry.arguments?.getString("website") ?: ""
                    
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        url = decodedUrl,
                        targetServer = decodedServer,
                        website = decodedWebsite,
                        onBack = { navController.popBackStack() }
                    )
                }"""

new_route = """                composable("player?mediaId={mediaId}&isMovie={isMovie}&title={title}&url={url}&server={server}&website={website}&poster={poster}") { backStackEntry ->
                    val mediaId = backStackEntry.arguments?.getString("mediaId") ?: ""
                    val isMovieStr = backStackEntry.arguments?.getString("isMovie") ?: "true"
                    val isMovie = isMovieStr.toBoolean()
                    val title = backStackEntry.arguments?.getString("title") ?: "Unknown"
                    val url = backStackEntry.arguments?.getString("url") ?: ""
                    val server = backStackEntry.arguments?.getString("server") ?: ""
                    val website = backStackEntry.arguments?.getString("website") ?: ""
                    val poster = backStackEntry.arguments?.getString("poster") ?: ""
                    
                    val decodedTitle = URLDecoder.decode(title, "UTF-8")
                    val decodedUrl = if (url.isNotEmpty()) URLDecoder.decode(url, "UTF-8") else ""
                    val decodedServer = if (server.isNotEmpty()) URLDecoder.decode(server, "UTF-8") else ""
                    val decodedWebsite = if (website.isNotEmpty()) URLDecoder.decode(website, "UTF-8") else ""
                    val decodedPoster = if (poster.isNotEmpty()) URLDecoder.decode(poster, "UTF-8") else ""
                    
                    com.example.ui.screens.player.PlayerScreen(
                        mediaId = mediaId,
                        isMovie = isMovie,
                        title = decodedTitle,
                        posterUrl = decodedPoster,
                        url = decodedUrl,
                        targetServer = decodedServer,
                        website = decodedWebsite,
                        onBack = { navController.popBackStack() }
                    )
                }"""

content = content.replace(old_route, new_route)
with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
