import re
with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    content = f.read()

content = content.replace(
    'navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")',
    'val encodedPoster = java.net.URLEncoder.encode(posterUrl, "UTF-8")\n                                navController.navigate("player?mediaId=$movieId&isMovie=true&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")'
)

content = content.replace(
    'navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite")',
    'val encodedPoster = java.net.URLEncoder.encode(posterUrl, "UTF-8")\n                                navController.navigate("player?mediaId=$seriesId&isMovie=false&title=$encodedTitle&url=$encodedUrl&server=$encodedServer&website=$encodedWebsite&poster=$encodedPoster")'
)

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(content)
