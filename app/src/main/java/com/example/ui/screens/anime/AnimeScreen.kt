package com.example.ui.screens.anime

import android.widget.Toast
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.foundation.background
import androidx.compose.foundation.border
import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.lazy.itemsIndexed

import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Category
import androidx.compose.material.icons.filled.LocalMovies
import androidx.compose.material.icons.filled.NewReleases
import androidx.compose.material.icons.filled.Star
import androidx.compose.material3.*

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState

import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.ui.ViewModelFactory
import com.example.ui.components.ContinueWatchingCardShared
import com.example.ui.components.HeroSectionShared
import com.example.ui.components.MediaActionBottomSheet
import com.example.ui.components.MediaCard
import com.example.ui.components.VerticalGrid
import com.example.ui.components.MediaScreenSkeleton
import com.example.ui.components.HeroCarousel
import com.example.ui.components.HeroItem
import com.example.ui.components.SectionTitleShared
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AnimeScreen(
    onAnimeClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    onNavigateToUpcoming: () -> Unit = {},
    viewModel: AnimeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val libraryRepository = remember { LibraryRepository(context) }
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }

    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val animeHistoryItems = historyItems.filter { !it.isMovie }

    val scope = rememberCoroutineScope()

    if (uiState.isLoading) {
        MediaScreenSkeleton()
        return
    }

    if (uiState.error != null) {
        Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
            Text(text = uiState.error ?: "Unknown error", color = MaterialTheme.colorScheme.onBackground)
        }
        return
    }

    val scrollState = rememberScrollState()
    var showBottomSheet by remember { mutableStateOf(false) }
    var selectedMediaId by remember { mutableStateOf("") }
    var selectedMediaTitle by remember { mutableStateOf("") }
    var selectedMediaPoster by remember { mutableStateOf("") }

    val animeStr = stringResource(R.string.anime)
    var selectedCategory by remember { mutableStateOf("Anime") }

    data class CategoryItem(val id: String, val label: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)
    val categories = listOf(
        CategoryItem("Anime", stringResource(R.string.category_anime), Icons.Default.LocalMovies),
        
        CategoryItem("Genres", stringResource(R.string.category_genres), Icons.Default.Category),
        CategoryItem("New Releases", stringResource(R.string.new_releases), Icons.Default.NewReleases),
        CategoryItem("Top Rated", stringResource(R.string.category_top_rated), Icons.Default.Star)
    )
    val ptrState = rememberPullToRefreshState()
    
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadData() },
        state = ptrState,
        modifier = Modifier.fillMaxSize()
    ) {


    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            
    ) {
        // Hero Section
        HeroCarousel(items = uiState.newEpisodes.take(10).map { HeroItem(it.id, it.title, it.backdropUrl, false) }, onClick = onAnimeClick)


        Spacer(modifier = Modifier.height(16.dp))
        // Categories Tab Row
        LazyRow(
            modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 8.dp),
            horizontalArrangement = Arrangement.spacedBy(8.dp)
        ) {
            items(categories) { category ->
                Box(
                    modifier = Modifier
                        .clip(RoundedCornerShape(8.dp))
                        .background(if (selectedCategory == category.id) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface)
                        .clickable {
                            if (selectedCategory == category.id) {
                                selectedCategory = animeStr
                            } else {
                                selectedCategory = category.id
                            }
                        }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = category.icon, 
                            contentDescription = category.label, 
                            tint = if (selectedCategory == category.id) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = category.label,
                            color = if (selectedCategory == category.id) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 14.sp,
                            fontWeight = if (selectedCategory == category.id) FontWeight.SemiBold else FontWeight.Normal
                        )
                    }
                }
            }
        }
        Spacer(modifier = Modifier.height(24.dp))
        if (selectedCategory == animeStr) {
            if (animeHistoryItems.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(animeHistoryItems) { item ->
                        ContinueWatchingCardShared(item = item) {
                            onAnimeClick(item.id)
                        }
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Trending Anime
            if (uiState.trendingAnime.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.trending_anime), onSeeAllClick = onNavigateToTrending)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.trendingAnime) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
                                selectedMediaId = series.id
                                selectedMediaTitle = series.title
                                selectedMediaPoster = series.posterUrl
                                showBottomSheet = true
                            }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // New Releases
            if (uiState.newEpisodes.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.newEpisodes) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rank = null,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
                                selectedMediaId = series.id
                                selectedMediaTitle = series.title
                                selectedMediaPoster = series.posterUrl
                                showBottomSheet = true
                            }
                        )
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }

            // Popular Anime
            SectionTitleShared(stringResource(R.string.popular_anime), onSeeAllClick = onNavigateToPopular)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.series) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = index + 1,
                        rating = series.rating,
                        year = "2024",
                        isMovie = false,
                        mediaId = series.id,
                        onClick = { onAnimeClick(series.id) },
                        onLongClick = { 
                            selectedMediaId = series.id
                            selectedMediaTitle = series.title
                            selectedMediaPoster = series.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))

            // Coming Soon Anime
            if (uiState.upcomingAnime.isNotEmpty()) {
                SectionTitleShared(stringResource(R.string.coming_soon), onSeeAllClick = onNavigateToUpcoming)
                LazyRow(
                    contentPadding = PaddingValues(horizontal = 16.dp),
                    horizontalArrangement = Arrangement.spacedBy(16.dp)
                ) {
                    items(uiState.upcomingAnime) { series ->
                        MediaCard(
                            title = series.title,
                            posterUrl = series.posterUrl,
                            rating = series.rating,
                            year = series.firstAirDate?.take(4) ?: "2024",
                            isMovie = false,
                            mediaId = series.id,
                            onClick = { onAnimeClick(series.id) },
                            onLongClick = { 
                                selectedMediaId = series.id
                                selectedMediaTitle = series.title
                                selectedMediaPoster = series.posterUrl
                                showBottomSheet = true
                            },
                            modifier = Modifier.width(140.dp)
                        )
                    }
                }
                Spacer(modifier = Modifier.height(24.dp))
            }
        } else {
            val displayItems = when (selectedCategory) {
                "New Releases" -> uiState.series.reversed()
                "Top Rated" -> uiState.series.sortedByDescending { it.rating }
                "Genres" -> uiState.series.shuffled()
                else -> uiState.series
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = null,
                    rating = series.rating,
                    year = series.firstAirDate?.take(4) ?: "2024",
                    isMovie = false,
                    mediaId = series.id,
                    onClick = { onAnimeClick(series.id) },
                    onLongClick = { 
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }
    }
    }
if (showBottomSheet) {
            MediaActionBottomSheet(
                isMovie = false,
                onDismissRequest = { showBottomSheet = false },
                onDownloadStart = { quality ->
                    scope.launch {
                        downloadRepository.addToDownloads(DownloadItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = false,
                            quality = quality
                        ))
                        Toast.makeText(context, "Download Started", Toast.LENGTH_SHORT).show()
                    }
                },
                onAddToLibrary = {
                    scope.launch {
                        libraryRepository.addToLibrary(LibraryItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = false
                        ))
                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                    }
                }
            )
        }
    }
