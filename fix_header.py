import re

file_path = "app/src/main/java/com/example/ui/components/CineStreamHeader.kt"
with open(file_path, "r") as f:
    content = f.read()

# We need to extract MaterialTheme.colorScheme calls out of drawBehind and other non-composable scopes.
# We'll declare them at the top of CineStreamHeader.

replacements = {
    'drawRect(MaterialTheme.colorScheme.background)': 'drawRect(bgColor)',
    'colors = listOf(MaterialTheme.colorScheme.primary.copy(alpha = 0.3f), Color.Transparent)': 'colors = listOf(primary30, Color.Transparent)',
    'colors = listOf(Color.Transparent, MaterialTheme.colorScheme.primary.copy(alpha = 0.3f))': 'colors = listOf(Color.Transparent, primary30)',
    'color = MaterialTheme.colorScheme.surface,': 'color = surfaceColor,',
    'color = MaterialTheme.colorScheme.primary,': 'color = primaryColor,',
}

# we need to inject the color variables right after `val iconBorder = MaterialTheme.colorScheme.surfaceVariant`
injection = """
    val primaryColor = MaterialTheme.colorScheme.primary
    val primary30 = MaterialTheme.colorScheme.primary.copy(alpha = 0.3f)
    val bgColor = MaterialTheme.colorScheme.background
    val surfaceColor = MaterialTheme.colorScheme.surface
"""

if 'val iconBorder = MaterialTheme.colorScheme.surfaceVariant' in content:
    content = content.replace('val iconBorder = MaterialTheme.colorScheme.surfaceVariant', 'val iconBorder = MaterialTheme.colorScheme.surfaceVariant' + injection)

for old, new in replacements.items():
    content = content.replace(old, new)

with open(file_path, "w") as f:
    f.write(content)

