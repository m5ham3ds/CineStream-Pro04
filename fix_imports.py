with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    lines = f.readlines()

new_lines = []
for line in lines:
    if line.startswith("import androidx.compose.material.Slider"):
        continue
    new_lines.append(line)

# Add imports at the top (after package declaration)
final_lines = []
for line in new_lines:
    final_lines.append(line)
    if line.startswith("package "):
        final_lines.append("import androidx.compose.material.Slider\n")
        final_lines.append("import androidx.compose.material.SliderDefaults\n")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.writelines(final_lines)
