with open("app/src/main/java/com/example/MainActivity.kt", "r") as f:
    content = f.read()

if "DownloadManagerService.init" not in content:
    content = content.replace(
        "val downloadRepo = remember { com.example.data.repository.DownloadRepository(this@MainActivity) }",
        "val downloadRepo = remember { com.example.data.repository.DownloadRepository(this@MainActivity) }\n        com.example.data.repository.DownloadManagerService.init(this@MainActivity.applicationContext)"
    )

with open("app/src/main/java/com/example/MainActivity.kt", "w") as f:
    f.write(content)
