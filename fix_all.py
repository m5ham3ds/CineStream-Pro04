import os
import re

files = [
    'app/src/main/java/com/example/ui/screens/home/TrendingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/NewReleasesScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/PopularScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/WatchingScreen.kt',
    'app/src/main/java/com/example/ui/screens/home/UpcomingScreen.kt'
]

for file_path in files:
    if not os.path.exists(file_path):
        continue
    with open(file_path, 'r') as f:
        content = f.read()

    # Define anime string outside
    anime_decl = 'val animeStr = stringResource(R.string.anime)'
    if anime_decl not in content:
        # insert after collectAsState
        content = re.sub(r'(val uiState by viewModel.uiState.collectAsState\(\))', r'\1\n    ' + anime_decl, content)
        # For WatchingScreen which might have different state
        content = re.sub(r'(val historyItems by historyRepository.getHistoryItems\(\).collectAsState\(initial = emptyList\(\)\))', r'\1\n    ' + anime_decl, content)

    # replace stringResource(R.string.anime) with animeStr
    content = content.replace('stringResource(R.string.anime)', 'animeStr')

    # Fix WatchingScreen
    if 'WatchingScreen' in file_path:
        # Add the definitions if missing
        if 'val tabsList =' not in content:
            # find where `val filteredItems = when` is
            top_decl = '''val tabsList = listOf("All", "Movies", "TV Series", animeStr)
    val pagerState = rememberPagerState(pageCount = { tabsList.size })
    val coroutineScope = rememberCoroutineScope()
    val selectedTab = tabsList[pagerState.currentPage]'''
            content = re.sub(r'val filteredItems = when \(selectedTab\) \{', top_decl + '\n    val getItemsForTab = { tab: String -> when (tab) {', content)
            
            # also fix the end of `when` block
            content = content.replace('else -> historyItems\n    }', 'else -> historyItems\n        }\n    }')
            
            # replace `filteredItems` with `items` everywhere
            content = content.replace('filteredItems', 'items')
            
            # replace row
            row_match = re.search(r'Row\(\s*modifier = Modifier.*?horizontalArrangement = Arrangement.SpaceEvenly\s*\)\s*\{.*?\n\s*Spacer\(modifier = Modifier.height\(8.dp\)\)', content, re.DOTALL)
            if row_match:
                row_content = row_match.group(0)
                new_row = '''Row(
                    modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
                        .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(12.dp)).clip(RoundedCornerShape(12.dp)),
                    horizontalArrangement = Arrangement.SpaceEvenly
                ) {
                    tabsList.forEach { tab ->
                        val isSelected = selectedTab == tab
                        Box(
                            modifier = Modifier.weight(1f).clickable { coroutineScope.launch { pagerState.animateScrollToPage(tabsList.indexOf(tab)) } }
                                .background(if (isSelected) MaterialTheme.colorScheme.surfaceVariant else Color.Transparent)
                                .border(if (isSelected) 1.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.primary else Color.Transparent, RoundedCornerShape(12.dp))
                                .padding(vertical = 12.dp),
                            contentAlignment = Alignment.Center
                        ) {
                            Text(tab, color = if (isSelected) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal, fontSize = 14.sp)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(8.dp))'''
                content = content.replace(row_content, new_row)
            
            # wrap LazyColumn
            lazy_col_match = re.search(r'if \(items.isEmpty\(\)\) \{.*?LazyColumn\(.*?\)\s*\{\s*items\(items\)\s*\{.*?\}\s*\}\s*\}', content, re.DOTALL)
            if lazy_col_match:
                lazy_content = lazy_col_match.group(0)
                new_lazy = '''HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
                    val currentTab = tabsList[page]
                    val items = getItemsForTab(currentTab)
                    ''' + lazy_content + '\n                }'
                content = content.replace(lazy_content, new_lazy)

    with open(file_path, 'w') as f:
        f.write(content)

