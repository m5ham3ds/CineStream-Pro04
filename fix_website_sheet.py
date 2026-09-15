import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Replace the broken website sheet block
old_website = r'    if \(showWebsiteSheet\) \{\s*ModalBottomSheet\(\s*onDismissRequest = \{ showWebsiteSheet = false \},\s*containerColor = MaterialTheme.colorScheme.surface\s*\)\s*\{\s*LazyColumn\(modifier = Modifier\.fillMaxWidth\(\)\)\s*\{\s*item\s*\{\s*Column\(modifier = Modifier\.padding\(16\.dp\)\)\s*\{.*?Spacer\(modifier = Modifier\.height\(32\.dp\)\)\s*\}\s*\}\s*\}\s*'
# Wait, let's just find the start of `if (showWebsiteSheet) {` to `if (showDownloadSheet) {`

match = re.search(r'(    if \(showWebsiteSheet\) \{.*?\n)    if \(showDownloadSheet\) \{', content, re.DOTALL)
if match:
    new_website = """    if (showWebsiteSheet) {
        ModalBottomSheet(
            onDismissRequest = { showWebsiteSheet = false },
            containerColor = MaterialTheme.colorScheme.surface
        ) {
            LazyColumn(modifier = Modifier.fillMaxWidth()) {
                item {
                    Text(stringResource(R.string.select_source), modifier = Modifier.padding(horizontal = 16.dp), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                    Spacer(modifier = Modifier.height(16.dp))
                }
                items(uiState.availableWebsites) { w ->
                    TextButton(
                        onClick = { 
                            viewModel.selectWebsite(w)
                            showWebsiteSheet = false
                            android.widget.Toast.makeText(context, "Switched source to $w", android.widget.Toast.LENGTH_SHORT).show()
                        },
                        modifier = Modifier.fillMaxWidth(),
                        contentPadding = PaddingValues(vertical = 16.dp)
                    ) {
                        Text(w, color = if (w == uiState.currentWebsite) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.onBackground)
                    }
                }
                item { Spacer(modifier = Modifier.height(32.dp)) }
            }
        }
    }

"""
    content = content[:match.start(1)] + new_website + content[match.end(1):]
    with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
        f.write(content)
    print("Fixed website sheet")
else:
    print("Not found")
