import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_save = """                                quality = quality,
                                progress = 0.05f,"""

new_save = """                                quality = "$quality||$url",
                                progress = 0.05f,"""

if old_save in content:
    content = content.replace(old_save, new_save)
    with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
        f.write(content)
    print("Replaced PlayerScreen save block")
else:
    print("Could not find old_save")
