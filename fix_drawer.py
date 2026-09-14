import re

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "r") as f:
    text = f.read()

text = text.replace("    val currentAppLayoutDirection = LocalLayoutDirection.current\n    CompositionLocalProvider(LocalLayoutDirection provides androidx.compose.ui.unit.LayoutDirection.Ltr) {\n", "")
text = text.replace("        CompositionLocalProvider(LocalLayoutDirection provides currentAppLayoutDirection) {\n", "")

text = text.rstrip()
if text.endswith("}"): text = text[:-1].rstrip()
if text.endswith("}"): text = text[:-1].rstrip()

with open("app/src/main/java/com/example/navigation/AppNavigation.kt", "w") as f:
    f.write(text + "\n")
