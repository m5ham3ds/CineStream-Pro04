import re

with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "r") as f:
    c = f.read()

target = """@Composable
fun LibraryScreen(
    onItemClick: (String, Boolean) -> Unit
) {
    val context = LocalContext.current"""

replacement = """@Composable
fun LibraryScreen(
    onItemClick: (String, Boolean) -> Unit
) {
    var isLoading by remember { mutableStateOf(true) }
    LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(600)
        isLoading = false
    }
    if (isLoading) {
        com.example.ui.components.LibraryScreenSkeleton()
        return
    }

    val context = LocalContext.current"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/library/LibraryScreen.kt", "w") as f:
    f.write(c)

