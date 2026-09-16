import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    c = f.read()

# For MovieDetailsScreen
target_movie = """        if (uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) { CircularProgressIndicator() }
        } else if (uiState.movie != null) {"""
replace_movie = """        if (uiState.isLoading) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {"""
c = c.replace(target_movie, replace_movie)

# For SeriesDetailsScreen
target_series = """    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }

        if (series != null) {"""
replace_series = """    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if (uiState.isLoading && series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }

        if (series != null) {"""
c = c.replace(target_series, replace_series)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(c)
