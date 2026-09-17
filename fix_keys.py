import re

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt",
    "app/src/main/java/com/example/ui/components/SharedComponents.kt"
]

for filepath in files_to_fix:
    try:
        with open(filepath, "r") as f:
            c = f.read()
            
        # replace `items(movieHistoryItems) {` with `items(movieHistoryItems, key = { it.id }) {`
        # But be careful, sometimes it's `items(uiState.trendingMovies) { movie ->`
        
        # A simpler regex: `items\(([^)]+)\)\s*\{\s*([a-zA-Z0-9_]+)\s*->`
        # wait, sometimes it's `itemsIndexed`
        
        c = re.sub(r'items\(([^,]+)\)\s*\{\s*([a-zA-Z0-9_]+)\s*->', r'items(\1, key = { \2.id }) { \2 ->', c)
        c = re.sub(r'itemsIndexed\(([^,]+)\)\s*\{\s*([a-zA-Z0-9_]+),\s*([a-zA-Z0-9_]+)\s*->', r'itemsIndexed(\1, key = { _, \3 -> \3.id }) { \2, \3 ->', c)
        
        with open(filepath, "w") as f:
            f.write(c)
    except Exception as e:
        pass

