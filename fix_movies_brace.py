with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "r") as f:
    content = f.read()

content = content.replace("    }\nif (showBottomSheet) {", "    }\n    }\nif (showBottomSheet) {")

with open("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "w") as f:
    f.write(content)
