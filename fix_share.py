file_path = "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('ContentTypeCard("Movies",', 'ContentTypeCard(stringResource(R.string.category_movies),')
content = content.replace('ContentTypeCard("TV Series",', 'ContentTypeCard(stringResource(R.string.category_series),')
content = content.replace('ContentTypeCard("Anime",', 'ContentTypeCard(stringResource(R.string.category_anime),')
content = content.replace('ContentTypeCard("All Files",', 'ContentTypeCard("All Files",') # or add stringResource if needed

with open(file_path, "w") as f:
    f.write(content)
