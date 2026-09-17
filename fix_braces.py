import re
import os

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt",
    "app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt",
    "app/src/main/java/com/example/ui/screens/about/AboutScreen.kt",
    "app/src/main/java/com/example/ui/screens/social/SocialScreen.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
]

for filepath in files_to_fix:
    if not os.path.exists(filepath):
        continue
    with open(filepath, "r") as f:
        c = f.read()

    # We need to find where the missing brace belongs.
    # The error says "Expecting '}'" at the end of the file or function.
    # We can just use the same brace counting logic, BUT since the file is currently imbalanced, brace counting will fail!
    # Let's count open/close braces in the whole file.
    
    open_braces = c.count('{')
    close_braces = c.count('}')
    
    if open_braces > close_braces:
        diff = open_braces - close_braces
        print(f"{filepath} missing {diff} braces")
