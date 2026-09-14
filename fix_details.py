import re

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "r") as f:
    text = f.read()

# For MovieDetailsScreen
# 1. Add showNotReleasedDialog state
text = text.replace(
    'var showDeleteConfirm by remember { mutableStateOf(false) }',
    'var showDeleteConfirm by remember { mutableStateOf(false) }\n    var showNotReleasedDialog by remember { mutableStateOf(false) }'
)

# 2. Add dialog UI in MovieDetailsScreen
dialog_code = """
    if (showNotReleasedDialog) {
        AlertDialog(
            onDismissRequest = { showNotReleasedDialog = false },
            title = { Text(stringResource(R.string.coming_soon), color = MaterialTheme.colorScheme.onBackground) },
            text = { Text("هذا العمل لم يُعرض بعد، ولكنه سيعرض قريباً.", color = MaterialTheme.colorScheme.onSurfaceVariant) },
            confirmButton = {
                TextButton(onClick = { showNotReleasedDialog = false }) { Text("حسناً") }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    }
"""
text = text.replace('// Hero Image or Video Player', dialog_code + '\n    // Hero Image or Video Player')

# 3. Change Play button logic in MovieDetailsScreen
# We want to check: val isReleased = (movie.releaseDate ?: "") <= java.time.LocalDate.now().toString()
# If not released, show dialog, else normal flow.
movie_play_logic = """
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null)
                            } else {
                                val isReleased = (movie.releaseDate ?: "") <= java.time.LocalDate.now().toString()
                                if (!isReleased) {
                                    showNotReleasedDialog = true
                                } else {
                                    isDownloadMode = false
                                    if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                        showNoExtensionsDialog = true
                                    } else {
                                        showSourceSheet = true
                                    }
                                }
                            }
"""
# Replace the existing onClick content for Movie
text = re.sub(
r'if \(downloadItem\?\.isCompleted == true\) \{\s*onPlay\(movie\.title, "local_offline_file://\$\{downloadItem\.id\}", null, null\)\s*\} else \{\s*isDownloadMode = false\s*if \(ExtensionManager\.installedExtensions\.value\.isEmpty\(\)\) \{\s*showNoExtensionsDialog = true\s*\} else \{\s*showSourceSheet = true\s*\}\s*\}',
movie_play_logic.strip(), text, count=1, flags=re.MULTILINE
)


# For SeriesDetailsScreen
# 1. Add showNotReleasedDialog state
text = text.replace(
    'var showBatchDownloadSheet by remember { mutableStateOf(false) }',
    'var showBatchDownloadSheet by remember { mutableStateOf(false) }\n    var showNotReleasedDialog by remember { mutableStateOf(false) }'
)

# 2. Add dialog UI in SeriesDetailsScreen
# Find where to put it: maybe before `Box(modifier = Modifier.fillMaxSize())`
text = text.replace('val firstUnplayedEpisode = episodes.firstOrNull { it.id !in progress } ?: episodes.firstOrNull()', 'val firstUnplayedEpisode = episodes.firstOrNull { it.id !in progress } ?: episodes.firstOrNull()\n' + dialog_code)

# 3. Change Play button logic in SeriesDetailsScreen
# We check: val isReleased = (series.firstAirDate ?: "") <= java.time.LocalDate.now().toString()
series_play_logic = """
                            val isReleased = (series.firstAirDate ?: "") <= java.time.LocalDate.now().toString()
                            if (!isReleased) {
                                showNotReleasedDialog = true
                            } else if (firstUnplayedEpisode != null) {
                                selectedEpisodeForSource = firstUnplayedEpisode
                                isDownloadMode = false
                            } else {
                                Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                            }
"""
text = re.sub(
r'if \(firstUnplayedEpisode != null\) \{\s*selectedEpisodeForSource = firstUnplayedEpisode\s*isDownloadMode = false\s*\} else \{\s*Toast\.makeText\(context, "No episodes available", Toast\.LENGTH_SHORT\)\.show\(\)\s*\}',
series_play_logic.strip(), text, count=1, flags=re.MULTILINE
)

with open("app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt", "w") as f:
    f.write(text)

