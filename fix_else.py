for filename in ["app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt"]:
    with open(filename, "r") as f:
        content = f.read()
    
    content = content.replace("}\n} else {", "} else {")
    
    with open(filename, "w") as f:
        f.write(content)
