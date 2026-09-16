import re

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    c = f.read()

target1 = """        val cookie = android.webkit.CookieManager.getInstance().getCookie(uiState.currentVideoUrl ?: "") ?: ""
        val dataSourceFactory = DefaultHttpDataSource.Factory()
            .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
        if (cookie.isNotEmpty()) {
            dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
        }
        val mediaSourceFactory = DefaultMediaSourceFactory(dataSourceFactory)"""
        
replace1 = """        val cookie = android.webkit.CookieManager.getInstance().getCookie(uiState.currentVideoUrl ?: "") ?: ""
        val httpDataSourceFactory = DefaultHttpDataSource.Factory()
            .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
        if (cookie.isNotEmpty()) {
            httpDataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
        }
        val dataSourceFactory = androidx.media3.datasource.DefaultDataSource.Factory(context, httpDataSourceFactory)
        val mediaSourceFactory = DefaultMediaSourceFactory(dataSourceFactory)"""

c = c.replace(target1, replace1)

target2 = """            val cookie = android.webkit.CookieManager.getInstance().getCookie(url) ?: ""
            val dataSourceFactory = DefaultHttpDataSource.Factory()
                .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
            if (cookie.isNotEmpty()) {
                dataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
            }
            val mediaSource = DefaultMediaSourceFactory(dataSourceFactory).createMediaSource(MediaItem.fromUri(url))"""

replace2 = """            val cookie = android.webkit.CookieManager.getInstance().getCookie(url) ?: ""
            val httpDataSourceFactory = DefaultHttpDataSource.Factory()
                .setUserAgent("Mozilla/5.0 (Linux; Android 13; SM-S918B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Mobile Safari/537.36")
            if (cookie.isNotEmpty()) {
                httpDataSourceFactory.setDefaultRequestProperties(mapOf("Cookie" to cookie))
            }
            val dataSourceFactory = androidx.media3.datasource.DefaultDataSource.Factory(context, httpDataSourceFactory)
            val mediaSource = DefaultMediaSourceFactory(dataSourceFactory).createMediaSource(MediaItem.fromUri(url))"""

c = c.replace(target2, replace2)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(c)
