import re

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

# Add a state for showing download settings dialog
state_insert = """
    var showStartScreenSheet by remember { mutableStateOf(false) }
    var showDownloadSettingsDialog by remember { mutableStateOf(false) }
    
    val maxConcurrentDownloads by userPrefs.maxConcurrentDownloads.collectAsState(initial = 3)
    val maxSegments by userPrefs.maxSegments.collectAsState(initial = 8)
    val downloadNetwork by userPrefs.downloadNetwork.collectAsState(initial = 0)
"""
content = re.sub(r'var showStartScreenSheet by remember \{ mutableStateOf\(false\) \}', state_insert, content)

# Add Download Settings menu item under About, or General
menu_insert = """
                SettingsListItem(
                    icon = Icons.Default.Download,
                    title = stringResource(R.string.download_settings),
                    subtitle = stringResource(R.string.configure_downloads),
                    isLast = true,
                    onClick = { showDownloadSettingsDialog = true }
                )
            }
"""
# We'll insert it after the Language settings item inside General
general_menu_search = """
                SettingsListItem(
                    icon = Icons.Default.Language,
                    title = stringResource(R.string.language),
                    subtitle = when(appLanguage) {
                        "en" -> "English"
                        "ar" -> "العربية"
                        else -> stringResource(R.string.system_default)
                    },
                    isLast = true,
                    onClick = { showLanguageSheet = true }
                )
"""
general_menu_replace = """
                SettingsListItem(
                    icon = Icons.Default.Language,
                    title = stringResource(R.string.language),
                    subtitle = when(appLanguage) {
                        "en" -> "English"
                        "ar" -> "العربية"
                        else -> stringResource(R.string.system_default)
                    },
                    isLast = false,
                    onClick = { showLanguageSheet = true }
                )
""" + menu_insert
content = content.replace(general_menu_search, general_menu_replace)

# Now add the DownloadSettingsDialog composable at the bottom
dialog_insert = """
    if (showDownloadSettingsDialog) {
        AlertDialog(
            onDismissRequest = { showDownloadSettingsDialog = false },
            title = { Text(stringResource(R.string.download_settings)) },
            text = {
                Column {
                    Text(stringResource(R.string.max_concurrent_downloads) + ": $maxConcurrentDownloads", fontSize = 14.sp)
                    androidx.compose.material3.Slider(
                        value = maxConcurrentDownloads.toFloat(),
                        onValueChange = { coroutineScope.launch { userPrefs.saveMaxConcurrentDownloads(it.toInt()) } },
                        valueRange = 1f..5f,
                        steps = 3
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(stringResource(R.string.max_segments_per_download) + ": $maxSegments", fontSize = 14.sp)
                    androidx.compose.material3.Slider(
                        value = maxSegments.toFloat(),
                        onValueChange = { coroutineScope.launch { userPrefs.saveMaxSegments(it.toInt()) } },
                        valueRange = 1f..32f,
                        steps = 30
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(stringResource(R.string.download_network), fontSize = 14.sp, modifier = Modifier.padding(bottom = 8.dp))
                    
                    val networkOptions = listOf(R.string.network_all, R.string.network_wifi, R.string.network_cellular)
                    networkOptions.forEachIndexed { index, titleRes ->
                        Row(verticalAlignment = Alignment.CenterVertically, modifier = Modifier.fillMaxWidth().clickable {
                            coroutineScope.launch { userPrefs.saveDownloadNetwork(index) }
                        }) {
                            androidx.compose.material3.RadioButton(
                                selected = downloadNetwork == index,
                                onClick = { coroutineScope.launch { userPrefs.saveDownloadNetwork(index) } }
                            )
                            Text(stringResource(titleRes), fontSize = 14.sp)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showDownloadSettingsDialog = false }) { Text(stringResource(R.string.done)) }
            }
        )
    }
"""

# Inject dialog just before the last `}` of SettingsScreen
content = content.replace("    if (showStartScreenSheet) {", dialog_insert + "\n    if (showStartScreenSheet) {")

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(content)
