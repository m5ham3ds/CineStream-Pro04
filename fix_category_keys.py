import re

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        c = f.read()
        
    c = re.sub(r'items\(\s*categories\s*,\s*key\s*=\s*\{\s*it\s*\}\s*\)\s*\{\s*category\s*->', r'items(categories, key = { it.id }) { category ->', c)
    
    with open(filepath, "w") as f:
        f.write(c)
