import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# For Movie
content = content.replace("isAnime = movie.genres.any { it.contains(\"Animation\", ignoreCase = true) || it.contains(\"Anime\", ignoreCase = true) },\n                    onDismiss", "isAnime = movie.genres.any { it.contains(\"Animation\", ignoreCase = true) || it.contains(\"Anime\", ignoreCase = true) },\n                    isDownloadMode = isDownloadMode,\n                    onDismiss")

# For Series
content = content.replace("isAnime = series.genres.any { it.contains(\"Animation\", ignoreCase = true) || it.contains(\"Anime\", ignoreCase = true) },\n                    onDismiss", "isAnime = series.genres.any { it.contains(\"Animation\", ignoreCase = true) || it.contains(\"Anime\", ignoreCase = true) },\n                    isDownloadMode = isDownloadMode,\n                    onDismiss")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
