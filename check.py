def check_braces(filename):
    with open(filename, 'r') as f:
        content = f.read()
    
    open_count = content.count('{')
    close_count = content.count('}')
    print(f"{filename}: open={open_count}, close={close_count}")

check_braces("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt")
check_braces("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt")
check_braces("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt")
