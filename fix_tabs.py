import os

files = [
    "app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/PopularScreen.kt",
    "app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt"
]

for file_path in files:
    with open(file_path, "r") as f:
        content = f.read()

    # 1. Add string resources
    content = content.replace("val animeStr = stringResource(R.string.anime)",
"""val allStr = stringResource(R.string.all)
    val moviesStr = stringResource(R.string.movies)
    val seriesStr = stringResource(R.string.series)
    val animeStr = stringResource(R.string.anime)""")
    
    # 2. Update tabsList
    content = content.replace('val tabsList = listOf("All", "Movies", "TV Series", animeStr)', 'val tabsList = listOf(allStr, moviesStr, seriesStr, animeStr)')
    content = content.replace('val tabsList = listOf("All", "Movies", "Series", animeStr)', 'val tabsList = listOf(allStr, moviesStr, seriesStr, animeStr)')

    # 3. Update when (tab)
    content = content.replace('"Movies" ->', 'moviesStr ->')
    content = content.replace('"Series" ->', 'seriesStr ->')
    content = content.replace('"TV Series" ->', 'seriesStr ->')

    with open(file_path, "w") as f:
        f.write(content)
