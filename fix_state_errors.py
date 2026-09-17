import re

def patch_file(filepath, list_check):
    with open(filepath, "r") as f:
        c = f.read()
    
    # regex to match: if (uiState.error != null && uiState.*.isEmpty()...) { MediaScreenSkeleton(); return }
    pattern = r'    if \(uiState\.error != null[^\{]+\{\s+MediaScreenSkeleton\(\)\s+return\s+\}'
    replacement = f'''    if (uiState.error != null && {list_check}) {{
        MediaScreenSkeleton()
        return
    }}'''
    c = re.sub(pattern, replacement, c, flags=re.DOTALL)
    
    with open(filepath, "w") as f:
        f.write(c)

patch_file("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "uiState.trendingMovies.isEmpty()")
patch_file("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "uiState.movies.isEmpty()")
patch_file("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "uiState.series.isEmpty()")
patch_file("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "uiState.animeSeries.isEmpty()")

