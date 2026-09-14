import re

file_path = "app/src/main/java/com/example/ui/screens/details/PersonDetailsScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('SectionHeader("Top Movies")', 'SectionHeader(stringResource(R.string.top_movies))')
content = content.replace('SectionHeader("Top TV Shows")', 'SectionHeader(stringResource(R.string.top_shows))')

with open(file_path, "w") as f:
    f.write(content)
