import re
with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "r") as f:
    content = f.read()

# Add itemToDelete state
if "var itemToDelete by remember { mutableStateOf<DownloadItem?>(null) }" not in content:
    content = content.replace(
        "var selectedTab by remember { mutableStateOf(\"All\") }",
        "var selectedTab by remember { mutableStateOf(\"All\") }\n    var itemToDelete by remember { mutableStateOf<DownloadItem?>(null) }"
    )

# Add the dialog before the end of the DownloadsScreen function
dialog_code = """
    itemToDelete?.let { item ->
        AlertDialog(
            onDismissRequest = { itemToDelete = null },
            title = { Text(stringResource(R.string.delete_download_title, item.title)) },
            text = { Text(stringResource(R.string.delete_download_desc)) },
            confirmButton = {
                TextButton(onClick = {
                    scope.launch {
                        downloadRepository.removeFromDownloads(item)
                    }
                    itemToDelete = null
                }) {
                    Text(stringResource(R.string.delete_confirm), color = Color.Red)
                }
            },
            dismissButton = {
                TextButton(onClick = { itemToDelete = null }) {
                    Text(stringResource(R.string.cancel))
                }
            },
            containerColor = MaterialTheme.colorScheme.surface,
            titleContentColor = MaterialTheme.colorScheme.onBackground,
            textContentColor = MaterialTheme.colorScheme.onSurfaceVariant
        )
    }
"""
if "AlertDialog" not in content:
    content = content.replace(
        "    LazyColumn(",
        dialog_code + "\n    LazyColumn("
    )

# Update the onDelete lambda
content = content.replace(
    """                    onDelete = {
                        scope.launch {
                            downloadRepository.removeFromDownloads(item)
                        }
                    }""",
    """                    onDelete = {
                        itemToDelete = item
                    }"""
)

with open("app/src/main/java/com/example/ui/screens/downloads/DownloadsScreen.kt", "w") as f:
    f.write(content)

# We need to add strings for R.string.delete_download_title, delete_download_desc, delete_confirm, cancel
