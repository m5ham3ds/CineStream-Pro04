import re
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

# Remove the LaunchedEffect from MainActivity
old_mock = """        val downloads by downloadRepo.getDownloadItems().collectAsState(initial = emptyList())
        LaunchedEffect(downloads) {
            val inProgress = downloads.filter { !it.isCompleted && !it.isPaused }
            if (inProgress.isNotEmpty()) {
                kotlinx.coroutines.delay(2000)
                inProgress.forEach { item ->
                    val newProgress = item.progress + 0.03f
                    if (newProgress >= 1f) {
                        downloadRepo.updateDownload(item.copy(progress = 1f, isCompleted = true))
                    } else {
                        downloadRepo.updateDownload(item.copy(progress = newProgress))
                    }
                }
            }
        }"""
new_mock = """        // Real downloads are handled in DownloadRepository now"""
content = content.replace(old_mock, new_mock)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
