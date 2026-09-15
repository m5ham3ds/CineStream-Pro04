import re
with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

old_content = """        Surface(modifier = Modifier.fillMaxSize()) {
          AppNavigation()
        }"""
new_content = """        val downloadRepo = remember { com.example.data.repository.DownloadRepository(this@MainActivity) }
        val downloads by downloadRepo.getDownloadItems().collectAsState(initial = emptyList())
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
        }
        
        Surface(modifier = Modifier.fillMaxSize()) {
          AppNavigation()
        }"""
content = content.replace(old_content, new_content)

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
