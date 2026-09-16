import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

target = """                            if (showNoMoreExtensionsDialog) {
                                AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text("لا يوجد مواقع أخرى", color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text("عذراً، فشل البحث في جميع المواقع المتاحة.", color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) {
                                            Text("إغلاق", color = MaterialTheme.colorScheme.primary)
                                        }
                                    }
                                )
                            }"""

replacement = """                            if (showNoMoreExtensionsDialog) {
                                androidx.compose.material3.AlertDialog(
                                    onDismissRequest = { showNoMoreExtensionsDialog = false },
                                    title = { Text("لا يوجد مواقع أخرى", color = MaterialTheme.colorScheme.onBackground) },
                                    text = { Text("عذراً، فشل البحث في جميع المواقع المتاحة.", color = Color.LightGray) },
                                    containerColor = Color(0xFF222225),
                                    confirmButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                                onNavigateToExtensions()
                                            }
                                        ) {
                                            Text("الإضافات", color = MaterialTheme.colorScheme.primary)
                                        }
                                    },
                                    dismissButton = {
                                        androidx.compose.material3.TextButton(
                                            onClick = {
                                                showNoMoreExtensionsDialog = false
                                                onDismiss()
                                            }
                                        ) {
                                            Text("إغلاق", color = Color.LightGray)
                                        }
                                    }
                                )
                            }"""

if target in c:
    c = c.replace(target, replacement)
    print("Replaced no_more_extensions successfully.")
else:
    print("Could not find target block!")

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

