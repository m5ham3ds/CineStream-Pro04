import re

with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "r") as f:
    c = f.read()

target = """@Composable
fun AboutScreen(onBack: () -> Unit = {}) {
    val scrollState = rememberScrollState()"""
    
replacement = """import androidx.compose.runtime.*

@Composable
fun AboutScreen(onBack: () -> Unit = {}) {
    var transitionFinished by remember { mutableStateOf(false) }
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(400)
        transitionFinished = true
    }

    if (!transitionFinished) {
        com.example.ui.components.AboutScreenSkeleton()
        return
    }

    val scrollState = rememberScrollState()"""
    
c = c.replace(target, replacement)
with open("app/src/main/java/com/example/ui/screens/about/AboutScreen.kt", "w") as f:
    f.write(c)
