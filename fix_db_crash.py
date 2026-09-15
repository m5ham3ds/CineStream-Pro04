import re
with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "r") as f:
    content = f.read()

content = content.replace("version = 3", "version = 4")

with open("app/src/main/java/com/example/data/db/AppDatabase.kt", "w") as f:
    f.write(content)
