import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    c = f.read()

target = """    var searchQuery by remember { mutableStateOf("") }

    if (currentUser == null) {"""

replacement = """    var searchQuery by remember { mutableStateOf("") }
    val isLoading by viewModel.isLoading.collectAsState()
    
    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(400)
        transitionFinished = true
    }

    if (isLoading || !transitionFinished) {
        com.example.ui.components.SocialScreenSkeleton()
        return
    }

    if (currentUser == null) {"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(c)

