import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

def replace_sheet(sheet_name, content):
    pattern = r'(if \(' + sheet_name + r'\) \{\s*ModalBottomSheet.*?LazyColumn.*?)\.padding\(16\.dp\)\.fillMaxWidth\(\)\)(.*?items\(.*?\)\s*\{\s*\w+\s*->\s*TextButton\([^)]*modifier = Modifier\.fillMaxWidth\(\))'
    
    def repl(m):
        # We need to make sure we add contentPadding to TextButton
        s = m.group(1) + r'.fillMaxWidth())' + m.group(2) + r', contentPadding = PaddingValues(vertical = 16.dp)'
        return s

    new_content = re.sub(pattern, repl, content, flags=re.DOTALL)
    
    # Also fix the title size
    new_content = re.sub(r'(Text\([^,]+,\s*color = MaterialTheme\.colorScheme\.onBackground,)\s*fontSize = 20\.sp,', r'\1 style = MaterialTheme.typography.titleLarge,', new_content)
    
    return new_content

content = replace_sheet('showQualitySheet', content)
content = replace_sheet('showEpisodesSheet', content)
content = replace_sheet('showServerSheet', content)

# Website sheet uses Column instead of LazyColumn in original code, let's fix it
website_old = """    if (showWebsiteSheet) {
        ModalBottomSheet(
            onDismissRequest = { showWebsiteSheet = false },
            containerColor = MaterialTheme.colorScheme.surface
        ) {
            Column(modifier = Modifier.padding(16.dp).verticalScroll(androidx.compose.foundation.rememberScrollState())) {"""

website_new = """    if (showWebsiteSheet) {
        ModalBottomSheet(
            onDismissRequest = { showWebsiteSheet = false },
            containerColor = MaterialTheme.colorScheme.surface
        ) {
            LazyColumn(modifier = Modifier.fillMaxWidth()) {
                item {
                    Column(modifier = Modifier.padding(16.dp)) {"""

if website_old in content:
    content = content.replace(website_old, website_new)
    # also we need to close the item and fix the loop
    # Wait, it's easier to just use regex for website sheet
    
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)

