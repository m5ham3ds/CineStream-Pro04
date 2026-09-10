package com.example.ui.screens.home

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
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.foundation.pager.*
import kotlinx.coroutines.delay
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Add
import androidx.compose.material.icons.filled.PlayArrow
import androidx.compose.material3.*

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState

import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.domain.models.Movie
import com.example.ui.ViewModelFactory
import com.example.ui.components.MediaActionBottomSheet

import androidx.compose.ui.platform.LocalContext
import com.example.data.repository.HistoryRepository
import androidx.compose.runtime.collectAsState

import com.example.ui.components.MediaCard
import com.example.ui.components.VerticalGrid
import com.example.ui.components.MediaScreenSkeleton
import com.example.ui.components.HeroCarousel
import com.example.ui.components.HeroItem
import com.example.ui.components.ContinueWatchingCardShared
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun HomeScreen(
    onMovieClick: (String) -> Unit,
    onSeriesClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    onNavigateToUpcoming: () -> Unit = {},
    onNavigateToAnime: () -> Unit = {},
    viewModel: HomeViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val historyRepository = remember { HistoryRepository(context) }
    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val libraryRepository = remember { LibraryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }
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
    var bottomSheetIsMovie by remember { mutableStateOf(true) }
    var selectedMediaId by remember { mutableStateOf("") }
    var selectedMediaTitle by remember { mutableStateOf("") }
    var selectedMediaPoster by remember { mutableStateOf("") }

    var selectedCategory by remember { mutableStateOf("Home") }
    val categories = listOf("Home", "Movies", "Series", stringResource(R.string.anime), "Documentaries")
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
             // Leave space for bottom nav
    ) {
        // Hero Section
        if (uiState.trendingMovies.isNotEmpty()) {
            HeroCarousel(items = uiState.trendingMovies.take(5).map { HeroItem(it.id, it.title, it.backdropUrl, true) }, onClick = onMovieClick)
        }


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
                        .background(if (selectedCategory == category) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface)
                        .border(
                            width = 1.dp,
                            color = if (selectedCategory == category) Color.Transparent else Color.DarkGray,
                            shape = RoundedCornerShape(8.dp)
                        )
                        .clickable {
                            if (selectedCategory == category) {
                                selectedCategory = "Home"
                            } else {
                                selectedCategory = category
                            }
                        }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Text(
                        text = category,
                        color = MaterialTheme.colorScheme.onBackground,
                        fontSize = 14.sp,
                        fontWeight = if (selectedCategory == category) FontWeight.SemiBold else FontWeight.Normal
                    )
                }
            }
        }


        Spacer(modifier = Modifier.height(24.dp))

        
        if (selectedCategory == "Home") {
// Trending Now
        SectionTitle(stringResource(R.string.trending_now), onSeeAllClick = onNavigateToTrending)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.trendingMovies) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = index + 1,
                    rating = 8.0 + (index * 0.1),
                    year = "2024",
                    mediaId = movie.id,
                            onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        bottomSheetIsMovie = true
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))
        
        // Continue Watching
        if (historyItems.isNotEmpty()) {
            SectionTitle(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(historyItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        if (item.isMovie) onMovieClick(item.id) else onSeriesClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // Trending Series
        SectionTitle(stringResource(R.string.trending_series), onSeeAllClick = onNavigateToTrending)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.trendingSeries) { index, series ->
                MediaCard(
                    title = series.title,
                    posterUrl = series.posterUrl,
                    rank = index + 1,
                    rating = 8.5 + (index * 0.1),
                    year = "${series.seasons.size} Seasons",
                    isMovie = false,
                    mediaId = series.id,
                            onClick = { onSeriesClick(series.id) },
                    onLongClick = { 
                        bottomSheetIsMovie = false
                        selectedMediaId = series.id
                        selectedMediaTitle = series.title
                        selectedMediaPoster = series.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }


        Spacer(modifier = Modifier.height(24.dp))
        
        // Anime
        if (uiState.animeSeries.isNotEmpty()) {
            SectionTitle(stringResource(R.string.anime), onSeeAllClick = onNavigateToAnime)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.animeSeries) { index, series ->
                    MediaCard(
                        title = series.title,
                        posterUrl = series.posterUrl,
                        rank = 0,
                        rating = series.rating,
                        year = series.year.toString(),
                        isMovie = false,
                        mediaId = series.id,
                            onClick = { onSeriesClick(series.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
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

        // Coming Soon
        if (uiState.upcomingMovies.isNotEmpty()) {
            SectionTitle(stringResource(R.string.coming_soon), onSeeAllClick = onNavigateToUpcoming)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                itemsIndexed(uiState.upcomingMovies) { index, movie ->
                    MediaCard(
                        title = movie.title,
                        posterUrl = movie.posterUrl,
                        rank = 0,
                        rating = movie.rating,
                        year = movie.year.toString(),
                        mediaId = movie.id,
                            onClick = { onMovieClick(movie.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = movie.id
                            selectedMediaTitle = movie.title
                            selectedMediaPoster = movie.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

        // New Releases
        if (uiState.newReleasesMovies.isNotEmpty()) {
            SectionTitle(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                val mix = (uiState.newReleasesMovies.take(10) + uiState.newReleasesSeries.map { 
                    Movie(id = it.id, title = it.title, overview = it.overview, posterUrl = it.posterUrl, backdropUrl = it.backdropUrl, year = it.year, rating = it.rating, genres = it.genres, runtime = 0)
                }.take(10)).shuffled()
                itemsIndexed(mix) { index, item ->
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = 0,
                        rating = item.rating,
                        year = item.year.toString(),
                        onClick = { onMovieClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }

} else {
            val displayItems = when (selectedCategory) {
                "Movies" -> uiState.allMovies
                "Series" -> uiState.allSeries
                stringResource(R.string.anime) -> uiState.animeSeries
                "Documentaries" -> uiState.allMovies.filter { it.genres.contains("Documentary") }
                else -> emptyList()
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { item ->
                // Because displayItems can be Movie or Series, we need to handle both
                // We'll just cast check since Kotlin supports it
                if (item is com.example.domain.models.Movie) {
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = null,
                        rating = item.rating,
                        year = item.year.toString(),
                        isMovie = true,
                        mediaId = item.id,
                        onClick = { onMovieClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = true
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                } else if (item is com.example.domain.models.Series) {
                    MediaCard(
                        title = item.title,
                        posterUrl = item.posterUrl,
                        rank = null,
                        rating = item.rating,
                        year = item.year.toString(),
                        isMovie = false,
                        mediaId = item.id,
                        onClick = { onSeriesClick(item.id) },
                        onLongClick = { 
                            bottomSheetIsMovie = false
                            selectedMediaId = item.id
                            selectedMediaTitle = item.title
                            selectedMediaPoster = item.posterUrl
                            showBottomSheet = true
                        }
                    )
                }
            }
        }
    }
if (showBottomSheet) {
            MediaActionBottomSheet(
                isMovie = bottomSheetIsMovie,
                onDismissRequest = { showBottomSheet = false },
                onDownloadStart = { quality ->
                    scope.launch {
                        downloadRepository.addToDownloads(DownloadItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = bottomSheetIsMovie,
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
                            isMovie = bottomSheetIsMovie
                        ))
                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                    }
                }
            )
        }
    }
}



@Composable
fun SectionTitle(title: String, onSeeAllClick: (() -> Unit)? = null) {
    Row(
        modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp, vertical = 12.dp),
        horizontalArrangement = Arrangement.SpaceBetween,
        verticalAlignment = Alignment.CenterVertically
    ) {
        Text(
            text = title,
            style = MaterialTheme.typography.titleMedium,
            fontWeight = FontWeight.Bold,
            color = MaterialTheme.colorScheme.onBackground
        )
        if (onSeeAllClick != null) {
            Text(
                text = stringResource(R.string.see_all),
                style = MaterialTheme.typography.labelLarge,
                color = MaterialTheme.colorScheme.primary,
                modifier = Modifier.clickable { onSeeAllClick() }
            )
        }
    }
}
