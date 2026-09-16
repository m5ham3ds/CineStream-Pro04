with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

import re

target = re.search(r"if \(showDownloadSettingsDialog\) \{.*?\},[\s]*containerColor = MaterialTheme\.colorScheme\.surface,[\s]*titleContentColor = MaterialTheme\.colorScheme\.onSurface,[\s]*textContentColor = MaterialTheme\.colorScheme\.onSurfaceVariant[\s]*\)", content, re.DOTALL)

replacement = """if (showDownloadSettingsDialog) {
        DownloadSettingsDialog(
            maxConcurrentDownloads = maxConcurrentDownloads,
            maxSegments = maxSegments,
            downloadNetwork = downloadNetwork,
            onMaxConcurrentChanged = { coroutineScope.launch { userPrefs.saveMaxConcurrentDownloads(it) } },
            onMaxSegmentsChanged = { coroutineScope.launch { userPrefs.saveMaxSegments(it) } },
            onNetworkChanged = { coroutineScope.launch { userPrefs.saveDownloadNetwork(it) } },
            onDismiss = { showDownloadSettingsDialog = false }
        )
    }"""

if target:
    content = content.replace(target.group(0), replacement)
    with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
        f.write(content)
    print("Replaced download settings block")
else:
    print("Could not find download settings block")
