@file:OptIn(androidx.compose.foundation.ExperimentalFoundationApi::class)
package com.example.ui.screens.details

import androidx.compose.animation.core.animateFloat
import androidx.compose.animation.core.infiniteRepeatable
import androidx.compose.animation.core.tween
import androidx.compose.animation.core.LinearEasing
import androidx.compose.animation.core.RepeatMode
import androidx.compose.ui.draw.clipToBounds
import androidx.compose.ui.unit.dp

import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowLeft
import androidx.compose.material.icons.automirrored.filled.Send
import androidx.compose.material.icons.automirrored.filled.HelpOutline
import androidx.compose.material.icons.automirrored.outlined.ArrowBack
import com.example.utils.SiteVerificationManager
import androidx.compose.ui.res.stringResource
import com.example.R

import android.content.Intent
import android.net.Uri
import android.widget.Toast
import androidx.compose.foundation.background
import androidx.compose.foundation.clickable
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.ExperimentalFoundationApi
import androidx.compose.foundation.combinedClickable
import androidx.compose.foundation.lazy.LazyRow
import androidx.compose.foundation.lazy.items
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.shape.CircleShape
import androidx.compose.foundation.shape.RoundedCornerShape
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.*
import androidx.compose.material3.*

import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.pulltorefresh.PullToRefreshBox
import androidx.compose.material3.pulltorefresh.rememberPullToRefreshState

