import re

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "r") as f:
    c = f.read()

target = """            if (uiState.isSearching) {
                Box(modifier = Modifier.fillMaxWidth().height(200.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                }
            } else {"""

replacement = """            if (uiState.isSearching) {
                com.example.ui.components.SearchScreenSkeleton()
            } else {"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/search/SearchScreen.kt", "w") as f:
    f.write(c)
