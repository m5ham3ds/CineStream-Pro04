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

    # Add imports
    if 'import androidx.compose.foundation.pager.HorizontalPager' not in content:
        content = content.replace('import androidx.compose.foundation.layout.*', 'import androidx.compose.foundation.pager.HorizontalPager\nimport androidx.compose.foundation.pager.rememberPagerState\nimport kotlinx.coroutines.launch\nimport androidx.compose.foundation.layout.*')

    # Find the top part
    old_top = 'var selectedTab by remember { mutableStateOf("All") }'
    new_top = '''val tabsList = listOf("All", "Movies", "Series", stringResource(R.string.anime))
    val pagerState = rememberPagerState(pageCount = { tabsList.size })
    val coroutineScope = rememberCoroutineScope()
    val selectedTab = tabsList[pagerState.currentPage]'''
    
    if old_top in content:
        content = content.replace(old_top, new_top)

    old_items = '''val items = when (selectedTab) {'''
    new_items = '''val getItemsForTab = { tab: String -> 
        when (tab) {'''
    if old_items in content:
        content = content.replace(old_items, new_items)

    old_tabs_row = '''val tabs = listOf("All", "Movies", "Series", stringResource(R.string.anime))
            tabs.forEach { tab ->'''
    new_tabs_row = '''tabsList.forEach { tab ->'''
    if old_tabs_row in content:
        content = content.replace(old_tabs_row, new_tabs_row)

    old_clickable = '''.clickable { selectedTab = tab }'''
    new_clickable = '''.clickable { coroutineScope.launch { pagerState.animateScrollToPage(tabsList.indexOf(tab)) } }'''
    if old_clickable in content:
        content = content.replace(old_clickable, new_clickable)

    # Now wrap the PullToRefreshBox with HorizontalPager
    old_ptr = '''val ptrState = rememberPullToRefreshState()
        PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
            if (uiState.isLoading && items.isEmpty()) {'''
            
    new_ptr = '''val ptrState = rememberPullToRefreshState()
        HorizontalPager(state = pagerState, modifier = Modifier.fillMaxSize()) { page ->
            val currentTab = tabsList[page]
            val items = getItemsForTab(currentTab)
            PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
                if (uiState.isLoading && items.isEmpty()) {'''
                
    if old_ptr in content:
        content = content.replace(old_ptr, new_ptr)
        
        # We also need to add a closing brace for HorizontalPager at the end of the file.
        # Let's just find the last two closing braces and insert one before them.
        content = content.rsplit('}', 2)
        content = content[0] + '}\n        }\n    }\n}'

    with open(file_path, 'w') as f:
        f.write(content)

