package com.example.ui.screens.player

import android.content.Context
import androidx.compose.ui.res.stringResource
import com.example.R
import androidx.compose.material3.MaterialTheme
import android.net.Uri
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.background
import androidx.compose.foundation.layout.*
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.ArrowBack
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.runtime.Composable
import androidx.compose.runtime.DisposableEffect
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.graphics.Color
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.unit.dp
import androidx.compose.ui.viewinterop.AndroidView
import androidx.media3.common.MediaItem
import androidx.media3.exoplayer.ExoPlayer
import androidx.media3.ui.PlayerView
import java.io.File

@Composable
fun TrailerScreen(trailerId: String, onBack: () -> Unit) {
    Column(modifier = Modifier.fillMaxSize().background(MaterialTheme.colorScheme.background)) {
        Row(modifier = Modifier.fillMaxWidth().padding(16.dp)) {
            IconButton(onClick = onBack) {
                Icon(Icons.AutoMirrored.Filled.ArrowBack, contentDescription = "Back", tint = MaterialTheme.colorScheme.onBackground)
            }
        }
        
        if (trailerId.startsWith("local_offline_file://")) {
            val fileId = trailerId.removePrefix("local_offline_file://")
            val context = LocalContext.current
            val file = File(context.filesDir, "downloads/$fileId.mp4")
            if (file.exists()) {
                ExoPlayerView(url = Uri.fromFile(file).toString())
            } else {
                Box(modifier = Modifier.fillMaxSize(), contentAlignment = androidx.compose.ui.Alignment.Center) {
                    androidx.compose.material3.Text(stringResource(R.string.file_not_found), color = MaterialTheme.colorScheme.onBackground)
                }
            }
        } else if (trailerId.startsWith("http://") || trailerId.startsWith("https://") && trailerId.contains(".mp4") || trailerId.contains(".m3u8")) {
            ExoPlayerView(url = trailerId)
        } else {
            AndroidView(
                modifier = Modifier.fillMaxSize(),
                factory = { context ->
                    val wasmDir = java.io.File(context.cacheDir, "WebView/Default/HTTP Cache/Code Cache/wasm")
                    if (!wasmDir.exists()) {
                        wasmDir.mkdirs()
                    }
                    
                    WebView(context).apply {
                        setLayerType(android.view.View.LAYER_TYPE_SOFTWARE, null)
                        settings.javaScriptEnabled = true
                        settings.domStorageEnabled = true
                        settings.mediaPlaybackRequiresUserGesture = false
                        webChromeClient = WebChromeClient()
                        webViewClient = WebViewClient()
                        val htmlData = """
                            <html>
                                <body style="margin:0;padding:0;background-color:black;display:flex;justify-content:center;align-items:center;">
                                    <iframe width="100%" height="100%" src="https://www.youtube.com/embed/$trailerId?autoplay=1&fs=1&modestbranding=1&rel=0" frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" allowfullscreen></iframe>
                                </body>
                            </html>
                        """.trimIndent()
                        loadData(htmlData, "text/html", "UTF-8")
                    }
                }
            )
        }
    }
}

@Composable
fun ExoPlayerView(url: String) {
    val context = LocalContext.current
    val exoPlayer = remember {
        ExoPlayer.Builder(context).build().apply {
            val mediaItem = MediaItem.fromUri(Uri.parse(url))
            setMediaItem(mediaItem)
            prepare()
            playWhenReady = true
        }
    }
    
    DisposableEffect(Unit) {
        onDispose {
            exoPlayer.release()
        }
    }
    
    AndroidView(
        factory = {
            PlayerView(context).apply {
                player = exoPlayer
            }
        },
        modifier = Modifier.fillMaxSize()
    )
}
