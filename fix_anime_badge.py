file_path = "app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('Badge(text = "الأنمي",', 'Badge(text = stringResource(R.string.anime_tab),')

with open(file_path, "w") as f:
    f.write(content)
