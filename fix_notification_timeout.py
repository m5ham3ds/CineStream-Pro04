import re
with open("app/src/main/java/com/example/utils/NotificationHelper.kt", "r") as f:
    content = f.read()

old_complete = """            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)"""
new_complete = """            .setPriority(NotificationCompat.PRIORITY_DEFAULT)
            .setAutoCancel(true)
            .setTimeoutAfter(3000)"""

content = content.replace(old_complete, new_complete)

with open("app/src/main/java/com/example/utils/NotificationHelper.kt", "w") as f:
    f.write(content)
