with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    c = f.read()

target = """                    onPauseResume = {
                        scope.launch {
                            downloadRepository.updateDownload(item.copy(isPaused = !item.isPaused))
                        }
                    },"""

replace = """                    onPauseResume = {
                        val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                            action = "CANCEL"
                            putExtra("id", item.id)
                        }
                        context.startService(intent)
                        scope.launch {
                            downloadRepository.updateDownload(item.copy(isPaused = true))
                        }
                    },"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(c)

