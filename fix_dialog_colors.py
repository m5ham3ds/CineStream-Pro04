with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "r") as f:
    content = f.read()

old_dialog = """    if (showDownloadSettingsDialog) {
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
    }"""

new_dialog = """    if (showDownloadSettingsDialog) {
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
                        steps = 3,
                        colors = androidx.compose.material3.SliderDefaults.colors(
                            thumbColor = MaterialTheme.colorScheme.primary,
                            activeTrackColor = MaterialTheme.colorScheme.primary
                        )
                    )
                    Spacer(modifier = Modifier.height(16.dp))
                    Text(stringResource(R.string.max_segments_per_download) + ": $maxSegments", fontSize = 14.sp)
                    androidx.compose.material3.Slider(
                        value = maxSegments.toFloat(),
                        onValueChange = { coroutineScope.launch { userPrefs.saveMaxSegments(it.toInt()) } },
                        valueRange = 1f..32f,
                        steps = 30,
                        colors = androidx.compose.material3.SliderDefaults.colors(
                            thumbColor = MaterialTheme.colorScheme.primary,
                            activeTrackColor = MaterialTheme.colorScheme.primary
                        )
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
                                onClick = { coroutineScope.launch { userPrefs.saveDownloadNetwork(index) } },
                                colors = androidx.compose.material3.RadioButtonDefaults.colors(
                                    selectedColor = MaterialTheme.colorScheme.primary
                                )
                            )
                            Text(stringResource(titleRes), fontSize = 14.sp)
                        }
                    }
                }
            },
            confirmButton = {
                TextButton(onClick = { showDownloadSettingsDialog = false }) { 
                    Text(stringResource(R.string.done), color = MaterialTheme.colorScheme.primary) 
                }
            },
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onSurface,
            textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }"""

content = content.replace(old_dialog, new_dialog)

with open("app/src/main/java/com/example/ui/screens/settings/SettingsScreen.kt", "w") as f:
    f.write(content)
