import re

new_code = """package com.example.ui.components

import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.content.pm.ActivityInfo
import android.view.View
import androidx.activity.compose.BackHandler
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView
import androidx.lifecycle.compose.LocalLifecycleOwner
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.YouTubePlayer
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.listeners.AbstractYouTubePlayerListener
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.listeners.FullscreenListener
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.options.IFramePlayerOptions
import com.pierfrancescosoffritti.androidyoutubeplayer.core.player.views.YouTubePlayerView

fun Context.findActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

@Composable
fun InlineYouTubePlayer(
    videoId: String,
    modifier: Modifier = Modifier,
    onFullscreenChange: (Boolean) -> Unit = {}
) {
    val context = LocalContext.current
    val lifecycleOwner = LocalLifecycleOwner.current
    var isFullScreen by remember { mutableStateOf(false) }
    var exitFullscreenAction by remember { mutableStateOf<(() -> Unit)?>(null) }
    var youtubePlayer by remember { mutableStateOf<YouTubePlayer?>(null) }

    LaunchedEffect(videoId, youtubePlayer) {
        youtubePlayer?.loadVideo(videoId, 0f)
    }

    BackHandler(enabled = isFullScreen) {
        exitFullscreenAction?.invoke()
    }

    Box(modifier = modifier) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                YouTubePlayerView(ctx).apply {
                    enableAutomaticInitialization = false
                    lifecycleOwner.lifecycle.addObserver(this)

                    addFullscreenListener(object : FullscreenListener {
                        override fun onEnterFullscreen(fullscreenView: View, exitFullscreen: () -> Unit) {
                            isFullScreen = true
                            exitFullscreenAction = exitFullscreen
                            onFullscreenChange(true)
                            try {
                                ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_SENSOR_LANDSCAPE
                            } catch (e: Exception) { }
                        }

                        override fun onExitFullscreen() {
                            isFullScreen = false
                            exitFullscreenAction = null
                            onFullscreenChange(false)
                            try {
                                ctx.findActivity()?.requestedOrientation = ActivityInfo.SCREEN_ORIENTATION_UNSPECIFIED
                            } catch (e: Exception) { }
                        }
                    })

                    val listener = object : AbstractYouTubePlayerListener() {
                        override fun onReady(player: YouTubePlayer) {
                            youtubePlayer = player
                        }
                    }

                    val options = IFramePlayerOptions.Builder()
                        .controls(1)
                        .fullscreen(1)
                        .build()

                    initialize(listener, options)
                }
            },
            onRelease = { 
                lifecycleOwner.lifecycle.removeObserver(it)
                it.release() 
            }
        )
    }
}
"""

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(new_code)
