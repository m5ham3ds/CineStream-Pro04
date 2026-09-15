import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace("onPlay: (String, String, String?, String?) -> Unit", "onPlay: (String, String, String?, String?, String) -> Unit")

content = content.replace('onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null)', 'onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null, movie.posterUrl)')
content = content.replace('onPlay(movie.title, url, serverName, website)', 'onPlay(movie.title, url, serverName, website, movie.posterUrl)')

content = content.replace('onPlay(fullTitle, "local_offline_file://${series.id}_${episode.id}", null, null)', 'onPlay(fullTitle, "local_offline_file://${series.id}_${episode.id}", null, null, episode.thumbnailUrl)')
content = content.replace('onPlay(fullTitle, url, serverName, website)', 'onPlay(fullTitle, url, serverName, website, ep.thumbnailUrl)')

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
