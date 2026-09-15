import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_android_view = """                AndroidView(
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                mediaPlaybackRequiresUserGesture = false
                                useWideViewPort = true
                                loadWithOverviewMode = true
                                setSupportZoom(true)
                                builtInZoomControls = true
                                displayZoomControls = false
                                val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)
                                userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")
                            }
                            val cookieManager = CookieManager.getInstance()
                            cookieManager.setAcceptCookie(true)
                            cookieManager.setAcceptThirdPartyCookies(this, true)
                            webViewClient = WebViewClient()
                            loadUrl(videoUrl)
                        }
                    },
                    modifier = Modifier.fillMaxSize()
                )"""

new_android_view = """                AndroidView(
                    factory = { ctx ->
                        WebView(ctx).apply {
                            settings.apply {
                                javaScriptEnabled = true
                                domStorageEnabled = true
                                mediaPlaybackRequiresUserGesture = false
                                useWideViewPort = true
                                loadWithOverviewMode = true
                                setSupportZoom(true)
                                builtInZoomControls = true
                                displayZoomControls = false
                                val originalUserAgent = WebSettings.getDefaultUserAgent(ctx)
                                userAgentString = originalUserAgent.replace("; wv", "").replace("Version/4.0 ", "")
                            }
                            val cookieManager = CookieManager.getInstance()
                            cookieManager.setAcceptCookie(true)
                            cookieManager.setAcceptThirdPartyCookies(this, true)
                            webViewClient = WebViewClient()
                            loadUrl(videoUrl)
                        }
                    },
                    update = { webView ->
                        val lastUrl = webView.getTag(com.example.R.id.tag_url) as? String
                        if (lastUrl != videoUrl) {
                            webView.setTag(com.example.R.id.tag_url, videoUrl)
                            webView.loadUrl(videoUrl)
                        }
                    },
                    onRelease = { webView ->
                        webView.destroy()
                    },
                    modifier = Modifier.fillMaxSize()
                )"""

if old_android_view in content:
    content = content.replace(old_android_view, new_android_view)
    with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
        f.write(content)
    print("Replaced successfully!")
else:
    print("Could not find the block to replace!")
