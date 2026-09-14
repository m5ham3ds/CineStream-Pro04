package com.example.ui.screens.home
import com.example.ui.components.rememberCardMediaDetail
import com.example.ui.components.CardMediaDetail
import kotlin.math.absoluteValue
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.material.icons.filled.Pause

import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.outlined.ArrowBack

import androidx.compose.foundation.background
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.pager.HorizontalPager
import androidx.compose.foundation.pager.rememberPagerState
import kotlinx.coroutines.launch
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.MoreVert
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.res.painterResource
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import coil.compose.AsyncImage
import com.example.data.model.HistoryItem
import com.example.data.repository.HistoryRepository
import com.example.ui.components.CustomTopBar

@Composable
fun WatchingScreen(
    onItemClick: (String, Boolean) -> Unit,
    onBack: () -> Unit
) {
    val context = LocalContext.current
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val allStr = stringResource(R.string.all)
    val moviesStr = stringResource(R.string.movies)
    val seriesStr = stringResource(R.string.series)
    val animeStr = stringResource(R.string.anime)
    

    val tabsList = listOf(allStr, moviesStr, seriesStr, animeStr)
    val pagerState = rememberPagerState(pageCount = { tabsList.size })
    val coroutineScope = rememberCoroutineScope()
    val selectedTab = tabsList[pagerState.currentPage]
    val getItemsForTab = { tab: String -> when (tab) {
        moviesStr -> historyItems.filter { it.isMovie }
        seriesStr -> historyItems.filter { !it.isMovie } // Assume TV Series if not movie
        animeStr -> emptyList() // You can adjust this if HistoryItem adds anime type
        else -> historyItems
        }
    }

    Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        CustomTopBar(
            titleFirst = stringResource(R.string.watching_title_first),
            titleSecond = stringResource(R.string.watching_title_second),
            subtitle = stringResource(R.string.watching_subtitle),
            onBack = onBack,
            showFilter = false
        )

        // Pill Tabs
        Row(
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
        if (historyItems.isEmpty()) {
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
                    items(items, key = { it.id }) { item ->
                        DetailedContinueWatchingCard(item = item, onClick = { onItemClick(item.id, item.isMovie) })
                    }
                }
            }
        }
    }
}

@Composable
fun DetailedContinueWatchingCard(item: com.example.data.model.HistoryItem, onClick: () -> Unit) {
    val mediaDetail = rememberCardMediaDetail(item) ?: CardMediaDetail(
        title = item.title, year = "", rating = "", overview = "", backdropUrl = item.posterUrl, isMovie = item.isMovie
    )
    val typeText = if (mediaDetail.isMovie) stringResource(R.string.movies) else stringResource(R.string.series)
    val fakeProgress = (Math.abs(item.id.hashCode()) % 100) / 100f
    
    Box(
        modifier = Modifier
            .fillMaxWidth()
            .height(140.dp)
            .clip(RoundedCornerShape(16.dp))
            .background(MaterialTheme.colorScheme.surface)
            .border(1.dp, MaterialTheme.colorScheme.primary.copy(alpha=0.5f), RoundedCornerShape(16.dp))
            .clickable { onClick() }
    ) {
        Row(modifier = Modifier.fillMaxSize()) {
            // Left Image Section
            Box(
                modifier = Modifier
                    .weight(0.45f)
                    .fillMaxHeight()
                    .clip(RoundedCornerShape(topStart = 16.dp, bottomStart = 16.dp))
            ) {
                coil.compose.AsyncImage(
                    model = mediaDetail.backdropUrl,
                    contentDescription = mediaDetail.title,
                    contentScale = ContentScale.Crop,
                    modifier = Modifier.fillMaxSize()
                )
                Box(modifier = Modifier.fillMaxSize().background(Color.Black.copy(alpha = 0.2f)))
                
                // Bottom Left Badge "Movie"
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .padding(start = 8.dp, bottom = 16.dp)
                        .background(Color.Black.copy(alpha = 0.7f), RoundedCornerShape(4.dp))
                        .padding(horizontal = 6.dp, vertical = 2.dp)
                ) {
                    Text(text = typeText, color = Color.White, fontSize = 12.sp, fontWeight = FontWeight.Bold)
                }
                
                // Bottom Right Time
                Text(
                    text = "32:14 / 1:54:20",
                    color = Color.White,
                    fontSize = 11.sp,
                    fontWeight = FontWeight.Bold,
                    modifier = Modifier.align(Alignment.BottomEnd).padding(end = 8.dp, bottom = 16.dp)
                )
                
                // Progress Bar at the very bottom
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomStart)
                        .fillMaxWidth()
                        .padding(horizontal = 8.dp, bottom = 6.dp)
                        .height(4.dp)
                        .clip(RoundedCornerShape(2.dp))
                        .background(Color.Gray.copy(alpha=0.5f))
                ) {
                    Box(
                        modifier = Modifier
                            .fillMaxWidth(fakeProgress.coerceAtLeast(0.1f))
                            .fillMaxHeight()
                            .background(MaterialTheme.colorScheme.primary)
                    )
                }
            }
            
            // Right Content Section
            Box(
                modifier = Modifier
                    .weight(0.55f)
                    .fillMaxHeight()
            ) {
                Column(
                    modifier = Modifier
                        .fillMaxSize()
                        .padding(12.dp)
                ) {
                    Row(
                        modifier = Modifier.fillMaxWidth(),
                        horizontalArrangement = Arrangement.SpaceBetween,
                        verticalAlignment = Alignment.Top
                    ) {
                        Text(
                            text = mediaDetail.title,
                            color = Color.White,
                            fontSize = 18.sp,
                            fontWeight = FontWeight.Bold,
                            maxLines = 1,
                            overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                            modifier = Modifier.weight(1f)
                        )
                        Icon(
                            imageVector = androidx.compose.material.icons.Icons.Default.MoreVert,
                            contentDescription = "More",
                            tint = Color.Gray,
                            modifier = Modifier.size(20.dp)
                        )
                    }
                    
                    Spacer(modifier = Modifier.height(2.dp))
                    
                    Text(
                        text = "${mediaDetail.year} | $typeText |",
                        color = Color.Gray,
                        fontSize = 12.sp
                    )
                    
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    Text(
                        text = mediaDetail.overview,
                        color = Color.Gray,
                        fontSize = 12.sp,
                        maxLines = 3,
                        overflow = androidx.compose.ui.text.style.TextOverflow.Ellipsis,
                        lineHeight = 16.sp
                    )
                }
                
                // Big FAB-like play button at bottom right
                Box(
                    modifier = Modifier
                        .align(Alignment.BottomEnd)
                        .padding(end = 12.dp, bottom = 12.dp)
                        .size(44.dp)
                        .background(MaterialTheme.colorScheme.primary, CircleShape),
                    contentAlignment = Alignment.Center
                ) {
                    Icon(
                        imageVector = androidx.compose.material.icons.Icons.Filled.PlayArrow,
                        contentDescription = "Play",
                        tint = Color.White,
                        modifier = Modifier.size(26.dp)
                    )
                }
            }
        }
    }
}

