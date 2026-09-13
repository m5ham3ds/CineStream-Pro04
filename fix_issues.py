import os
import re

# Fix Color.kt
color_kt_path = "app/src/main/java/com/example/ui/theme/Color.kt"
with open(color_kt_path, "r") as f:
    color_kt = f.read()

color_kt = color_kt.replace('Color(0xFFF7F7F7)', 'Color(0xFFE5E5E5)')
color_kt = color_kt.replace('Color(0xFFFCFCFC)', 'Color(0xFFF0F0F0)')
color_kt = color_kt.replace('Color(0xFF121212)', 'Color(0xFF222222)')

with open(color_kt_path, "w") as f:
    f.write(color_kt)

# Fix CineStreamHeader.kt
header_path = "app/src/main/java/com/example/ui/components/CineStreamHeader.kt"
with open(header_path, "r") as f:
    header = f.read()

# Replace hardcoded colors with theme colors
header = header.replace('val bgDark = Color(0xFF141416)', 'val bgDark = MaterialTheme.colorScheme.background')
header = header.replace('val iconBorder = Color(0xFF2C2C30)', 'val iconBorder = MaterialTheme.colorScheme.surfaceVariant')
header = header.replace('Color(0xFF0C0C0E)', 'MaterialTheme.colorScheme.background')
header = header.replace('Color(0xFF3A050A)', 'MaterialTheme.colorScheme.primary.copy(alpha = 0.3f)')
header = header.replace('Color(0xFF222225)', 'MaterialTheme.colorScheme.surface')
header = header.replace('Color(0xFFFF1A1A)', 'MaterialTheme.colorScheme.primary')
header = header.replace('Color(0xFF1E1E24)', 'MaterialTheme.colorScheme.surface')
header = header.replace('Color(0xFFFF2A2A)', 'MaterialTheme.colorScheme.primary')
header = header.replace('Color(0xFFE0E0E0)', 'MaterialTheme.colorScheme.onBackground')
header = header.replace('Color(0xFFAAAAAA)', 'MaterialTheme.colorScheme.onSurfaceVariant')
header = header.replace('Color(0xFFFF3030)', 'MaterialTheme.colorScheme.primary')
header = header.replace('Color(0xFFFF2020)', 'MaterialTheme.colorScheme.primary')

with open(header_path, "w") as f:
    f.write(header)

# Fix ShareScreen.kt
share_path = "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
with open(share_path, "r") as f:
    share = f.read()

share = share.replace('Color.Red', 'MaterialTheme.colorScheme.primary')
share = share.replace('Color.Green', 'Color(0xFF10b981)')
share = share.replace('Color(0xFF3b82f6)', 'Color(0xFF3b82f6)') # Keep blue
share = share.replace('Text(if (isSent) "Sent" else "Received"', 'Text(if (isSent) stringResource(R.string.sent) else stringResource(R.string.received)')
share = share.replace('Text("Connected to ${connectedEndpoint?.name}"', 'Text(stringResource(R.string.connected_to, connectedEndpoint?.name ?: ""))')

with open(share_path, "w") as f:
    f.write(share)

# Fix ExtensionsScreen.kt
ext_path = "app/src/main/java/com/example/ui/screens/extensions/ExtensionsScreen.kt"
with open(ext_path, "r") as f:
    ext = f.read()

ext = ext.replace('Color.Red', 'MaterialTheme.colorScheme.primary')

with open(ext_path, "w") as f:
    f.write(ext)
