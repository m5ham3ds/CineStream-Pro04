import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    content = f.read()

# Remove the broken one
content = content.replace("onNavigateToExtensions: () -> Unit = {\n    val context = androidx.compose.ui.platform.LocalContext.current}", "onNavigateToExtensions: () -> Unit = {}")

# Add the correct one
content = content.replace(") {\n    val coroutineScope", ") {\n    val context = androidx.compose.ui.platform.LocalContext.current\n    val coroutineScope")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(content)
