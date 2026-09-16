with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

c = c.replace(
    'com.example.utils.AndroidDownloader.downloadVideo(context, url, "${movie.id}.mp4", "${movie.title} - $serverName")',
    'com.example.utils.AndroidDownloader(context).downloadFile(url, "${movie.id}.mp4", "${movie.title} - $serverName")'
)

c = c.replace(
    'com.example.utils.AndroidDownloader.downloadVideo(context, url, "${epIdStr}.mp4", "$fullTitle - $serverName")',
    'com.example.utils.AndroidDownloader(context).downloadFile(url, "${epIdStr}.mp4", "$fullTitle - $serverName")'
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

