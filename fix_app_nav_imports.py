import re

file_path = "app/src/main/java/com/example/navigation/AppNavigation.kt"
with open(file_path, "r") as f:
    content = f.read()

imports = [
    "import androidx.compose.runtime.CompositionLocalProvider",
    "import androidx.compose.ui.platform.LocalLayoutDirection",
    "import androidx.compose.ui.unit.LayoutDirection"
]

for imp in imports:
    if imp not in content:
        content = content.replace("import androidx.compose.runtime.Composable", f"import androidx.compose.runtime.Composable\n{imp}")

with open(file_path, "w") as f:
    f.write(content)
