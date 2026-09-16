import re

with open("app/src/main/java/com/example/ui/screens/player/ServerSelectionDialog.kt", "r") as f:
    c = f.read()

# 1. Inject `showCancelConfirmDialog` UI
# We need to put it before `extractingEmbedUrl?.let { url ->`
cancel_dialog_code = """
        if (showCancelConfirmDialog) {
            AlertDialog(
                onDismissRequest = { showCancelConfirmDialog = false },
                title = { Text("إلغاء العملية", color = MaterialTheme.colorScheme.onBackground) },
                text = { Text("هل أنت متأكد أنك تود إلغاء العملية؟", color = androidx.compose.ui.graphics.Color.LightGray) },
                containerColor = androidx.compose.ui.graphics.Color(0xFF222225),
                confirmButton = {
                    TextButton(
                        onClick = {
                            showCancelConfirmDialog = false
                            onDismiss()
                        }
                    ) {
                        Text("نعم", color = MaterialTheme.colorScheme.error)
                    }
                },
                dismissButton = {
                    TextButton(onClick = { showCancelConfirmDialog = false }) {
                        Text("لا", color = MaterialTheme.colorScheme.onBackground)
                    }
                }
            )
        }
"""
c = c.replace("extractingEmbedUrl?.let { url ->", cancel_dialog_code + "\n        extractingEmbedUrl?.let { url ->")

# 2. Extract "تجربة موقع آخر" out of LazyColumn
# Currently it's:
#                                 item {
#                                     Spacer(modifier = Modifier.height(16.dp))
#                                     Text(
#                                         text = "تجربة موقع آخر",
# ...
#                                     )
#                                 }
#                             }
#                         } else {
pattern_servers = r"(\s*)item\s*\{\s*Spacer\(modifier = Modifier.height\(16.dp\)\)\s*Text\(\s*text = \"تجربة موقع آخر\"[^\)]+\)\s*\}\s*\}(\s*)\} else \{"
# Replacement: close the LazyColumn first, then add the spacer and text.
def repl_servers(m):
    indent = m.group(1)
    return f"{indent}}}" + m.group(0).replace(f"{indent}item {{", f"{indent}").replace("        }\n                            }\n                        } else {", "        }\n                        } else {")
    
# Let's do it manually using find and replace to be safer.
