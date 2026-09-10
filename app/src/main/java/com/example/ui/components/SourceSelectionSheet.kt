package com.example.ui.components

import androidx.compose.foundation.clickable
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.foundation.layout.*
import androidx.compose.foundation.lazy.LazyColumn
import androidx.compose.foundation.lazy.items
import androidx.compose.material3.*
import androidx.compose.runtime.*
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.text.font.FontWeight
import androidx.compose.ui.unit.dp
import com.example.domain.providers.ProviderManager
import com.example.domain.providers.VideoSource
import kotlinx.coroutines.launch

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SourceSelectionSheet(
    mediaId: String,
    mediaTitle: String = "Unknown",
    isMovie: Boolean,
    episodeId: String? = null,
    onDismiss: () -> Unit,
    onSourceSelected: (VideoSource) -> Unit
) {
    val scope = rememberCoroutineScope()
    var isLoading by remember { mutableStateOf(true) }
    var sources by remember { mutableStateOf<List<VideoSource>>(emptyList()) }

    LaunchedEffect(mediaId) {
        isLoading = true
        // Pass dummy episode ID if not a movie
        sources = ProviderManager.extractVideoLinks(mediaId, isMovie, episodeId)
        isLoading = false
    }

    ModalBottomSheet(onDismissRequest = onDismiss) {
        Column(
            modifier = Modifier
                .fillMaxWidth()
                .padding(16.dp)
        ) {
            Text(
                text = "Select Server & Quality",
                style = MaterialTheme.typography.titleLarge,
                fontWeight = FontWeight.Bold,
                modifier = Modifier.padding(bottom = 16.dp)
            )

            if (isLoading && sources.isEmpty()) {
                Box(modifier = Modifier.fillMaxWidth().padding(32.dp), contentAlignment = Alignment.Center) {
                    CircularProgressIndicator()
                }
            } else if (sources.isEmpty()) {
                Text(stringResource(R.string.no_sources), modifier = Modifier.padding(16.dp))
            } else {
                LazyColumn {
                    items(sources) { source ->
                        Card(
                            modifier = Modifier
                                .fillMaxWidth()
                                .padding(vertical = 4.dp)
                                .clickable { 
                                    onSourceSelected(source)
                                    onDismiss()
                                },
                            colors = CardDefaults.cardColors(containerColor = MaterialTheme.colorScheme.surfaceVariant)
                        ) {
                            Row(
                                modifier = Modifier.padding(16.dp),
                                horizontalArrangement = Arrangement.SpaceBetween,
                                verticalAlignment = Alignment.CenterVertically
                            ) {
                                Column {
                                    Text(text = source.providerName, fontWeight = FontWeight.Bold)
                                }
                                Badge(containerColor = MaterialTheme.colorScheme.primary) {
                                    Text(text = source.quality, modifier = Modifier.padding(horizontal = 4.dp, vertical = 2.dp))
                                }
                            }
                        }
                    }
                }
            }
            Spacer(modifier = Modifier.height(32.dp))
        }
    }
}
