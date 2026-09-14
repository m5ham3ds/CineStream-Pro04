import re
import os

# 1. Fix TmdbApiService.kt - Remove ALL explicit language parameters
filepath = "app/src/main/java/com/example/data/remote/TmdbApiService.kt"
with open(filepath, "r") as f:
    text = f.read()

# Remove @Query("language") language: String,
text = re.sub(r',\s*@Query\("language"\) language:\s*String', '', text)
text = re.sub(r'@Query\("language"\) language:\s*String\s*,', '', text)
text = re.sub(r'@Query\("language"\) language:\s*String', '', text)

with open(filepath, "w") as f:
    f.write(text)

# 2. Fix TmdbMediaRepositoryImpl.kt - Remove language passing
repo_path = "app/src/main/java/com/example/data/repository/TmdbMediaRepositoryImpl.kt"
with open(repo_path, "r") as f:
    repo_text = f.read()

repo_text = repo_text.replace("private val language = if (java.util.Locale.getDefault().language == \"ar\") \"ar\" else \"en-US\"", "")
repo_text = repo_text.replace("private val language = java.util.Locale.getDefault().toLanguageTag()", "")
repo_text = repo_text.replace(", language", "")

with open(repo_path, "w") as f:
    f.write(repo_text)

# 3. Fix SharedUI.kt and WatchingScreen.kt - Remove language passing
for fp in ["app/src/main/java/com/example/ui/components/SharedUI.kt", "app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"]:
    with open(fp, "r") as f:
        ui_text = f.read()
    
    # Remove the language parameter from getMovieDetails and getSeriesDetails
    ui_text = ui_text.replace(', if (java.util.Locale.getDefault().language == "ar") "ar" else "en-US"', '')
    ui_text = ui_text.replace(', java.util.Locale.getDefault().toLanguageTag()', '')

    with open(fp, "w") as f:
        f.write(ui_text)

# 4. Fix AppNavigation.kt for Drawer Direction - User wants it from the RIGHT (RTL)
nav_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(nav_path, "r") as f:
    nav_text = f.read()

# Change LayoutDirection.Ltr to LayoutDirection.Rtl for the drawer
nav_text = nav_text.replace("CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr)", "CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Rtl)")
# Wait, I previously used: CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr)
# Let's ensure it's precisely replaced.

with open(nav_path, "w") as f:
    f.write(nav_text)

