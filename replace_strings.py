import os

files_to_update = {
    'app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt': [
        ('Text("Connecting to ${uiState.currentWebsite}$serverText...", color = MaterialTheme.colorScheme.onBackground)',
         'Text(stringResource(R.string.connecting_to, "${uiState.currentWebsite}$serverText"), color = MaterialTheme.colorScheme.onBackground)'),
        ('Text("Loading ${uiState.currentWebsite}$serverText...", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)',
         'Text(stringResource(R.string.loading_site, "${uiState.currentWebsite}$serverText"), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)'),
        ('Text("Current Site: ${uiState.currentWebsite}", color = MaterialTheme.colorScheme.onSurfaceVariant',
         'Text(stringResource(R.string.current_site, uiState.currentWebsite), color = MaterialTheme.colorScheme.onSurfaceVariant')
    ],
    'app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt': [
        ('Text("$usedStr / $totalStr used", color = MaterialTheme.colorScheme.onSurfaceVariant',
         'Text(stringResource(R.string.used_space, usedStr, totalStr), color = MaterialTheme.colorScheme.onSurfaceVariant'),
        ('Text("$usedPercentageInt% used", color = MaterialTheme.colorScheme.onSurfaceVariant',
         'Text(stringResource(R.string.used_percentage, usedPercentageInt), color = MaterialTheme.colorScheme.onSurfaceVariant'),
        ('Text("$availableStr free", color = MaterialTheme.colorScheme.onSurfaceVariant',
         'Text(stringResource(R.string.free_space, availableStr), color = MaterialTheme.colorScheme.onSurfaceVariant')
    ],
    'app/src/main/java/com/example/ui/screens/share/ShareScreen.kt': [
        ('Text("${groupedSeries[folderName]?.size ?: 0} Episodes", color = MaterialTheme.colorScheme.onSurfaceVariant',
         'Text(stringResource(R.string.episodes_count, groupedSeries[folderName]?.size ?: 0), color = MaterialTheme.colorScheme.onSurfaceVariant'),
        ('Text("Connected to ${connectedEndpoint!!.name}", fontWeight = FontWeight.Bold)',
         'Text(stringResource(R.string.connected_to, connectedEndpoint!!.name), fontWeight = FontWeight.Bold)'),
    ]
}

for path, replacements in files_to_update.items():
    if os.path.exists(path):
        with open(path, 'r') as f:
            content = f.read()
            
        for old, new in replacements:
            content = content.replace(old, new)
            
        with open(path, 'w') as f:
            f.write(content)

