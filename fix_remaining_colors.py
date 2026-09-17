import re

def fix_file(filepath, replacements):
    with open(filepath, "r") as f:
        c = f.read()
    for old, new in replacements:
        c = c.replace(old, new)
    with open(filepath, "w") as f:
        f.write(c)

fix_file("app/src/main/java/com/example/ui/screens/social/ChatScreen.kt", [
    ('Color(0xFF4CAF50)', 'MaterialTheme.colorScheme.tertiary')
])

fix_file("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", [
    ('Color(0xFF555555)', 'MaterialTheme.colorScheme.outline')
])

fix_file("app/src/main/java/com/example/ui/screens/share/ShareScreen.kt", [
    ('Color(0xFF3b82f6)', 'MaterialTheme.colorScheme.secondary')
])

