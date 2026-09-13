import re
import os

def fix_screen(file_path, default_id):
    if not os.path.exists(file_path):
        return

    with open(file_path, 'r') as f:
        content = f.read()

    # Change CategoryItem definition
    content = content.replace(
        'data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)',
        'data class CategoryItem(val id: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)'
    )

    # Change occurrences of `category.name` to `category.id` for logic, except in `Text`
    content = content.replace('selectedCategory == category.name', 'selectedCategory == category.id')
    content = content.replace('contentDescription = category.name', 'contentDescription = category.label')
    content = content.replace('selectedCategory = category.name', 'selectedCategory = category.id')
    content = content.replace('text = category.name', 'text = category.label')
    
    # We also need to fix the `CategoryItem` initializations.
    # We will do regex substitutions for them.
    # e.g., CategoryItem("Movies", Icons.Default.LocalMovies)
    # -> CategoryItem("Movies", stringResource(R.string.category_movies), Icons.Default.LocalMovies)
    
    if "MoviesScreen" in file_path:
        content = content.replace('CategoryItem("Movies",', 'CategoryItem("Movies", stringResource(R.string.category_movies),')
    elif "SeriesScreen" in file_path:
        content = content.replace('CategoryItem("Series",', 'CategoryItem("Series", stringResource(R.string.category_series),')
    elif "AnimeScreen" in file_path:
        content = content.replace('CategoryItem("Anime",', 'CategoryItem("Anime", stringResource(R.string.category_anime),')
    
    content = content.replace('CategoryItem("Genres",', 'CategoryItem("Genres", stringResource(R.string.category_genres),')
    content = content.replace('CategoryItem("Top Rated",', 'CategoryItem("Top Rated", stringResource(R.string.category_top_rated),')
    
    # For New Releases
    content = content.replace('CategoryItem(stringResource(R.string.new_releases),', 'CategoryItem("New Releases", stringResource(R.string.new_releases),')
    
    # For Trending Anime section title
    content = content.replace('SectionTitleShared("Trending Anime",', 'SectionTitleShared(stringResource(R.string.trending_anime),')
    content = content.replace('SectionTitleShared("Trending Movies",', 'SectionTitleShared(stringResource(R.string.trending_movies),')

    # Change the when blocks in else:
    content = content.replace('stringResource(R.string.new_releases) ->', '"New Releases" ->')

    with open(file_path, 'w') as f:
        f.write(content)

fix_screen("app/src/main/java/com/example/ui/screens/movies/MoviesScreen.kt", "Movies")
fix_screen("app/src/main/java/com/example/ui/screens/series/SeriesScreen.kt", "Series")
fix_screen("app/src/main/java/com/example/ui/screens/anime/AnimeScreen.kt", "Anime")
