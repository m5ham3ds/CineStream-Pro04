for filename in ["app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt"]:
    with open(filename, "r") as f:
        content = f.read()

    # Find the last `}`
    last_brace = content.rfind("}")
    if last_brace != -1:
        content = content[:last_brace] + content[last_brace+1:]
        with open(filename, "w") as f:
            f.write(content)
