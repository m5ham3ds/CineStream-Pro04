with open("app/src/main/java/com/example/data/sync/CloudSyncManager.kt", "r") as f:
    content = f.read()

new_sync = """
    suspend fun syncFromCloud(userId: String) {
        val userDoc = firestore.collection("users").document(userId)
        
        try {
            // 1. Push local data to cloud (in case they used the app as guest)
            val localLibrary = kotlinx.coroutines.flow.firstOrNull(db.libraryDao().getAllItems()) ?: emptyList()
            localLibrary.forEach { userDoc.collection("library").document(it.id).set(it) }

            val localHistory = kotlinx.coroutines.flow.firstOrNull(db.historyDao().getAllHistory()) ?: emptyList()
            localHistory.forEach { userDoc.collection("history").document(it.id).set(it) }

            val localEpisodes = kotlinx.coroutines.flow.firstOrNull(db.watchedEpisodeDao().getAllWatched()) ?: emptyList()
            localEpisodes.forEach { userDoc.collection("watched_episodes").document(it.id).set(it) }

            // 2. Pull cloud data to local
            val librarySnapshot = userDoc.collection("library").get().await()
            val libraryItems = librarySnapshot.toObjects(LibraryItem::class.java)
            libraryItems.forEach { db.libraryDao().insertItem(it) }

            val historySnapshot = userDoc.collection("history").get().await()
            val historyItems = historySnapshot.toObjects(HistoryItem::class.java)
            historyItems.forEach { db.historyDao().insertHistory(it) }

            val episodesSnapshot = userDoc.collection("watched_episodes").get().await()
            val episodes = episodesSnapshot.toObjects(WatchedEpisode::class.java)
            episodes.forEach { db.watchedEpisodeDao().insert(it) }
        } catch (e: Exception) {
            e.printStackTrace()
        }
    }
"""
import re
content = re.sub(r'suspend fun syncFromCloud\(userId: String\) \{.*?\}(?=\n\n    suspend fun clearLocalData)', new_sync.strip(), content, flags=re.DOTALL)
content = content.replace('import kotlinx.coroutines.tasks.await', 'import kotlinx.coroutines.tasks.await\nimport kotlinx.coroutines.flow.firstOrNull')

with open("app/src/main/java/com/example/data/sync/CloudSyncManager.kt", "w") as f:
    f.write(content)
