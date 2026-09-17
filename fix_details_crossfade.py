import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# Fix MovieDetailsScreen
target_movie_cond = r'        if \(uiState\.isLoading \|\| !transitionFinished \|\| uiState\.movie == null\) \{\s+DetailsSkeleton\(\)\s+\}\s+else if \(uiState\.movie != null\) \{'
replacement_movie_cond = r'''        val showSkeleton = uiState.isLoading || !transitionFinished || uiState.movie == null
        androidx.compose.animation.Crossfade(targetState = showSkeleton, animationSpec = androidx.compose.animation.core.tween(800), label = "fade") { loading ->
            if (loading) {
                DetailsSkeleton()
            } else {'''
c = re.sub(target_movie_cond, replacement_movie_cond, c)

# Fix SeriesDetailsScreen
# Series has:
#        val series = uiState.series
#        if ((uiState.isLoading || !transitionFinished) && series == null) {
#            DetailsSkeleton()
#            return@PullToRefreshBox
#        }
#        if (series == null && !uiState.isLoading) {
#            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
#                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
#            }
#            return@PullToRefreshBox
#        }
#        if (series != null) {

target_series_cond = r'        val series = uiState\.series\s+if \(\(uiState\.isLoading \|\| !transitionFinished\) && series == null\) \{\s+DetailsSkeleton\(\)\s+return@PullToRefreshBox\s+\}\s+if \(series == null && !uiState\.isLoading\) \{\s+Box\(modifier = Modifier\.fillMaxSize\(\), contentAlignment = Alignment\.Center\) \{\s+Text\(uiState\.error \?: "Failed to load details", color = MaterialTheme\.colorScheme\.error\)\s+\}\s+return@PullToRefreshBox\s+\}\s+if \(series != null\) \{'

replacement_series_cond = r'''        val series = uiState.series
        val showSkeleton = uiState.isLoading || !transitionFinished || series == null
        androidx.compose.animation.Crossfade(targetState = showSkeleton, animationSpec = androidx.compose.animation.core.tween(800), label = "fade") { loading ->
            if (loading) {
                DetailsSkeleton()
            } else {'''
            
c = re.sub(target_series_cond, replacement_series_cond, c)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

