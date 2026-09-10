package com.example.ui.screens.home

import androidx.compose.foundation.background
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.grid.GridCells
import androidx.compose.foundation.lazy.grid.LazyVerticalGrid
import androidx.compose.foundation.lazy.grid.itemsIndexed
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material3.*
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaCard
import com.example.ui.components.CustomTopBar

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun PopularScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit,
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    var selectedTab by remember { mutableStateOf("All") }
    
    val items = when (selectedTab) {
        "Movies" -> uiState.trendingMovies.map { it to true }
        "Series" -> uiState.trendingSeries.map { it to false }
        stringResource(R.string.anime) -> uiState.animeSeries.map { it to false }
        else -> (uiState.trendingMovies.map { it to true } + uiState.trendingSeries.map { it to false } + uiState.animeSeries.map { it to false })
    }
    
    Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        CustomTopBar(
            titleFirst = stringResource(R.string.popular_title_first), titleSecond = stringResource(R.string.popular_title_second), subtitle = stringResource(R.string.popular_subtitle), onBack = onBack, showFilter = true
        )
        
        Row(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp)
                .border(1.dp, MaterialTheme.colorScheme.surfaceVariant, RoundedCornerShape(12.dp)).clip(RoundedCornerShape(12.dp)),
            horizontalArrangement = Arrangement.SpaceEvenly
        ) {
            val tabs = listOf("All", "Movies", "Series", stringResource(R.string.anime))
            tabs.forEach { tab ->
                val isSelected = selectedTab == tab
                Box(
                    modifier = Modifier.weight(1f).clickable { selectedTab = tab }
                        .background(if (isSelected) MaterialTheme.colorScheme.surfaceVariant else Color.Transparent)
                        .border(if (isSelected) 1.dp else 0.dp, if (isSelected) MaterialTheme.colorScheme.primary else Color.Transparent, RoundedCornerShape(12.dp))
                        .padding(vertical = 12.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(tab, color = if (isSelected) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant, fontWeight = if (isSelected) FontWeight.Bold else FontWeight.Normal, fontSize = 14.sp)
                }
            }
        }
        
        Spacer(modifier = Modifier.height(8.dp))
        
        val ptrState = rememberPullToRefreshState()
        PullToRefreshBox(isRefreshing = uiState.isLoading, onRefresh = { viewModel.loadData() }, state = ptrState, modifier = Modifier.fillMaxSize()) {
            if (uiState.isLoading && items.isEmpty()) {
                com.example.ui.components.GridScreenSkeleton()
            } else {
                LazyVerticalGrid(columns = GridCells.Fixed(3), contentPadding = PaddingValues(start = 16.dp, end = 16.dp, bottom = 100.dp), horizontalArrangement = Arrangement.spacedBy(12.dp), verticalArrangement = Arrangement.spacedBy(12.dp)) {
                itemsIndexed(items) { index, (media, isMovie) ->
                    // Dynamic check for Media type
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
