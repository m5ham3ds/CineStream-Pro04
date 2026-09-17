import re

with open("app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt", "r") as f:
    c = f.read()

c = c.replace("newReleasesAnime = newReleases", "newEpisodes = newReleases")
with open("app/src/main/java/com/example/ui/screens/anime/AnimeViewModel.kt", "w") as f:
    f.write(c)

