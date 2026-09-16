import re
with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    c = f.read()

c = c.replace("androidx.compose.material.icons.Icons.Filled.CheckCircle", "Icons.Default.CheckCircle")
c = c.replace("androidx.compose.material.icons.Icons.Outlined.CheckCircle", "Icons.Outlined.CheckCircle")
c = c.replace("Icons.Outlined.CheckCircle", "Icons.Default.CheckCircle") # Fallback to default to avoid Outlined missing

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(c)
