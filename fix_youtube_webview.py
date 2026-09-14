import re

new_code = """package com.example.ui.components

import android.annotation.SuppressLint
import android.app.Activity
import android.content.Context
import android.content.ContextWrapper
import android.content.pm.ActivityInfo
import android.view.View
import android.view.ViewGroup
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.viewinterop.AndroidView

fun Context.findActivity(): Activity? = when (this) {
    is Activity -> this
    is ContextWrapper -> baseContext.findActivity()
    else -> null
}

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun InlineYouTubePlayer(
    videoId: String,
    modifier: Modifier = Modifier,
    onFullscreenChange: (Boolean) -> Unit = {}
) {
    val context = LocalContext.current
    val url = "https://www.youtube.com/embed/$videoId?autoplay=1&fs=1&rel=0"

    Box(modifier = modifier) {
        AndroidView(
            modifier = Modifier.fillMaxSize(),
            factory = { ctx ->
                WebView(ctx).apply {
                    layoutParams = ViewGroup.LayoutParams(
                        ViewGroup.LayoutParams.MATCH_PARENT,
                        ViewGroup.LayoutParams.MATCH_PARENT
                    )
                    settings.javaScriptEnabled = true
                    settings.domStorageEnabled = true
                    settings.mediaPlaybackRequiresUserGesture = false
                    webChromeClient = WebChromeClient()
                    webViewClient = WebViewClient()
                    setLayerType(View.LAYER_TYPE_HARDWARE, null)
                    loadUrl(url)
                }
            },
            update = { webView ->
                val currentUrl = "https://www.youtube.com/embed/$videoId?autoplay=1&fs=1&rel=0"
                if (webView.url != currentUrl) {
                    webView.loadUrl(currentUrl)
                }
            }
        )
    }
}
"""

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(new_code)

