import re

with open("app/src/main/java/com/example/MyApplication.kt", "r") as f:
    c = f.read()

c = c.replace("maxSizeBytes(500L * 1024 * 1024)", "maxSizeBytes(450L * 1024 * 1024) // 450 MB")

with open("app/src/main/java/com/example/MyApplication.kt", "w") as f:
    f.write(c)

