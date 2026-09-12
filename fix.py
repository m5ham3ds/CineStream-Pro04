import re

for filename in ["app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt"]:
    with open(filename, "r") as f:
        content = f.read()

    # Find the end of the `if (selectedCategory == "...")` block to make sure it's properly closed before `else {`
    if "} else {" in content:
        parts = content.split("} else {", 1)
        if not parts[0].strip().endswith("}"):
            content = parts[0] + "}\n} else {" + parts[1]
    
    # Try closing up open braces. Let's just append '}' at the end if there are unmatched ones.
    # Alternatively we can just do a very simple fix based on the errors.
    
    with open(filename, "w") as f:
        f.write(content)