import androidx.compose.runtime.*
import com.example.ui.screens.player.ServerSelectionDialog
import com.example.extensions.ExtensionManager
import com.example.ui.screens.extensions.NoExtensionsDialog
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.draw.clip
import androidx.compose.ui.graphics.Brush
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.layout.ContentScale
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.text.style.TextOverflow
import androidx.compose.ui.unit.dp
import androidx.compose.ui.unit.sp
import androidx.lifecycle.viewmodel.compose.viewModel
import coil.compose.AsyncImage
import com.example.data.model.DownloadItem
import com.example.data.model.LibraryItem
import com.example.data.repository.DownloadRepository
import com.example.data.repository.LibraryRepository
import com.example.domain.models.CastMember
import com.example.domain.models.Episode
import com.example.domain.models.Season
import com.example.domain.models.VideoTrailer
import com.example.ui.ViewModelFactory
import kotlinx.coroutines.launch
import java.net.URLEncoder

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun MovieDetailsScreen(
    onPersonClick: (String) -> Unit = {},
    movieId: String, 
    onBack: () -> Unit,
    onPlay: (String, String, String?, String?, String) -> Unit,
    onNavigateToExtensions: () -> Unit = {},
    viewModel: MovieDetailsViewModel = viewModel(factory = ViewModelFactory())
) {
    val uiState by viewModel.uiState.collectAsState()
    val context = LocalContext.current
    val downloadRepository = remember { DownloadRepository(context) }
    val libraryRepository = remember { LibraryRepository(context) }
    val scope = rememberCoroutineScope()
    val libraryItems by libraryRepository.getLibraryItems().collectAsState(initial = emptyList())
    val downloadItems by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    
    val isFavorite = libraryItems.any { it.id == movieId }
    val downloadItem = downloadItems.find { it.id == movieId }
    var showDeleteConfirm by remember { mutableStateOf(false) }
    var showNotReleasedDialog by remember { mutableStateOf(false) }

    LaunchedEffect(movieId) {
        viewModel.loadMovie(movieId)
    }

    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(1200) // matches slide transition and ensures full skeleton cycle
        transitionFinished = true
    }

    Scaffold(
        containerColor = MaterialTheme.colorScheme.background
    ) { padding ->
        if (uiState.isLoading || !transitionFinished || uiState.movie == null) {
            DetailsSkeleton()
        } else if (uiState.movie != null) {
            val movie = uiState.movie!!
            val ctx = LocalContext.current
            val historyRepository = remember { com.example.data.repository.HistoryRepository(ctx) }
            var showSourceSheet by remember { mutableStateOf(false) }
    var showNoExtensionsDialog by remember { mutableStateOf(false) }
            var isDownloadMode by remember { mutableStateOf(false) }
            var selectedTrailerId by remember { mutableStateOf<String?>(null) }

            val ptrState = rememberPullToRefreshState()
            PullToRefreshBox(
                isRefreshing = uiState.isLoading,
                onRefresh = { viewModel.loadMovie(movieId) },
                state = ptrState,
                modifier = Modifier.fillMaxSize().padding(bottom = padding.calculateBottomPadding())
            ) {
            Column(
                modifier = Modifier
                    .fillMaxSize()
                    .verticalScroll(rememberScrollState())
            ) {
                
                if (showDeleteConfirm) {
                    AlertDialog(
                        onDismissRequest = { showDeleteConfirm = false },
                        title = { Text(stringResource(R.string.delete_download), color = MaterialTheme.colorScheme.onBackground) },
                        text = { Text(stringResource(R.string.delete_download_confirm), color = MaterialTheme.colorScheme.onSurfaceVariant) },
                        confirmButton = {
                            TextButton(onClick = {
                                downloadItem?.let {
                                    scope.launch { downloadRepository.removeFromDownloads(it) }
                                }
                                showDeleteConfirm = false
                            }) { Text(stringResource(R.string.yes_delete), color = Color.Red) }
                        },
                        dismissButton = {
                            TextButton(onClick = { showDeleteConfirm = false }) { Text(stringResource(R.string.cancel), color = MaterialTheme.colorScheme.onBackground) }
                        },
                        containerColor = MaterialTheme.colorScheme.surface
                    )
                }
                
                
    if (showNotReleasedDialog) {
        AlertDialog(
            onDismissRequest = { showNotReleasedDialog = false },
            title = { Text(stringResource(R.string.coming_soon), color = MaterialTheme.colorScheme.onBackground) },
            text = { Text(stringResource(R.string.not_released_yet), color = MaterialTheme.colorScheme.onSurfaceVariant) },
            confirmButton = {
                TextButton(onClick = { showNotReleasedDialog = false }) { Text(stringResource(R.string.ok_button)) }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    }

    // Hero Image or Video Player

                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                        Text(text = movie.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${movie.year} • ${movie.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Star, contentDescription = stringResource(R.string.rating_r), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(String.format("%.1f", movie.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                            }
                            Badge(containerColor = MaterialTheme.colorScheme.surfaceVariant) { Text("18+", color = MaterialTheme.colorScheme.onBackground) }
                        }
                    }
                } else {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
                        AsyncImage(
                            model = movie.posterUrl.takeIf { it.isNotBlank() } ?: movie.backdropUrl,
                            contentDescription = movie.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(modifier = Modifier.fillMaxSize().background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background.copy(alpha=0.6f), MaterialTheme.colorScheme.background),
                                startY = 0f
                            )
                        ))
                        Column(
                            modifier = Modifier.align(Alignment.BottomStart).padding(16.dp)
                        ) {
                            Text(text = movie.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("${movie.year} • ${movie.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Star, contentDescription = stringResource(R.string.rating_r), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text(String.format("%.1f", movie.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = MaterialTheme.colorScheme.surfaceVariant) { Text("18+", color = MaterialTheme.colorScheme.onBackground) } // Placeholder for age rating
                            }
                        }
                    }
                }
                
                // Action Buttons
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Button(
                        onClick = { 
                            if (downloadItem?.isCompleted == true) {
                                onPlay(movie.title, "local_offline_file://${downloadItem.id}", null, null, movie.posterUrl)
                            } else {
                                val isReleased = (movie.releaseDate ?: "") <= java.time.LocalDate.now().toString()
                                if (!isReleased) {
                                    showNotReleasedDialog = true
                                } else {
                                    isDownloadMode = false
                                    if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                        showNoExtensionsDialog = true
                                    } else {
                                        showSourceSheet = true
                                    }
                                }
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = stringResource(R.string.play_now), tint = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(if (downloadItem?.isCompleted == true) "Resume Offline" else "Resume", color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                    }
                                        Box(
                        contentAlignment = Alignment.Center,
                        modifier = Modifier
                            .size(50.dp)
                            .background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                            .clip(CircleShape)
                            .combinedClickable(
                                onClick = { 
                                    if (downloadItem?.isCompleted == true) {
                                        Toast.makeText(context, "Already downloaded", Toast.LENGTH_SHORT).show()
                                    } else if (downloadItem != null) {
                                        val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                            action = if (downloadItem.isPaused) "RESUME" else "PAUSE"
                                            putExtra("id", movie.id.toString())
                                        }
                                        context.startService(intent)
                                        scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                        Toast.makeText(context, if (downloadItem.isPaused) "Resumed" else "Paused", Toast.LENGTH_SHORT).show()
                                    } else {
                                        isDownloadMode = true
                                        if (ExtensionManager.installedExtensions.value.isEmpty()) {
                                            showNoExtensionsDialog = true
                                        } else {
                                            showSourceSheet = true
                                        }
                                    }
                                },
                                onLongClick = {
                                    if (downloadItem != null && !downloadItem.isCompleted) {
                                        showDeleteConfirm = true
                                    }
                                }
                            )
                    ) {
                        if (downloadItem?.isCompleted == true) {
                            Icon(Icons.Default.Check, contentDescription = stringResource(R.string.completed), tint = MaterialTheme.colorScheme.primary)
                        } else if (downloadItem != null) {
                            AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
                        } else {
                            Icon(Icons.Default.Download, contentDescription = stringResource(R.string.downloads), tint = MaterialTheme.colorScheme.onBackground)
                        }
                    }
                    IconButton(
                        onClick = { 
                            scope.launch {
                                val item = LibraryItem(id = movie.id, title = movie.originalTitle ?: movie.title, posterUrl = movie.posterUrl, isMovie = true)
                                if (isFavorite) libraryRepository.removeFromLibrary(item)
                                else libraryRepository.addToLibrary(item)
                            }
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        Icon(if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder, contentDescription = stringResource(R.string.add_to_library_favorites), tint = MaterialTheme.colorScheme.onBackground)
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Trailers
                if (movie.trailers.isNotEmpty()) {
                    Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(movie.trailers) { trailer ->
                            TrailerCard(trailer) {
                                selectedTrailerId = trailer.key
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
                
                // Overview
                Text(stringResource(R.string.overview), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text(movie.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(horizontal = 16.dp))
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Cast
                if (movie.cast.isNotEmpty()) {
                    Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        items(movie.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
            }

            }
            if (showNoExtensionsDialog) {
                NoExtensionsDialog(
                    onDismiss = { showNoExtensionsDialog = false },
                    onGoToExtensions = { 
                        onNavigateToExtensions()
                    },
                    onRetry = {
                        if (ExtensionManager.installedExtensions.value.isNotEmpty()) {
                            showNoExtensionsDialog = false
                            showSourceSheet = true
                        }
                    }
                )
            }
            if (showSourceSheet) {
                ServerSelectionDialog(
                    title = movie.originalTitle ?: movie.title,
                    year = movie.year.toString(),
                    isMovie = true,
                    isAnime = movie.genres.any { it.contains("Animation", ignoreCase = true) || it.contains("Anime", ignoreCase = true) },
                    isDownloadMode = isDownloadMode,
                    onDismiss = { showSourceSheet = false },
                    onNavigateToExtensions = onNavigateToExtensions,
                    onPlay = { url, serverName, website ->
                        showSourceSheet = false
                        if (isDownloadMode) {
                            scope.launch {
                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = movie.id, mediaId = movie.id, title = movie.originalTitle ?: movie.title, posterUrl = movie.posterUrl, isMovie = true, quality = "$serverName||$url"
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, movie.id.toString(), "${movie.title} - $serverName")
                            }
                        } else {
                            scope.launch {
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = movie.id,
                                        title = movie.originalTitle ?: movie.title,
                                        posterUrl = movie.posterUrl,
                                        isMovie = true
                                    )
                                )
                                onPlay(movie.title, url, serverName, website, movie.posterUrl)
                            }
                        }
                    }
                )
            }

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = padding.calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(MaterialTheme.colorScheme.background.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back), tint = MaterialTheme.colorScheme.onBackground)
            }

    }
}
}

@Composable
fun SeriesDetailsScreen(
    onPersonClick: (String) -> Unit = {},
    seriesId: String,
    onBack: () -> Unit,
    onPlay: (String, String, String?, String?, String) -> Unit,
    onNavigateToExtensions: () -> Unit = {}
) {
    val context = LocalContext.current
    val viewModel: SeriesDetailsViewModel = viewModel(factory = ViewModelFactory())
    val uiState by viewModel.uiState.collectAsState()
    val scope = rememberCoroutineScope()
    val libraryRepository = remember { LibraryRepository(context) }
    val isFavorite by libraryRepository.isItemInLibrary(seriesId).collectAsState(initial = false)
    val downloadRepository = remember { DownloadRepository(context) }
    val downloads by downloadRepository.getDownloadItems().collectAsState(initial = emptyList())
    val downloadedEpisodeIds = downloads.map { it.id }.toSet()
    val historyRepository = remember { com.example.data.repository.HistoryRepository(context) }
    val watchedRepo = remember { com.example.data.repository.WatchedEpisodeRepository(context) }
    val watchedEpisodes by watchedRepo.getAllWatched().collectAsState(initial = emptyList())
    val watchedEpisodeIds = watchedEpisodes.map { it.id }.toSet()

    var selectedEpisodeForSource by remember { mutableStateOf<Episode?>(null) }
    var isDownloadMode by remember { mutableStateOf(false) }
    var showBatchDownloadSheet by remember { mutableStateOf(false) }
    var showNotReleasedDialog by remember { mutableStateOf(false) }
    var selectedTrailerId by remember { mutableStateOf<String?>(null) }

    LaunchedEffect(seriesId) {
        viewModel.loadSeries(seriesId)
    }

    var transitionFinished by remember { androidx.compose.runtime.mutableStateOf(false) }
    androidx.compose.runtime.LaunchedEffect(Unit) {
        kotlinx.coroutines.delay(1200) // matches slide transition and ensures full skeleton cycle
        transitionFinished = true
    }

    val pullRefreshState = rememberPullToRefreshState()
    PullToRefreshBox(
        isRefreshing = uiState.isLoading,
        onRefresh = { viewModel.loadSeries(seriesId) },
        state = pullRefreshState
    ) {
        val series = uiState.series
        if ((uiState.isLoading || !transitionFinished) && series == null) {
            DetailsSkeleton()
            return@PullToRefreshBox
        }
        if (series == null && !uiState.isLoading) {
            Box(modifier = Modifier.fillMaxSize(), contentAlignment = Alignment.Center) {
                Text(uiState.error ?: "Failed to load details", color = MaterialTheme.colorScheme.error)
            }
            return@PullToRefreshBox
        }
        if (series != null) {
            val listState = androidx.compose.foundation.lazy.rememberLazyListState()
        val isScrollNearBottom by remember {
            derivedStateOf {
                val layoutInfo = listState.layoutInfo
                val totalItems = layoutInfo.totalItemsCount
                val lastVisibleItemIndex = layoutInfo.visibleItemsInfo.lastOrNull()?.index ?: 0
                totalItems > 0 && lastVisibleItemIndex >= totalItems - 2
            }
        }
    
    LaunchedEffect(isScrollNearBottom) {
        if (isScrollNearBottom) {
            if (uiState.episodes.isEmpty() && !uiState.isEpisodesLoading) {
                viewModel.triggerInitialEpisodesLoad()
            } else if (uiState.episodes.size > uiState.visibleEpisodesCount && !uiState.isLoadingMore) {
                viewModel.loadMoreEpisodes(context)
            }
        }
    }
            androidx.compose.foundation.lazy.LazyColumn(
                modifier = Modifier.fillMaxSize(),
                state = listState
            ) {
                item {
                val firstUnplayedEpisode = uiState.episodes.firstOrNull { !watchedEpisodeIds.contains(it.id) } ?: uiState.episodes.firstOrNull()

                
    if (showNotReleasedDialog) {
        AlertDialog(
            onDismissRequest = { showNotReleasedDialog = false },
            title = { Text(stringResource(R.string.coming_soon), color = MaterialTheme.colorScheme.onBackground) },
            text = { Text(stringResource(R.string.not_released_yet), color = MaterialTheme.colorScheme.onSurfaceVariant) },
            confirmButton = {
                TextButton(onClick = { showNotReleasedDialog = false }) { Text(stringResource(R.string.ok_button)) }
            },
            containerColor = MaterialTheme.colorScheme.surface
        )
    }

    // Hero Image or Video Player
                if (selectedTrailerId != null) {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(16f/9f)) {
                        com.example.ui.components.InlineYouTubePlayer(
                            videoId = selectedTrailerId!!,
                            modifier = Modifier.fillMaxSize()
                        )
                    }
                    Spacer(modifier = Modifier.height(16.dp))
                    Column(modifier = Modifier.padding(horizontal = 16.dp)) {
                        Text(text = series.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically) {
                            Text("${series.year} • ${series.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                        }
                        Spacer(modifier = Modifier.height(8.dp))
                        
                        Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Icon(Icons.Default.Star, contentDescription = stringResource(R.string.rating_r), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                                Spacer(modifier = Modifier.width(4.dp))
                                Text(String.format("%.1f", series.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                            }
                            Badge(containerColor = MaterialTheme.colorScheme.surfaceVariant) { Text("18+", color = MaterialTheme.colorScheme.onBackground) }
                        }
                    }
                } else {
                    Box(modifier = Modifier.fillMaxWidth().aspectRatio(0.8f)) {
                        AsyncImage(
                            model = series.posterUrl.takeIf { it.isNotBlank() } ?: series.backdropUrl,
                            contentDescription = series.title,
                            contentScale = ContentScale.Crop,
                            modifier = Modifier.fillMaxSize()
                        )
                        Box(modifier = Modifier.fillMaxSize().background(
                            Brush.verticalGradient(
                                colors = listOf(Color.Transparent, MaterialTheme.colorScheme.background.copy(alpha=0.6f), MaterialTheme.colorScheme.background),
                                startY = 0f
                            )
                        ))
                        Column(
                            modifier = Modifier.align(Alignment.BottomStart).padding(16.dp)
                        ) {
                            Text(text = series.title, style = MaterialTheme.typography.displaySmall, fontWeight = FontWeight.Bold, color = MaterialTheme.colorScheme.onBackground)
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically) {
                                Text("${series.year} • ${series.genres.take(3).joinToString(" • ")}", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium)
                            }
                            Spacer(modifier = Modifier.height(8.dp))
                            
                            Row(verticalAlignment = Alignment.CenterVertically, horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                                Row(verticalAlignment = Alignment.CenterVertically) {
                                    Icon(Icons.Default.Star, contentDescription = stringResource(R.string.rating_r), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(18.dp))
                                    Spacer(modifier = Modifier.width(4.dp))
                                    Text(String.format("%.1f", series.rating), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = MaterialTheme.colorScheme.surfaceVariant) { Text("18+", color = MaterialTheme.colorScheme.onBackground) } // Placeholder for age rating
                            }
                        }
                    }
                }
                
                // Action Buttons
                Row(modifier = Modifier.fillMaxWidth().padding(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp), verticalAlignment = Alignment.CenterVertically) {
                    Button(
                        onClick = {
                            val isReleased = (series.firstAirDate ?: "") <= java.time.LocalDate.now().toString()
                            if (!isReleased) {
                                showNotReleasedDialog = true
                            } else if (firstUnplayedEpisode != null) {
                                selectedEpisodeForSource = firstUnplayedEpisode
                                isDownloadMode = false
                            } else {
                                Toast.makeText(context, "No episodes available", Toast.LENGTH_SHORT).show()
                            }
                        },
                        modifier = Modifier.weight(1f).height(50.dp),
                        colors = ButtonDefaults.buttonColors(containerColor = MaterialTheme.colorScheme.primary)
                    ) {
                        Icon(Icons.Default.PlayArrow, contentDescription = stringResource(R.string.play_now), tint = MaterialTheme.colorScheme.onBackground)
                        Spacer(modifier = Modifier.width(8.dp))
                        Text(stringResource(R.string.play), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                    }
                    IconButton(
                        onClick = {
                            showBatchDownloadSheet = true
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        Icon(Icons.Default.Download, contentDescription = stringResource(R.string.downloads), tint = MaterialTheme.colorScheme.onBackground)
                    }
                    IconButton(
                        onClick = {
                            scope.launch {
                                val item = LibraryItem(id = series.id, title = series.originalTitle ?: series.title, posterUrl = series.posterUrl, isMovie = false)
                                if (isFavorite) libraryRepository.removeFromLibrary(item)
                                else libraryRepository.addToLibrary(item)
                            }
                        },
                        modifier = Modifier.size(50.dp).background(MaterialTheme.colorScheme.surfaceVariant, CircleShape)
                    ) {
                        Icon(if (isFavorite) Icons.Default.Bookmark else Icons.Default.BookmarkBorder, contentDescription = stringResource(R.string.add_to_library_favorites), tint = MaterialTheme.colorScheme.onBackground)
                    }
                }
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Trailers
                if (series.trailers.isNotEmpty()) {
                    Text(stringResource(R.string.trailers), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(12.dp)) {
                        items(series.trailers) { trailer ->
                            TrailerCard(trailer) {
                                selectedTrailerId = trailer.key
                            }
                        }
                    }
                    Spacer(modifier = Modifier.height(24.dp))
                }
                
                // Overview
                Text(stringResource(R.string.overview), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                Spacer(modifier = Modifier.height(8.dp))
                Text(series.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodyMedium, modifier = Modifier.padding(horizontal = 16.dp))
                
                Spacer(modifier = Modifier.height(24.dp))
                
                // Cast
                if (series.cast.isNotEmpty()) {
                    Text(stringResource(R.string.cast), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(16.dp)) {
                        items(series.cast) { CastMemberCard(it) { onPersonClick(it.id) } }
                    }
                    Spacer(modifier = Modifier.height(32.dp))
                }
                // Seasons & Episodes
                if (series.seasons.isNotEmpty()) {
                    Text(stringResource(R.string.seasons_and_episodes), color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.titleMedium, fontWeight = FontWeight.Bold, modifier = Modifier.padding(horizontal = 16.dp))
                    Spacer(modifier = Modifier.height(8.dp))
                    
                    // Season Tabs
                    LazyRow(contentPadding = PaddingValues(horizontal = 16.dp), horizontalArrangement = Arrangement.spacedBy(8.dp)) {
                        items(series.seasons.filter { it.seasonNumber > 0 }) { season ->
                            val isSelected = uiState.selectedSeason?.id == season.id
                            FilterChip(
                                selected = isSelected,
                                onClick = { viewModel.selectSeason(season) },
                                label = { Text(stringResource(R.string.season_number, season.seasonNumber)) },
                                colors = FilterChipDefaults.filterChipColors(
                                    selectedContainerColor = MaterialTheme.colorScheme.primary,
                                    selectedLabelColor = MaterialTheme.colorScheme.onBackground
                                )
                            )
                        }
                    }
                    Spacer(modifier = Modifier.height(16.dp))

                    // Episodes
                } // Close if block
                } // Close item block
                
                if (uiState.isEpisodesLoading) {
                    item { Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) { CircularProgressIndicator() } }
                } else {
                    items(uiState.episodes.take(uiState.visibleEpisodesCount)) { episode ->
                        val isWatched = watchedEpisodeIds.contains(episode.id)
                        val downloadItem = downloads.find { it.id == "${series.id}_${episode.id}" }
                        val isDownloaded = downloadItem?.isCompleted == true
                        EpisodeCard(
                            episode = episode,
                            isWatched = isWatched,
                            downloadItem = downloadItem,
                            onClick = {
                                if (isDownloaded) {
                                    scope.launch {
                                        val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${episode.episodeNumber}"
                                        historyRepository.addToHistory(
                                            com.example.data.model.HistoryItem(
                                                id = series.id.toString(), title = fullTitle, posterUrl = episode.thumbnailUrl, isMovie = false
                                            )
                                        )
                                        onPlay(fullTitle, "local_offline_file://${series.id}_${episode.id}", null, null, episode.thumbnailUrl)
                                    }
                                } else {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = false
                                }
                            },
                            onLongClick = {
                                scope.launch {
                                    if (isWatched) watchedRepo.markAsUnwatched(episode.id)
                                    else watchedRepo.markAsWatched(episode.id)
                                }
                            },
                            onLongDownloadClick = {
                                if (downloadItem != null && !downloadItem.isCompleted) {
                                    // we can reuse the same delete confirmation but we need a state for episode delete
                                    val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                        action = "CANCEL"
                                        putExtra("id", "${series.id}_${episode.id}")
                                    }
                                    context.startService(intent)
                                    scope.launch { downloadRepository.removeFromDownloads(downloadItem) }
                                    Toast.makeText(context, "Download cancelled", Toast.LENGTH_SHORT).show()
                                }
                            },
                            onDownloadClick = {
                                if (downloadItem?.isCompleted == true) {
                                    Toast.makeText(context, "Already downloaded", Toast.LENGTH_SHORT).show()
                                } else if (downloadItem != null) {
                                    val intent = android.content.Intent(context, com.example.utils.StreamDownloaderService::class.java).apply {
                                        action = if (downloadItem.isPaused) "RESUME" else "PAUSE"
                                        putExtra("id", "${series.id}_${episode.id}")
                                    }
                                    context.startService(intent)
                                    scope.launch { downloadRepository.updateDownload(downloadItem.copy(isPaused = !downloadItem.isPaused)) }
                                    Toast.makeText(context, if (downloadItem.isPaused) "Resumed" else "Paused", Toast.LENGTH_SHORT).show()
                                } else {
                                    selectedEpisodeForSource = episode
                                    isDownloadMode = true
                                    if (com.example.extensions.ExtensionManager.installedExtensions.value.isEmpty()) {
                                        // No extensions logic - would be handled by parent, but let's just trigger sheet which handles it
                                    }
                                }
                            }
                        )
                    }
                    
                    if (uiState.episodes.size > uiState.visibleEpisodesCount || uiState.isLoadingMore) {
                        item {
                            Box(modifier = Modifier.fillMaxWidth().padding(vertical = 24.dp), contentAlignment = Alignment.Center) {
                                if (uiState.isLoadingMore) {
                                    Row(verticalAlignment = Alignment.CenterVertically) {
                                        CircularProgressIndicator(modifier = Modifier.size(20.dp), strokeWidth = 2.dp)
                                        Spacer(modifier = Modifier.width(12.dp))
                                        Text(stringResource(R.string.loading_eps), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                                    }
                                } else {
                                    Text(stringResource(R.string.swipe_to_load), color = MaterialTheme.colorScheme.onSurfaceVariant, fontSize = 14.sp)
                                }
                            }
                        }
                    }
                }
                item { Spacer(modifier = Modifier.height(32.dp)) }
            }
            
            if (selectedEpisodeForSource != null) {
                ServerSelectionDialog(
                    title = series.originalTitle ?: series.title,
                    year = series.year.toString(),
                    isMovie = false,
                    season = uiState.selectedSeason?.seasonNumber ?: 1,
                    episode = selectedEpisodeForSource?.episodeNumber ?: 1,
                    isAnime = series.genres.any { it.contains("Animation", ignoreCase = true) || it.contains("Anime", ignoreCase = true) },
                    isDownloadMode = isDownloadMode,
                    onDismiss = { selectedEpisodeForSource = null },
                    onNavigateToExtensions = onNavigateToExtensions,
                    onPlay = { url, serverName, website ->
                        val ep = selectedEpisodeForSource!!
                        selectedEpisodeForSource = null
                        if (isDownloadMode) {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                val epIdStr = "${series.id}_${ep.id}"
                                downloadRepository.addToDownloads(com.example.data.model.DownloadItem(
                                    id = epIdStr, mediaId = series.id.toString(), title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false, quality = "$serverName||$url"
                                ))
                                com.example.utils.AndroidDownloader.downloadVideo(context, url, epIdStr, "$fullTitle - $serverName")
                            }
                        } else {
                            scope.launch {
                                val fullTitle = "${series.title} - S${uiState.selectedSeason?.seasonNumber}E${ep.episodeNumber}"
                                historyRepository.addToHistory(
                                    com.example.data.model.HistoryItem(
                                        id = series.id.toString(), title = fullTitle, posterUrl = ep.thumbnailUrl, isMovie = false
                                    )
                                )
                                onPlay(fullTitle, url, serverName, website, ep.thumbnailUrl)
                            }
                        }
                    }
                )
            }

            if (showBatchDownloadSheet) {
                com.example.ui.components.BatchDownloadSheet(
                    series = series,
                    currentSeason = uiState.selectedSeason,
                    episodes = uiState.episodes,
                    onDismiss = { showBatchDownloadSheet = false }
                )
            }

            IconButton(
                onClick = onBack,
                modifier = Modifier
                    .padding(top = WindowInsets.statusBars.asPaddingValues().calculateTopPadding() + 8.dp, start = 16.dp)
                    .background(MaterialTheme.colorScheme.background.copy(alpha=0.3f), CircleShape)
            ) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = stringResource(R.string.back), tint = MaterialTheme.colorScheme.onBackground)
            }
        }
    }
}

@Composable
fun TrailerCard(trailer: VideoTrailer, onClick: () -> Unit) {
    Box(
        modifier = Modifier
            .width(200.dp)
            .aspectRatio(16f/9f)
            .clip(RoundedCornerShape(8.dp))
            .clickable { onClick() }
    ) {
        AsyncImage(
            model = "https://img.youtube.com/vi/${trailer.key}/hqdefault.jpg",
            contentDescription = trailer.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.fillMaxSize()
        )
        Box(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background.copy(alpha=0.3f)), contentAlignment = Alignment.Center) {
            Icon(Icons.Default.PlayArrow, contentDescription = stringResource(R.string.play_now), tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.size(48.dp))
        }
        Text(
            text = trailer.name,
            color = MaterialTheme.colorScheme.onBackground,
            style = MaterialTheme.typography.labelSmall,
            maxLines = 1,
            overflow = TextOverflow.Ellipsis,
            modifier = Modifier.align(Alignment.BottomStart).padding(8.dp)
        )
    }
}

@Composable
fun CastMemberCard(cast: CastMember, onClick: () -> Unit) {
    Column(horizontalAlignment = Alignment.CenterHorizontally, modifier = Modifier.width(80.dp).clickable { onClick() }) {
        AsyncImage(
            model = cast.profileUrl ?: "https://via.placeholder.com/150",
            contentDescription = cast.name,
            contentScale = ContentScale.Crop,
            modifier = Modifier.size(72.dp).clip(CircleShape).background(MaterialTheme.colorScheme.surfaceVariant)
        )
        Spacer(modifier = Modifier.height(8.dp))
        Text(cast.name, color = MaterialTheme.colorScheme.onBackground, style = MaterialTheme.typography.labelMedium, maxLines = 1, overflow = TextOverflow.Ellipsis)
        Text(cast.character, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall, maxLines = 1, overflow = TextOverflow.Ellipsis)
    }
}

@Composable
fun EpisodeCard(
    episode: Episode,
    isWatched: Boolean,
    downloadItem: com.example.data.model.DownloadItem? = null,
    onClick: () -> Unit,
    onLongClick: () -> Unit,
    onDownloadClick: () -> Unit,
    onLongDownloadClick: () -> Unit = {}
) {
    Row(
        modifier = Modifier
            .fillMaxWidth()
            .combinedClickable(
                onClick = onClick,
                onLongClick = onLongClick
            )
            .padding(horizontal = 16.dp, vertical = 8.dp),
        verticalAlignment = Alignment.CenterVertically
    ) {
        Box(
            modifier = Modifier.width(120.dp).aspectRatio(16f/9f).clip(RoundedCornerShape(8.dp))
        ) {
            AsyncImage(
                model = episode.thumbnailUrl,
                contentDescription = episode.title,
                contentScale = ContentScale.Crop,
                modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.surfaceVariant)
            )
            Icon(Icons.Default.PlayArrow, contentDescription = stringResource(R.string.play_now), tint = MaterialTheme.colorScheme.onBackground, modifier = Modifier.align(Alignment.Center))
        }
        Spacer(modifier = Modifier.width(16.dp))
        Column(modifier = Modifier.weight(1f)) {
            Text(
                text = "${episode.episodeNumber}. ${episode.title}",
                color = if (isWatched) MaterialTheme.colorScheme.onBackground.copy(alpha = 0.5f) else MaterialTheme.colorScheme.onBackground,
                style = MaterialTheme.typography.titleMedium,
                fontWeight = FontWeight.Bold,
                maxLines = 1,
                overflow = TextOverflow.Ellipsis
            )
            Spacer(modifier = Modifier.height(4.dp))
            Row(verticalAlignment = Alignment.CenterVertically) {
                Icon(Icons.Default.Star, contentDescription = stringResource(R.string.rating_r), tint = MaterialTheme.colorScheme.primary, modifier = Modifier.size(12.dp))
                Spacer(modifier = Modifier.width(4.dp))
                Text(String.format("%.1f", episode.rating), color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
                Spacer(modifier = Modifier.width(8.dp))
                Text("${episode.duration}m", color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.labelSmall)
            }
            Spacer(modifier = Modifier.height(4.dp))
            Text(episode.overview, color = MaterialTheme.colorScheme.onSurfaceVariant, style = MaterialTheme.typography.bodySmall, maxLines = 2, overflow = TextOverflow.Ellipsis)
        }
        Box(
            modifier = Modifier
                .size(48.dp)
                .clip(CircleShape)
                .combinedClickable(
                    onClick = onDownloadClick,
                    onLongClick = onLongDownloadClick
                ),
            contentAlignment = Alignment.Center
        ) {
            if (downloadItem?.isCompleted == true) {
                Icon(Icons.Default.Check, contentDescription = stringResource(R.string.completed), tint = MaterialTheme.colorScheme.primary)
            } else if (downloadItem != null) {
                AnimatedDownloadIcon(isPaused = downloadItem.isPaused)
            } else {
                Icon(Icons.Default.Download, contentDescription = stringResource(R.string.downloads), tint = MaterialTheme.colorScheme.onBackground)
    }
    }
    }
    }
@Composable
fun AnimatedDownloadIcon(isPaused: Boolean) {
    val infiniteTransition = androidx.compose.animation.core.rememberInfiniteTransition()
    val offset by infiniteTransition.animateFloat(
        initialValue = -5f,
        targetValue = 5f,
        animationSpec = androidx.compose.animation.core.infiniteRepeatable(
            animation = androidx.compose.animation.core.tween(800, easing = androidx.compose.animation.core.LinearEasing),
            repeatMode = androidx.compose.animation.core.RepeatMode.Restart
        )
    )
    
    androidx.compose.foundation.layout.Box(
        modifier = androidx.compose.ui.Modifier.size(24.dp).clipToBounds(), 
        contentAlignment = androidx.compose.ui.Alignment.Center
    ) {
        val tint = if (isPaused) androidx.compose.ui.graphics.Color.Gray.copy(alpha = 0.5f) else androidx.compose.material3.MaterialTheme.colorScheme.primary
        androidx.compose.material3.Icon(
            androidx.compose.material.icons.Icons.Default.ArrowDownward, 
            contentDescription = stringResource(R.string.downloading), 
            tint = tint, 
            modifier = if (isPaused) androidx.compose.ui.Modifier else androidx.compose.ui.Modifier.offset(y = offset.dp)
        )
    


}




}

