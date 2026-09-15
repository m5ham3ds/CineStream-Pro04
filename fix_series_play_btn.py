import re
with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    content = f.read()

# I will just write a python script to replace the `.mp4` mistake in MovieDetailsScreen
content = content.replace('"local_offline_file://${downloadItem.id}.mp4"', '"local_offline_file://${downloadItem.id}"')

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(content)
