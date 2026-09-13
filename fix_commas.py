import re
path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# Replace any occurrence of MaterialTheme.colorScheme.onBackground followed by space(s) and a word character (a-zA-Z)
content = re.sub(r'MaterialTheme\.colorScheme\.onBackground\s+([a-zA-Z])', r'MaterialTheme.colorScheme.onBackground, \1', content)

# Also fix `canvasColor`
content = re.sub(r'canvasColor\s+([a-zA-Z])', r'canvasColor, \1', content)

with open(path, 'w') as f:
    f.write(content)
