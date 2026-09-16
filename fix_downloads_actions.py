import re
with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    c = f.read()

c = c.replace(
    'onPauseResume = {',
    'onPauseResume = { // TODO '
)

# wait, better to use proper replace for onPauseResume
pause_replace = """
                    onPauseResume = {
                        val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                            action = "CANCEL"
                            putExtra("id", item.id)
                        }
                        context.startService(intent)
                        scope.launch {
                            downloadRepository.updateDownload(item.copy(isPaused = true))
                        }
                    },
"""
c = re.sub(r'onPauseResume = \{.*?\n                    \},', pause_replace.strip() + ',', c, flags=re.DOTALL)

# Delete confirmation
delete_replace = """
            onConfirm = {
                itemToDelete?.let { item ->
                    val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                        action = "CANCEL"
                        putExtra("id", item.id)
                    }
                    context.startService(intent)
                    scope.launch {
                        downloadRepository.deleteDownload(item)
                    }
                }
                itemToDelete = null
            },
"""
c = re.sub(r'onConfirm = \{.*?\n            \},', delete_replace.strip() + ',', c, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(c)

