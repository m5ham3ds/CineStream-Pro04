import re
with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

c = c.replace(
    "extractedDownloadLinks = downloadsMap\n",
    "extractedDownloadLinks = downloadsMap\n                                                                extractedServerIds = serversIds\n"
)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)
