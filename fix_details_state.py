import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# Fix MovieDetailsScreen transition
c = c.replace("kotlinx.coroutines.delay(400) // matches slide transition", "kotlinx.coroutines.delay(1200) // matches slide transition and ensures full skeleton cycle")

# In MovieDetailsScreen
target_movie_skeleton = """        if (uiState.isLoading || !transitionFinished) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {"""
replacement_movie_skeleton = """        if (uiState.isLoading || !transitionFinished || uiState.movie == null) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {"""
c = c.replace(target_movie_skeleton, replacement_movie_skeleton)


# In SeriesDetailsScreen
target_series_skeleton = """        if ((uiState.isLoading || !transitionFinished) && series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }
        
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }"""
replacement_series_skeleton = """        if (uiState.isLoading || !transitionFinished || series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }"""
c = c.replace(target_series_skeleton, replacement_series_skeleton)


with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)

