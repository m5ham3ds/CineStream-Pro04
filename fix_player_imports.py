with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

if "import androidx.compose.material.icons.filled.Check" not in c:
    c = c.replace("import androidx.compose.material.icons.filled.Warning", "import androidx.compose.material.icons.filled.Warning\nimport androidx.compose.material.icons.filled.Check")
    if "import androidx.compose.material.icons.filled.Check" not in c:
        c = c.replace("import androidx.compose.material.icons.filled.PlayArrow", "import androidx.compose.material.icons.filled.PlayArrow\nimport androidx.compose.material.icons.filled.Check")

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)

