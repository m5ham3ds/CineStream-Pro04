import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

content = content.replace("Text(modifier = Modifier.padding(horizontal = 16.dp),\n                        stringResource", "Text(modifier = Modifier.padding(horizontal = 16.dp),\n                        text = stringResource")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
