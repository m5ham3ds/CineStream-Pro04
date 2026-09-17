import os
import re

files_to_fix = [
    "app/src/main/java/com/example/ui/screens/home/HomeScreen.kt",
    "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt",
    "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt",
    "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
]

for filepath in files_to_fix:
    with open(filepath, "r") as f:
        content = f.read()
    
    # Check if they have Column(modifier = Modifier.verticalScroll
    if "verticalScroll(scrollState)" in content:
        print(f"Fixing {filepath}")
        
        # Replace `val scrollState = rememberScrollState()`
        content = re.sub(r'val scrollState = rememberScrollState\(\)\s*', '', content)
        
        # Replace `Column(` -> `LazyColumn(` and remove `verticalScroll(scrollState)`
        # Note: we need to wrap the contents inside LazyColumn with `item { ... }`
        
        # This approach using Regex for full layout changes is risky because we might break brackets.
        # Let's inspect the files closely first.

