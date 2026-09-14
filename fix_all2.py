import re

# Fix Tmdb language
filepath = "app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt"
with open(filepath, "r") as f:
    text = f.read()

text = text.replace('private val language = java.util.Locale.getDefault().toLanguageTag()', 'private val language = if (java.util.Locale.getDefault().language == "ar") "ar" else "en-US"')

with open(filepath, "w") as f:
    f.write(text)

# Also fix the calls in SharedUI and WatchingScreen
for fp in ["app/src/main/java/com/example/ui/components/SharedUI.kt", "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"]:
    with open(fp, "r") as f:
        text = f.read()
    text = text.replace('java.util.Locale.getDefault().toLanguageTag()', 'if (java.util.Locale.getDefault().language == "ar") "ar" else "en-US"')
    with open(fp, "w") as f:
        f.write(text)

