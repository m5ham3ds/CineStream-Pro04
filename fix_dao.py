with open("app/src/main/java/com/example/data/db/DownloadDao.kt", "r") as f:
    content = f.read()

if "getAllItemsSync" not in content:
    content = content.replace("fun getAllItems(): Flow<List<DownloadItem>>", "fun getAllItems(): Flow<List<DownloadItem>>\n\n    @Query(\"SELECT * FROM download_items\")\n    suspend fun getAllItemsSync(): List<DownloadItem>")

with open("app/src/main/java/com/example/data/db/DownloadDao.kt", "w") as f:
    f.write(content)
