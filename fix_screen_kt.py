import re

with open("app/src/main/java/com/example/navigation/Screen.kt", "r") as f:
    c = f.read()

target = "    object About : Screen(\"about\", \"About Us\", Icons.Default.Info)"
replacement = "    object About : Screen(\"about\", \"About Us\", Icons.Default.Info)\n    object Notifications : Screen(\"notifications\", \"Notifications\", Icons.Default.Notifications)"

c = c.replace(target, replacement)
# missing import for Notifications icon
c = c.replace("import androidx.compose.material.icons.filled.Info", "import androidx.compose.material.icons.filled.Info\nimport androidx.compose.material.icons.filled.Notifications")

with open("app/src/main/java/com/example/navigation/Screen.kt", "w") as f:
    f.write(c)
