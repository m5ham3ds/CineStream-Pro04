import re
import os

filepath = 'app/src/main/java/com/example/ui/screens/details/DetailsScreens.kt'
with open(filepath, 'r') as f:
    content = f.read()

# 1. Add scroll detection at the top of SeriesDetailsScreen
# Find `val scrollState = rememberScrollState()`
scroll_state_decl = '''    val scrollState = rememberScrollState()
    
    val isScrollNearBottom by remember {
        derivedStateOf { scrollState.value >= scrollState.maxValue - 150 && scrollState.maxValue > 0 }
    }
    
    LaunchedEffect(isScrollNearBottom) {
        if (isScrollNearBottom) {
            if (uiState.episodes.isEmpty() && !uiState.isEpisodesLoading) {
                viewModel.triggerInitialEpisodesLoad()
            } else if (uiState.episodes.size > uiState.visibleEpisodesCount && !uiState.isLoadingMore) {
                viewModel.loadMoreEpisodes()
            }
        }
    }'''
content = re.sub(r'    val scrollState = rememberScrollState\(\)', scroll_state_decl, content)

# 2. Replace TextButton Load More
load_more_button = '''if (uiState.episodes.size > uiState.visibleEpisodesCount) {
                            TextButton(
                                onClick = { viewModel.loadMoreEpisodes() },
                                modifier = Modifier.fillMaxWidth().padding(vertical = 16.dp)
                            ) {
                                Text("Load More Episodes", color = MaterialTheme.colorScheme.primary, fontWeight = FontWeight.Bold)
                            }
                        }'''

new_load_more = '''if (uiState.episodes.size > uiState.visibleEpisodesCount || uiState.isLoadingMore) {
                            Box(modifier = Modifier.fillMaxWidth().padding(vertical = 24.dp), contentAlignment = Alignment.Center) {
                                if (uiState.isLoadingMore) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                                        Spacer(modifier = Modifier.width(12.dp))
                                        Text("جاري تحميل الحلقات...", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                                    }
                                } else {
                                    Text("اسحب للأعلى لتحميل المزيد", color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                                }
                            }
                        }'''
content = content.replace(load_more_button, new_load_more)

with open(filepath, 'w') as f:
    f.write(content)
