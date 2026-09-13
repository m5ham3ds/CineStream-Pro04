file_path = "app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('CategoryItem(animeStr, Icons.Default.LocalMovies),', 'CategoryItem("Anime", stringResource(R.string.category_anime), Icons.Default.LocalMovies),')
# Change initial selected category back to "Anime" (the id) instead of localized string, to match logic.
content = content.replace('var selectedCategory by remember { mutableStateOf(animeStr) }', 'var selectedCategory by remember { mutableStateOf("Anime") }')

with open(file_path, "w") as f:
    f.write(content)
