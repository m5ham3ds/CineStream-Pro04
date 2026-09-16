with open("app/src/main/java/com/example/data/db/DownloadDao.kt", "r") as f:
    c = f.read()

target1 = """    @Query("SELECT * FROM download_items WHERE id = :itemId LIMIT 1")
    suspend fun getItemById(itemId: String): DownloadItem?"""

replace1 = """    @Query("SELECT * FROM download_items WHERE id = :itemId LIMIT 1")
    fun getItemByIdFlow(itemId: String): Flow<DownloadItem?>

    @Query("SELECT * FROM download_items WHERE id = :itemId LIMIT 1")
    suspend fun getItemById(itemId: String): DownloadItem?"""
c = c.replace(target1, replace1)

with open("app/src/main/java/com/example/data/db/DownloadDao.kt", "w") as f:
    f.write(c)

with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "r") as f:
    c2 = f.read()

target2 = """    suspend fun getItemByIdSync(id: String): DownloadItem? {
        return downloadDao.getItemById(id)
    }"""
    
replace2 = """    fun getDownloadItemById(id: String): Flow<DownloadItem?> {
        return downloadDao.getItemByIdFlow(id)
    }

    suspend fun getItemByIdSync(id: String): DownloadItem? {
        return downloadDao.getItemById(id)
    }"""

c2 = c2.replace(target2, replace2)

with open("app/src/main/java/com/example/data/repository/DownloadRepository.kt", "w") as f:
    f.write(c2)
