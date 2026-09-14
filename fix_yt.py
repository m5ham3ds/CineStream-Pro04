import re

new_code = """package com.example.ui.components

import android.annotation.SuppressLint
import android.view.ViewGroup
import android.webkit.WebChromeClient
import android.webkit.WebView
import android.webkit.WebViewClient
import androidx.compose.foundation.layout.Box
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.viewinterop.AndroidView

@SuppressLint("SetJavaScriptEnabled")
@Composable
fun InlineYouTubePlayer(
    videoId: String,
    modifier: Modifier = Modifier,
    onFullscreenChange: (Boolean) -> Unit = {}
) {
    val htmlData = \"\"\"
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
            <style>
                body { margin: 0; padding: 0; background-color: #000000; overflow: hidden; }
                iframe { width: 100vw; height: 100vh; border: none; }
            </style>
        </head>
        <body>
            <iframe 
                src="https://www.youtube.com/embed/${videoId}?autoplay=1&fs=1&rel=0&enablejsapi=1&playsinline=1" 
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture" 
                allowfullscreen>
            </iframe>
        </body>
        </html>
    \"\"\".trimIndent()

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
                    webViewClient = object : WebViewClient() {
                        override fun shouldOverrideUrlLoading(view: WebView?, url: String?): Boolean {
                            return false // Allow WebView to load the URL
                        }
                    }
                    tag = videoId
                    // Using youtube.com as base URL bypasses domain embedding restrictions (Error 150/153)
                    loadDataWithBaseURL("https://www.youtube.com", htmlData, "text/html", "utf-8", null)
                }
            },
            update = { webView ->
                if (webView.tag != videoId) {
                    webView.tag = videoId
                    webView.loadDataWithBaseURL("https://www.youtube.com", htmlData, "text/html", "utf-8", null)
                }
            }
        )
    }
}
"""

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(new_code)

