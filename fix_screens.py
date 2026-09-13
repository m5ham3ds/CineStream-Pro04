import re
import os

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

    # If already fully migrated with tabsList, skip or clean up
    # Since they are messed up, let's use regex to extract the `getItemsForTab` body or `items = when` body.
    
    # 1. Imports
    if 'import androidx.compose.foundation.pager.HorizontalPager' not in content:
        content = content.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.pager.HorizontalPager\nimport androidx.compose.foundation.pager.rememberPagerState\nimport kotlinx.coroutines.launch\nimport androidx.compose.foundation.layout.*')

    # 2. Extract when block
    when_match = re.search(r'(val items = when.*?\{.*?\}|val getItemsForTab = \{ tab: String ->\s*when \(tab\) \{.*?\n\s*\})', content, re.DOTALL)
    if when_match:
        when_block = when_match.group(1)
        # Convert to function
        if 'val items = when' in when_block:
            when_body = when_block.replace('val items = when (selectedTab) {', '').strip()
            # remove last brace
            when_body = when_body[:-1].strip()
        else:
            when_body = when_block.replace('val getItemsForTab = { tab: String ->', '').strip()
            if when_body.startswith('when (tab) {'):
                when_body = when_body[len('when (tab) {'):].strip()
            when_body = when_body[:-1].strip() # remove last brace
            when_body = when_body[:-1].strip() # remove second last brace (from function)
            
        new_items_func = f'''val getItemsForTab = {{ tab: String -> 
        when (tab) {{
            {when_body}
        }}
    }}'''
        content = content.replace(when_block, new_items_func)

    # 3. Clean up old tab declarations
    content = re.sub(r'var selectedTab by remember \{ mutableStateOf\("All"\) \}', '', content)
    content = re.sub(r'val tabs = listOf\("All", "Movies", "Series", stringResource\(R.string.anime\)\)\n\s*val pagerState = rememberPagerState\(pageCount = \{ tabs.size \}\)\n\s*val coroutineScope = rememberCoroutineScope\(\)\n\s*val selectedTab = tabs\[pagerState.currentPage\]', '', content)
    content = re.sub(r'val tabsList = listOf\("All", "Movies", "Series", stringResource\(R.string.anime\)\)\n\s*val pagerState = rememberPagerState\(pageCount = \{ tabsList.size \}\)\n\s*val coroutineScope = rememberCoroutineScope\(\)\n\s*val selectedTab = tabsList\[pagerState.currentPage\]', '', content)
    
    # Add proper top declarations
    # Find `val uiState by viewModel.uiState.collectAsState()`
    top_decl = '''val uiState by viewModel.uiState.collectAsState()
    val tabsList = listOf("All", "Movies", "Series", stringResource(R.string.anime))
    val pagerState = rememberPagerState(pageCount = { tabsList.size })
    val coroutineScope = rememberCoroutineScope()
    val selectedTab = tabsList[pagerState.currentPage]'''
    content = re.sub(r'val uiState by viewModel.uiState.collectAsState\(\)', top_decl, content, count=1)

    # 4. Clean up Row content
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
        
    # 5. Fix PullToRefreshBox and LazyVerticalGrid
    # Since it's nested differently now, let's just replace from ptrState to the end.
    ptr_match = re.search(r'val ptrState = rememberPullToRefreshState\(\).*', content, re.DOTALL)
    if ptr_match:
        ptr_content = ptr_match.group(0)
        
        # We need to rebuild it cleanly
        new_ptr = '''val ptrState = rememberPullToRefreshState()
        HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
            val currentTab = tabsList[page]
            val items = getItemsForTab(currentTab)
            PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
                if (uiState.isLoading && items.isEmpty()) {
                    com.example.ui.components.GridScreenSkeleton()
                } else {
                    LazyVerticalGrid(columns = GridCells.Fixed(3), contentPadding = PaddingValues(start = 16.dp, end = 16.dp, bottom = 100.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                        itemsIndexed(items) { index, (media, isMovie) ->
                            val title = if (isMovie) (media as com.example.domain.models.Movie).title else (media as com.example.domain.models.Series).title
                            val poster = if (isMovie) (media as com.example.domain.models.Movie).posterUrl else (media as com.example.domain.models.Series).posterUrl
                            val id = if (isMovie) (media as com.example.domain.models.Movie).id else (media as com.example.domain.models.Series).id
                            MediaCard(
                                title = title,
                                posterUrl = poster,
                                isMovie = isMovie,
                                rank = index + 1,
                                mediaId = id,
                                onClick = { onItemClick(id, isMovie) }
                            )
                        }
                    }
                }
            }
        }
    }
}'''
        content = content.replace(ptr_content, new_ptr)

    with open(file_path, 'w') as f:
        f.write(content)

