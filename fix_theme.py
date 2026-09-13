import re
with open("app/src/main/java/com/example/ui/theme/Color.kt", "r") as f:
    content = f.read()

content = content.replace('Color(0xFFF5F5F5)', 'Color(0xFFF7F7F7)')
content = content.replace('Color(0xFFFFFFFF)', 'Color(0xFFFCFCFC)')

with open("app/src/main/java/com/example/ui/theme/Color.kt", "w") as f:
    f.write(content)

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "r") as f:
    theme_content = f.read()

theme_content = theme_content.replace('surfaceVariant = Color(0xFFEEEEEE),', 'surfaceVariant = Color(0xFFE5E5E5),')
theme_content = theme_content.replace('onSurfaceVariant = TextSecondary', 'onSurfaceVariant = Color(0xFF666666)')
theme_content = theme_content.replace('onBackground = TextPrimaryLight,', 'onBackground = Color(0xFF1E1E1E),')
theme_content = theme_content.replace('onSurface = TextPrimaryLight,', 'onSurface = Color(0xFF1E1E1E),')

with open("app/src/main/java/com/example/ui/theme/Theme.kt", "w") as f:
    f.write(theme_content)
