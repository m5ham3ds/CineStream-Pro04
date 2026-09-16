with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

imports_to_add = """
import androidx.compose.material.icons.filled.Close
import androidx.compose.material.icons.filled.Layers
import androidx.compose.material.icons.filled.Movie
import androidx.compose.material.icons.filled.Wifi
import androidx.compose.material.icons.filled.RadioButtonChecked
import androidx.compose.material.icons.filled.SignalCellular4Bar
import androidx.compose.material.icons.outlined.FileDownload
"""

content = content.replace("import androidx.compose.material.icons.Icons", imports_to_add + "\nimport androidx.compose.material.icons.Icons")

content = content.replace("androidx.compose.material.icons.Icons.Outlined.FileDownload", "Icons.Outlined.FileDownload")
content = content.replace("androidx.compose.material.icons.Icons.Default.Close", "Icons.Default.Close")
content = content.replace("androidx.compose.material.icons.Icons.Default.Layers", "Icons.Default.Layers")
content = content.replace("androidx.compose.material.icons.Icons.Default.Movie", "Icons.Default.Movie")
content = content.replace("androidx.compose.material.icons.Icons.Default.Wifi", "Icons.Default.Wifi")
content = content.replace("androidx.compose.material.icons.Icons.Default.RadioButtonChecked", "Icons.Default.RadioButtonChecked")
content = content.replace("androidx.compose.material.icons.Icons.Default.SignalCellular4Bar", "Icons.Default.SignalCellular4Bar")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(content)
