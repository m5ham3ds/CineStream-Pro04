import re
with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    c = f.read()

# Fix @Composable duplication
c = re.sub(r'(@Composable\s*){2,}fun DownloadSettingsDialog', r'@Composable\nfun DownloadSettingsDialog', c)

# Fix Icons
c = c.replace("Icons.Outlined.RadioButtonUnchecked", "Icons.Default.RadioButtonUnchecked")
c = c.replace("Icons.Outlined.RadioButtonChecked", "Icons.Default.RadioButtonChecked")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(c)
