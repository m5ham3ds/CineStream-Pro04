import re

def apply_deferral(file_path):
    with open(file_path, "r") as f:
        c = f.read()

    # Apply to MovieDetailsScreen
    target1 = """    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        if (uiState.isLoading) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {"""
        
    replacement1 = """    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(400) // matches slide transition
        transitionFinished = true
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        if (uiState.isLoading || !transitionFinished) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {"""

    # Apply to SeriesDetailsScreen
    target2 = """    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if (uiState.isLoading && series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }"""
        
    replacement2 = """    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(400) // matches slide transition
        transitionFinished = true
    }

    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if ((uiState.isLoading || !transitionFinished) && series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }"""

    if target1 in c:
        c = c.replace(target1, replacement1)
    if target2 in c:
        c = c.replace(target2, replacement2)
        
    with open(file_path, "w") as f:
        f.write(c)

apply_deferral("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt")

