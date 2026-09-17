import re

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "r") as f:
    c = f.read()

target = """    val searchResults = uiState.movieResults.map { UnifiedMediaResult(it.id, it.title, it.posterUrl, true) } +
                        uiState.seriesResults.map { UnifiedMediaResult(it.id, it.title, it.posterUrl, false) }
"""

replacement = target + """
    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(300)
        transitionFinished = true
    }
    
    if (!transitionFinished) {
        com.example.ui.components.SearchScreenSkeleton()
        return
    }
"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "w") as f:
    f.write(c)
