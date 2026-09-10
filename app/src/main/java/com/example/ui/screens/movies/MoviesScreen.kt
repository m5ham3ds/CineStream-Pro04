package com.example.ui.screens.movies

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
fun MoviesScreen(
    onMovieClick: (String) -> Unit,
    onNavigateToTrending: () -> Unit = {},
    onNavigateToWatching: () -> Unit = {},
    onNavigateToPopular: () -> Unit = {},
    onNavigateToNewReleases: () -> Unit = {},
    viewModel: MoviesViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val libraryRepository = remember { LibraryRepository(context) }
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    val downloadRepository = remember { DownloadRepository(context) }

    val historyItems by historyRepository.getHistoryItems().collectAsState(initial = emptyList())
    val movieHistoryItems = historyItems.filter { it.isMovie }

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

    var selectedCategory by remember { mutableStateOf("Movies") }

    data class CategoryItem(val name: String, val icon: androidx.compose.ui.graphics.vector.ImageVector)
    val categories = listOf(
        CategoryItem("Movies", Icons.Default.LocalMovies),
        CategoryItem("Genres", Icons.Default.Category),
        CategoryItem(stringResource(R.string.new_releases), Icons.Default.NewReleases),
        CategoryItem("Top Rated", Icons.Default.Star)
    )
    val ptrState = rememberPullToRefreshState()
    
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadMovies() },
        state = ptrState,
        modifier = Modifier.fillMaxSize()
    ) {


    Column(
        modifier = Modifier
            .fillMaxSize()
            .verticalScroll(scrollState)
            
    ) {
        // Hero Section
        HeroCarousel(items = uiState.movies.take(5).map { HeroItem(it.id, it.title, it.backdropUrl, true) }, onClick = onMovieClick)


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
                        .background(if (selectedCategory == category.name) MaterialTheme.colorScheme.primary else MaterialTheme.colorScheme.surface)
                        .clickable {
                            if (selectedCategory == category.name) {
                                selectedCategory = "Movies"
                            } else {
                                selectedCategory = category.name
                            }
                        }
                        .padding(horizontal = 16.dp, vertical = 8.dp),
                    contentAlignment = Alignment.Center
                ) {
                    Row(verticalAlignment = Alignment.CenterVertically) {
                        Icon(
                            imageVector = category.icon, 
                            contentDescription = category.name, 
                            tint = if (selectedCategory == category.name) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant,
                            modifier = Modifier.size(16.dp)
                        )
                        Spacer(modifier = Modifier.width(6.dp))
                        Text(
                            text = category.name,
                            color = if (selectedCategory == category.name) MaterialTheme.colorScheme.onBackground else MaterialTheme.colorScheme.onSurfaceVariant,
                            fontSize = 14.sp,
                            fontWeight = if (selectedCategory == category.name) FontWeight.SemiBold else FontWeight.Normal
                        )
                    }
                }
            }
        }


        Spacer(modifier = Modifier.height(24.dp))
        
        
        if (selectedCategory == "Movies") {
if (movieHistoryItems.isNotEmpty()) {
            SectionTitleShared(stringResource(R.string.continue_watching), onSeeAllClick = onNavigateToWatching)
            LazyRow(
                contentPadding = PaddingValues(horizontal = 16.dp),
                horizontalArrangement = Arrangement.spacedBy(16.dp)
            ) {
                items(movieHistoryItems) { item ->
                    ContinueWatchingCardShared(item = item) {
                        onMovieClick(item.id)
                    }
                }
            }
            Spacer(modifier = Modifier.height(24.dp))
        }


        // Popular Movies
        SectionTitleShared(stringResource(R.string.popular_movies), onSeeAllClick = onNavigateToPopular)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.movies) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = index + 1,
                    rating = 8.7 - (index * 0.1),
                    year = "2024",
                    mediaId = movie.id,
                            onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

        Spacer(modifier = Modifier.height(24.dp))

        // New Releases
        SectionTitleShared(stringResource(R.string.new_releases), onSeeAllClick = onNavigateToNewReleases)
        LazyRow(
            contentPadding = PaddingValues(horizontal = 16.dp),
            horizontalArrangement = Arrangement.spacedBy(16.dp)
        ) {
            itemsIndexed(uiState.movies.reversed()) { index, movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = null, // No rank for new releases
                    rating = 8.5,
                    year = "2024",
                    mediaId = movie.id,
                            onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }

} else {
            val displayItems = when (selectedCategory) {
                stringResource(R.string.new_releases) -> uiState.movies.reversed()
                "Top Rated" -> uiState.movies.sortedByDescending { it.rating }
                "Genres" -> uiState.movies.shuffled() // Placeholder for genres
                else -> uiState.movies
            }
            
            com.example.ui.components.VerticalGrid(
                items = displayItems,
                columns = 3,
                modifier = Modifier.padding(horizontal = 16.dp)
            ) { movie ->
                MediaCard(
                    title = movie.title,
                    posterUrl = movie.posterUrl,
                    rank = null,
                    rating = movie.rating,
                    year = movie.year.toString(),
                    isMovie = true,
                    mediaId = movie.id,
                    onClick = { onMovieClick(movie.id) },
                    onLongClick = { 
                        selectedMediaId = movie.id
                        selectedMediaTitle = movie.title
                        selectedMediaPoster = movie.posterUrl
                        showBottomSheet = true
                    }
                )
            }
        }
    }
if (showBottomSheet) {
            MediaActionBottomSheet(
                isMovie = true,
                onDismissRequest = { showBottomSheet = false },
                onDownloadStart = { quality ->
                    scope.launch {
                        downloadRepository.addToDownloads(DownloadItem(
                            id = selectedMediaId,
                            title = selectedMediaTitle,
                            posterUrl = selectedMediaPoster,
                            isMovie = true,
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
                            isMovie = true
                        ))
                        Toast.makeText(context, "Added to Library", Toast.LENGTH_SHORT).show()
                    }
                }
            )
        }
    }
}
