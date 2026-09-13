import re
path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# I will just replace all `MaterialTheme.colorScheme.onBackground` inside the Canvas block.
# Let's find "val canvasColor = MaterialTheme.colorScheme.onBackground" to the end of the file,
# and in that part, replace MaterialTheme.colorScheme.onBackground with canvasColor.

parts = content.split('val canvasColor = MaterialTheme.colorScheme.onBackground')
if len(parts) == 2:
    new_bottom = parts[1].replace('MaterialTheme.colorScheme.onBackground', 'canvasColor', 3)
    content = parts[0] + 'val canvasColor = MaterialTheme.colorScheme.onBackground' + new_bottom

with open(path, 'w') as f:
    f.write(content)
