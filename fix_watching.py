import re
import os

file_path = 'app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt'
with open(file_path, 'r') as f:
    content = f.read()

# Replace pill tabs row correctly
tabs_list_row = '''Row(
            modifier = Modifier
                .fillMaxWidth()
                .padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            tabsList.forEach { tab ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier
                        .clickable { coroutineScope.launch { pagerState.animateScrollToPage(tabsList.indexOf(tab)) } }
                        .clip(RoundedCornerShape(16.dp))
                        .background(if (isSelected) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface)
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = tab,
                        color = MaterialTheme.colorScheme.onBackground,
                        fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal,
                        fontSize = 14.sp
                    )
                }
            }
        }
'''
content = re.sub(r'Row\(\s*modifier = Modifier\s*\.fillMaxWidth\(\)\s*\.padding\(horizontal = 16.dp, vertical = 8.dp\),\s*horizontalArrangement = Arrangement.spacedBy\(8.dp\)\s*\)\s*\{.*?\}\s*\}', tabs_list_row, content, flags=re.DOTALL)

# Replace the LazyColumn content with HorizontalPager
old_list = '''if (historyItems.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(stringResource(R.string.no_watching_items), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 16.sp)
            }
        } else {
            LazyColumn(
                contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
                verticalArrangement = Arrangement.spacedBy(16.dp),
                modifier = Modifier.fillMaxSize()
            ) {
                items(items) { item ->
                    DetailedContinueWatchingCard(item = item, onClick = { onItemClick(item.id, item.isMovie) })
                }
            }
        }'''

new_list = '''if (historyItems.isEmpty()) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(stringResource(R.string.no_watching_items), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 16.sp)
            }
        } else {
            HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
                val currentTab = tabsList[page]
                val items = getItemsForTab(currentTab)
                LazyColumn(
                    contentPadding = PaddingValues(start = 16.dp, end = 16.dp, top = 8.dp, bottom = 100.dp),
                    verticalArrangement = Arrangement.spacedBy(16.dp),
                    modifier = Modifier.fillMaxSize()
                ) {
                    items(items) { item ->
                        DetailedContinueWatchingCard(item = item, onClick = { onItemClick(item.id, item.isMovie) })
                    }
                }
            }
        }'''

if old_list in content:
    content = content.replace(old_list, new_list)

with open(file_path, 'w') as f:
    f.write(content)

