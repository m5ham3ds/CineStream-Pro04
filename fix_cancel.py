import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

target = "extractingEmbedUrl?.let { url ->"

cancel_dialog_code = """
        if (showCancelConfirmDialog) {
            androidx.compose.material3.AlertDialog(
                onDismissRequest = { showCancelConfirmDialog = false },
                title = { Text("إلغاء العملية", color = MaterialTheme.colorScheme.onBackground) },
                text = { Text("هل أنت متأكد أنك تود إلغاء العملية؟", color = Color.LightGray) },
                containerColor = Color(0xFF222225),
                confirmButton = {
                    androidx.compose.material3.TextButton(
                        onClick = {
                            showCancelConfirmDialog = false
                            onDismiss()
                        }
                    ) {
                        Text("نعم", color = MaterialTheme.colorScheme.error)
                    }
                },
                dismissButton = {
                    androidx.compose.material3.TextButton(onClick = { showCancelConfirmDialog = false }) {
                        Text("لا", color = MaterialTheme.colorScheme.onBackground)
                    }
                }
            )
        }
        
"""

c = c.replace(target, cancel_dialog_code + target)

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "w") as f:
    f.write(c)

