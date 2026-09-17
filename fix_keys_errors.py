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
            
        c = re.sub(r'key\s*=\s*\{\s*category\.id\s*\}', r'key = { it }', c) # Because category in HomeScreen is just a String
        c = re.sub(r'key\s*=\s*\{\s*item\.id\s*\}', r'key = { it.id }', c)
        c = re.sub(r'key\s*=\s*\{\s*_,\s*movie\s*->\s*movie\.id\s*\}', r'key = { _, movie -> movie.id }', c)
        c = re.sub(r'key\s*=\s*\{\s*_,\s*series\s*->\s*series\.id\s*\}', r'key = { _, series -> series.id }', c)
        c = re.sub(r'key\s*=\s*\{\s*_,\s*anime\s*->\s*anime\.id\s*\}', r'key = { _, anime -> anime.id }', c)
        
        with open(filepath, "w") as f:
            f.write(c)
    except Exception as e:
        pass

# Also fix `SeriesViewModel` error: No parameter with name 'newReleasesSeries' found.
with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "r") as f:
    svm = f.read()
    svm = svm.replace("newReleasesSeries = newReleases", "newReleases = newReleases")
with open("app/src/main/java/com/example/ui/screens/series/SeriesViewModel.kt", "w") as f:
    f.write(svm)


