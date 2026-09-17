import re

with open("app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt", "r") as f:
    c = f.read()

target = """@Composable
fun ExtensionsScreen(onBackClick: () -> Unit) {
    val installedExtensions by ExtensionManager.installedExtensions.collectAsState()"""

replacement = """@Composable
fun ExtensionsScreen(onBackClick: () -> Unit) {
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(800)
        isLoading = false
    }
    
    if (isLoading) {
        com.example.ui.components.ExtensionsScreenSkeleton()
        return
    }

    val installedExtensions by ExtensionManager.installedExtensions.collectAsState()"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt", "w") as f:
    f.write(c)

