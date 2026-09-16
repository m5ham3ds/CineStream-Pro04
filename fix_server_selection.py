import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

target = """                                                .clickable {
                                                    onPlay(quality.url, selectedServerForQuality ?: "", currentSiteName)
                                                }"""
replace = """                                                .clickable {
                                                    onPlay(quality.url, if (isDownloadMode) quality.name else (selectedServerForQuality ?: ""), currentSiteName)
                                                }"""

c = c.replace(target, replace)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

