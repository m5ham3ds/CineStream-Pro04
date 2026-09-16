import re
with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    c = f.read()

c = c.replace("androidx.compose.material.icons.Icons.Default.CheckCircle", "androidx.compose.material.icons.Icons.Filled.CheckCircle")
c = c.replace("androidx.compose.material.icons.Icons.Outlined.CheckCircle", "androidx.compose.material.icons.Icons.Outlined.CheckCircle")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(c)
