import re
with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    content = f.read()

simulate_effect = """
    // Simulate download progress
    LaunchedEffect(downloads) {
        val inProgress = downloads.filter { !it.isCompleted && !it.isPaused }
        if (inProgress.isNotEmpty()) {
            kotlinx.coroutines.delay(2000)
            inProgress.forEach { item ->
                val newProgress = item.progress + (0.02f .. 0.05f).random()
                if (newProgress >= 1f) {
                    downloadRepository.updateDownload(item.copy(progress = 1f, isCompleted = true))
                } else {
                    downloadRepository.updateDownload(item.copy(progress = newProgress))
                }
            }
        }
    }
"""

if "Simulate download progress" not in content:
    content = content.replace(
        "    val filteredDownloads = when (selectedTab) {",
        simulate_effect + "\n    val filteredDownloads = when (selectedTab) {"
    )

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(content)
