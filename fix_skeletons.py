import re

files_and_checks = {
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt": "uiState.trendingMovies.isEmpty()",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt": "uiState.trendingMovies.isEmpty() && uiState.movies.isEmpty()",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt": "uiState.trendingSeries.isEmpty() && uiState.series.isEmpty()",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt": "uiState.trendingAnime.isEmpty() && uiState.series.isEmpty()"
}

for filepath, empty_check in files_and_checks.items():
    with open(filepath, "r") as f:
        content = f.read()
    
    # replace the error check with a data check
    # find: if (uiState.error != null && ...) { MediaScreenSkeleton() return }
    # or just replace the whole skeleton block.
    
    # We'll just replace the isLoading block to include the empty check.
    # Current:
    #     if (uiState.isLoading || !transitionFinished) {
    #         MediaScreenSkeleton()
    #         return
    #     }
    #     if (uiState.error != null && uiState.something.isEmpty()) {
    #         MediaScreenSkeleton()
    #         return
    #     }
    
    # regex to find the two if statements and replace them with one.
    
    pattern = r'if\s*\(\s*uiState\.isLoading\s*\|\|\s*!transitionFinished\s*\)\s*\{\s*MediaScreenSkeleton\(\)\s*return\s*\}\s*if\s*\(\s*uiState\.error\s*!=\s*null\s*&&\s*uiState\.[a-zA-Z0-9_]+\.isEmpty\(\)\s*\)\s*\{\s*MediaScreenSkeleton\(\)\s*return\s*\}'
    
    new_block = f"""if (uiState.isLoading || !transitionFinished || ({empty_check})) {{
        MediaScreenSkeleton()
        return
    }}"""
    
    content = re.sub(pattern, new_block, content, count=1)
    
    # also remove any left over if (uiState.error != null ... just in case
    
    with open(filepath, "w") as f:
        f.write(content)

