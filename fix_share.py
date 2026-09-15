import re
with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "r") as f:
    content = f.read()

old_content = """                downloadRepository.addCompletedDownload(
                    DownloadItem(
                        id = id,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        quality = "Shared",
                        progress = 1f,
                        isCompleted = true
                    )
                )"""

new_content = """                downloadRepository.addCompletedDownload(
                    DownloadItem(
                        id = id,
                        mediaId = id,
                        title = title,
                        posterUrl = posterUrl,
                        isMovie = isMovie,
                        quality = "Shared",
                        progress = 1f,
                        isCompleted = true
                    )
                )"""

content = content.replace(old_content, new_content)

with open("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", "w") as f:
    f.write(content)
