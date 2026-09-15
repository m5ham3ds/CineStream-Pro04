import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

content = content.replace("downloadRepository.getAllDownloads()", "downloadRepository.getDownloadItems()")

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
