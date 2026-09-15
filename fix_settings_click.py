with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

target = "SettingsListItem(Icons.Outlined.Download, stringResource(R.string.downloads_settings), stringResource(R.string.downloads_desc), false) {}"
replacement = "SettingsListItem(Icons.Outlined.Download, stringResource(R.string.downloads_settings), stringResource(R.string.downloads_desc), false) { showDownloadSettingsDialog = true }"

content = content.replace(target, replacement)

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(content)
