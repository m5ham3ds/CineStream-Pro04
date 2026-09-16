import re
with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    c = f.read()

c = c.replace("Icons.Default.CheckCircle else Icons.Default.CheckCircle", "Icons.Default.Check else Icons.Default.Close")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(c)
