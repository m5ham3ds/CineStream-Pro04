with open("app/src/main/java/com/example/data/repository/DownloadManagerService.kt", "r") as f:
    content = f.read()

content = content.replace("while (isActive)", "while (kotlinx.coroutines.currentCoroutineContext().isActive)")

with open("app/src/main/java/com/example/data/repository/DownloadManagerService.kt", "w") as f:
    f.write(content)
