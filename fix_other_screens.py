import re

def fix_screen(file_path, movies_prop, series_prop, anime_prop):
    with open(file_path, "r") as f:
        text = f.read()

    # The block looks like:
    #         moviesStr -> uiState.X.map { it to true }
    #         seriesStr -> uiState.Y.map { it to false }
    #         animeStr -> uiState.Z.map { it to false }
    #         else -> (uiState.X.map { it to true } + uiState.Y.map { it to false } + uiState.Z.map { it to false })

    text = re.sub(r'moviesStr -> uiState\.[A-Za-z]+\.map', f'moviesStr -> uiState.{movies_prop}.map', text)
    text = re.sub(r'seriesStr -> uiState\.[A-Za-z]+\.map', f'seriesStr -> uiState.{series_prop}.map', text)
    text = re.sub(r'animeStr -> uiState\.[A-Za-z]+\.map', f'animeStr -> uiState.{anime_prop}.map', text)

    # For the else block, we can just replace the whole 'else -> ...' line
    else_line = f"        else -> (uiState.{movies_prop}.map {{ it to true }} + uiState.{series_prop}.map {{ it to false }} + uiState.{anime_prop}.map {{ it to false }})"
    text = re.sub(r'else -> .*', else_line, text)

    with open(file_path, "w") as f:
        f.write(text)

fix_screen("app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt", "trendingMovies", "trendingSeries", "trendingAnime")
fix_screen("app/src/main/java/com/example/ui/screens/home/PopularScreen.kt", "popularMovies", "popularSeries", "popularAnime")
fix_screen("app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt", "newReleasesMovies", "newReleasesSeries", "newReleasesAnime")

