import re

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "r") as f:
    c = f.read()

target = "@Database(entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class, WatchedEpisode::class], version = 4, exportSchema = false)"
replacement = "import com.example.data.model.NotificationItem\n\n@Database(entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class, WatchedEpisode::class, NotificationItem::class], version = 5, exportSchema = false)"

c = c.replace(target, replacement)

target2 = "abstract class AppDatabase : RoomDatabase() {"
replacement2 = "abstract class AppDatabase : RoomDatabase() {\n    abstract fun notificationDao(): NotificationDao"

c = c.replace(target2, replacement2)

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "w") as f:
    f.write(c)
