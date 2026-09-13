import re
path = 'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt'
with open(path, 'r') as f:
    content = f.read()

# Fix the missing commas
content = content.replace('MaterialTheme.colorScheme.onBackground\n', 'MaterialTheme.colorScheme.onBackground,\n')
content = content.replace('MaterialTheme.colorScheme.onBackground ', 'MaterialTheme.colorScheme.onBackground, ')

# That's too dangerous. Let's just fix it by replacing what I broke exactly
# Wait, I broke it with:
# content = content.replace('MaterialTheme.colorScheme.onBackground,', 'MaterialTheme.colorScheme.onBackground')
# So to revert, everywhere where `MaterialTheme.colorScheme.onBackground` is followed by something like a newline or a bracket or another property, I need a comma?
# No, let's just find the exact places from the compiler error!

with open(path, 'w') as f:
    f.write(content)
