path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# I want to change all 'color = onBackgroundColor' to 'color = MaterialTheme.colorScheme.onBackground'
# EXCEPT the ones inside `VerticalSlider`
# But actually `VerticalSlider` is a small function.
# I will just replace ALL of them.
content = content.replace('onBackgroundColor', 'MaterialTheme.colorScheme.onBackground')
content = content.replace('val MaterialTheme.colorScheme.onBackground = MaterialTheme.colorScheme.onBackground', 'val onBackgroundColor = MaterialTheme.colorScheme.onBackground')
content = content.replace('color = MaterialTheme.colorScheme.onBackground\n', 'color = onBackgroundColor\n') 

with open(path, 'w') as f:
    f.write(content)

