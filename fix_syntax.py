import re

def fix_file(filepath):
    with open(filepath, "r") as f:
        c = f.read()

    # Find where the main function ends by looking at the first @Composable after our Crossfade,
    # or the end of the file.
    crossfade_match = re.search(r'Crossfade\(targetState =', c)
    if not crossfade_match:
        print(f"No Crossfade in {filepath}")
        return

    # Find the next @Composable after Crossfade
    next_composable = re.search(r'@Composable', c[crossfade_match.end():])
    
    if next_composable:
        end_search_index = crossfade_match.end() + next_composable.start()
    else:
        end_search_index = len(c)
        
    # Search backwards from end_search_index for "    }}"
    # The last "    }}" before the next composable or EOF is the one we want to replace.
    last_braces = c.rfind("    }}", crossfade_match.end(), end_search_index)
    if last_braces != -1:
        c = c[:last_braces] + "        }\n    }\n}" + c[last_braces+6:]
        with open(filepath, "w") as f:
            f.write(c)
        print(f"Fixed {filepath}")
    else:
        print(f"Could not find closing braces for {filepath}")

files = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt",
    "app/src/main/java/com/example/ui/screens/about/AboutScreen.kt",
    "app/src/main/java/com/example/ui/screens/social/SocialScreen.kt",
    "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
]

for f in files:
    fix_file(f)

