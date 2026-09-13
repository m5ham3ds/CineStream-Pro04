#!/bin/bash
FILES=(
"app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt"
"app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt"
"app/src/main/java/com/example/ui/screens/home/PopularScreen.kt"
"app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt"
"app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt"
)

for file in "${FILES[@]}"; do
    if [ ! -f "$file" ]; then
        continue
    fi
    
    # Check if HorizontalPager is already imported
    if ! grep -q "HorizontalPager" "$file"; then
        sed -i 's/import androidx.compose.foundation.layout.*/import androidx.compose.foundation.pager.HorizontalPager\nimport androidx.compose.foundation.pager.rememberPagerState\nimport kotlinx.coroutines.launch\n&/' "$file"
    fi

    # Replace var selectedTab by remember { mutableStateOf("All") }
    sed -i 's/var selectedTab by remember { mutableStateOf("All") }/val tabs = listOf("All", "Movies", "Series", stringResource(R.string.anime))\n    val pagerState = rememberPagerState(pageCount = { tabs.size })\n    val coroutineScope = rememberCoroutineScope()\n    val selectedTab = tabs[pagerState.currentPage]/g' "$file"

    # Remove the inner val tabs = listOf(...)
    sed -i '/val tabs = listOf("All", "Movies", "Series", stringResource(R.string.anime))/d' "$file"
    # But wait, we just added it above, so the inner one and outer one will both match.
    # Actually it's better to do a proper replacement with python script.
done
