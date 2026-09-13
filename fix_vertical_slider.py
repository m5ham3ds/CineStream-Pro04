path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

content = content.replace('val onBackgroundColor = MaterialTheme.colorScheme.onBackground\n        Canvas', 'val onBackgroundColor = MaterialTheme.colorScheme.onBackground\n        androidx.compose.foundation.Canvas')

# Revert my poor previous replace logic
content = content.replace('color = onBackgroundColor\n', 'color = onBackgroundColor,')
content = content.replace('color = MaterialTheme.colorScheme.onBackground,', 'color = onBackgroundColor,')

with open(path, 'w') as f:
    f.write(content)

