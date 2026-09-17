import re

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "r") as f:
    c = f.read()

target = "@Database(entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class, WatchedEpisode::class, NotificationItem::class], version = 5, exportSchema = false)"
replacement = "import com.example.data.model.SupportMessage\n\n@Database(entities = [LibraryItem::class, DownloadItem::class, HistoryItem::class, WatchedEpisode::class, NotificationItem::class, SupportMessage::class], version = 6, exportSchema = false)"

c = c.replace(target, replacement)

target2 = "abstract fun notificationDao(): NotificationDao"
replacement2 = "abstract fun notificationDao(): NotificationDao\n    abstract fun supportDao(): SupportDao"

c = c.replace(target2, replacement2)

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "w") as f:
    f.write(c)

