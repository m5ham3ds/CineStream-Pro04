import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# Fix the padding of LazyColumn and TextButton in all ModalBottomSheets
# Old: LazyColumn(modifier = Modifier.padding(16.dp).fillMaxWidth())
# New: LazyColumn(modifier = Modifier.fillMaxWidth())

content = content.replace("LazyColumn(modifier = Modifier.padding(16.dp).fillMaxWidth())", "LazyColumn(modifier = Modifier.fillMaxWidth())")

# Add PaddingValues to TextButton
content = content.replace("modifier = Modifier.fillMaxWidth()\n                    ) {", "modifier = Modifier.fillMaxWidth(),\n                        contentPadding = PaddingValues(vertical = 16.dp)\n                    ) {")

# Add padding to the header Texts instead
content = re.sub(r'item\s*\{\s*Text\(', r'item {\n                    Text(modifier = Modifier.padding(horizontal = 16.dp),\n                        ', content)

# Website sheet uses Column
website_old = """    if (showWebsiteSheet) {
        ModalBottomSheet(
            onDismissRequest = { showWebsiteSheet = false },
            containerColor = MaterialTheme.colorScheme.surface
        ) {
            Column(modifier = Modifier.padding(16.dp).verticalScroll(androidx.compose.foundation.rememberScrollState())) {
                Text(stringResource(R.string.select_source), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleLarge, fontWeight = FontWeight.Bold)
                Spacer(modifier = Modifier.height(16.dp))
                uiState.availableWebsites.forEach { w ->
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
                Spacer(modifier = Modifier.height(32.dp))
            }
        }
    }"""

website_new = """    if (showWebsiteSheet) {
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
    }"""

if website_old in content:
    content = content.replace(website_old, website_new)
else:
    # Just replace it roughly
    print("Website old block not exact match, doing regex")
    content = re.sub(r'Column\(modifier = Modifier\.padding\(16\.dp\)\.verticalScroll\(androidx\.compose\.foundation\.rememberScrollState\(\)\)\)\s*\{.*?(Spacer\(modifier = Modifier\.height\(32\.dp\)\))\s*\}',
        r'LazyColumn(modifier = Modifier.fillMaxWidth()) {\nitem { Text("Sources", modifier=Modifier.padding(horizontal=16.dp), style=MaterialTheme.typography.titleLarge) }\nitems(uiState.availableWebsites) { w -> TextButton(onClick={viewModel.selectWebsite(w); showWebsiteSheet = false}, modifier=Modifier.fillMaxWidth(), contentPadding=PaddingValues(vertical=16.dp)) { Text(w) } }\nitem { \1 }\n}',
        content, flags=re.DOTALL)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
