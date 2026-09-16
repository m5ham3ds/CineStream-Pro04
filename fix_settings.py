import re
with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    c = f.read()

# Fix @Composable duplication
c = c.replace("@Composable\n@Composable\nfun DownloadSettingsDialog", "@Composable\nfun DownloadSettingsDialog")

# Revert to material3 slider
c = c.replace("import androidx.compose.material.Slider\n", "")
c = c.replace("import androidx.compose.material.SliderDefaults\n", "")
c = c.replace("androidx.compose.material.Slider", "androidx.compose.material3.Slider")
c = c.replace("androidx.compose.material.SliderDefaults", "androidx.compose.material3.SliderDefaults")
c = c.replace("activeTickColor = Color.Transparent,", "")
c = c.replace("inactiveTickColor = Color.Transparent", "")
c = c.replace("Icons.Default.RadioButtonUnchecked", "Icons.Outlined.RadioButtonUnchecked")
c = c.replace("Icons.Default.RadioButtonChecked", "Icons.Outlined.RadioButtonChecked")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(c)
