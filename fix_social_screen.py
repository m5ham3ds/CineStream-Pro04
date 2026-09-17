import re

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "r") as f:
    c = f.read()

target = """    val currentUser by viewModel.currentUser.collectAsState()
    val conversations by viewModel.conversations.collectAsState()
    val stories by viewModel.stories.collectAsState()
    val searchResults by viewModel.searchResults.collectAsState()
"""

replacement = target + """    val isLoading by viewModel.isLoading.collectAsState()

    if (isLoading) {
        com.example.ui.components.SocialScreenSkeleton()
        return
    }
"""

c = c.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/social/SocialScreen.kt", "w") as f:
    f.write(c)
