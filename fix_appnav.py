import re
with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

old_movie_onplay = """                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = server?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedWebsite = website?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?mediaId=$mediaId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        },"""

new_movie_onplay = """                        onPlay = { title, url, server, website, posterUrl -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = server?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedWebsite = website?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedPoster = URLEncoder.encode(posterUrl, "UTF-8")
                                navController.navigate("player?mediaId=$mediaId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }
                        },"""

content = content.replace(old_movie_onplay, new_movie_onplay)

old_series_onplay = """                        onPlay = { title, url, server, website -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = server?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedWebsite = website?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                navController.navigate("player?mediaId=$mediaId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")
                            }
                        },"""

new_series_onplay = """                        onPlay = { title, url, server, website, posterUrl -> 
                            if (url.startsWith("trailer:")) {
                                val trailerId = url.removePrefix("trailer:")
                                navController.navigate("trailer/$trailerId")
                            } else {
                                val encodedUrl = URLEncoder.encode(url, "UTF-8")
                                val encodedServer = server?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedWebsite = website?.let { URLEncoder.encode(it, "UTF-8") } ?: ""
                                val encodedTitle = URLEncoder.encode(title, "UTF-8")
                                val encodedPoster = URLEncoder.encode(posterUrl, "UTF-8")
                                navController.navigate("player?mediaId=$mediaId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")
                            }
                        },"""

content = content.replace(old_series_onplay, new_series_onplay)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
