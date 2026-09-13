with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "r") as f:
    content = f.read()
content = content.replace('var selectedCategory by remember { mutableStateOf(categories[0]) }\n    val categories =', 'val categories = listOf(stringResource(R.string.home), stringResource(R.string.movies), stringResource(R.string.series), stringResource(R.string.anime))\n    var selectedCategory by remember { mutableStateOf(categories[0]) }')
# Also remove the duplicate val categories line if any.
lines = content.split('\n')
out = []
for i, line in enumerate(lines):
    if 'val categories = listOf(stringResource(R.string.home)' in line and i > 0 and 'var selectedCategory' in lines[i-1]:
        pass # Skip the original one
    else:
        out.append(line)
with open("app/src/main/java/com/example/ui/screens/home/HomeScreen.kt", "w") as f:
    f.write("\n".join(out))
