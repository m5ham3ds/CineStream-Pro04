with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "r") as f:
    original = f.read()

import_part = original.split("@Composable")[0]

new_composable = """@Composable
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
    var loadedVideoId by remember { mutableStateOf<String?>(null) }

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

                    post { initialize(listener, options) }
                }
            },
            update = { _ ->
                val player = youtubePlayer
                if (player != null && loadedVideoId != videoId) {
                    player.loadVideo(videoId, 0f)
                    loadedVideoId = videoId
                }
            },
            onRelease = { it.release() }
        )
    }
}
"""

with open("app/src/main/java/com/example/ui/components/YouTubePlayer.kt", "w") as f:
    f.write(import_part + new_composable)
