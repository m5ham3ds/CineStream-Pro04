file_path = "app/src/main/java/com/example/ui/screens/share/ShareScreen.kt"
with open(file_path, "r") as f:
    content = f.read()

content = content.replace('Text(stringResource(R.string.connected_to, connectedEndpoint?.name ?: "")), color = Color(0xFF10b981), fontWeight = FontWeight.Bold)', 'Text(stringResource(R.string.connected_to, connectedEndpoint?.name ?: ""), color = Color(0xFF10b981), fontWeight = FontWeight.Bold)')

with open(file_path, "w") as f:
    f.write(content)
