import re

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'r') as f:
    text = f.read()

# Fix the height
text = text.replace('Modifier.fillMaxWidth().height(450.dp).clip', 'Modifier.fillMaxWidth().wrapContentHeight().clip')
text = text.replace('modifier = Modifier.fillMaxSize().background(Color(0xFF16161A))', 'modifier = Modifier.fillMaxWidth().wrapContentHeight().background(Color(0xFF16161A))')

# Fix the site name colors.
# There are two occurrences:
# withStyle(style = androidx.compose.ui.text.SpanStyle(color = Color(0xFF00C853))) { append(currentSiteName) }
# We want to change the color only for these specific ones, so let's match currentSiteName.
text = re.sub(r'color\s*=\s*Color\(0xFF00C853\)\)\)\s*\{\s*append\(currentSiteName\)\s*\}', r'color = Color(0xFFE50914))) { append(currentSiteName) }', text)

with open('app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt', 'w') as f:
    f.write(text)
