import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

# 1. Add isBuffering state
if "var isBuffering by remember" not in content:
    content = re.sub(
        r'var isPlaying by remember { mutableStateOf\(true\) }',
        r'var isPlaying by remember { mutableStateOf(true) }\n    var isBuffering by remember { mutableStateOf(true) }',
        content
    )

# 2. Add isBuffering logic to the listener
content = content.replace(
"""                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                    }
                }""",
"""                override fun onPlaybackStateChanged(state: Int) {
                    if (state == Player.STATE_READY) {
                        totalDuration = duration.coerceAtLeast(0L)
                        isBuffering = false
                    } else if (state == Player.STATE_BUFFERING) {
                        isBuffering = true
                    } else {
                        isBuffering = false
                    }
                }""")

# 3. Change Play/Pause icon logic
play_pause_code = """                                Icon(
                                    if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                    contentDescription = "Play/Pause",
                                    tint = MaterialTheme.colorScheme.onBackground,
                                    modifier = Modifier.size(36.dp)
                                )"""
new_play_pause_code = """                                if (isBuffering) {
                                    CircularProgressIndicator(color = MaterialTheme.colorScheme.primary, modifier = Modifier.size(36.dp))
                                } else {
                                    Icon(
                                        if (isPlaying) Icons.Default.Pause else Icons.Default.PlayArrow,
                                        contentDescription = "Play/Pause",
                                        tint = MaterialTheme.colorScheme.onBackground,
                                        modifier = Modifier.size(36.dp)
                                    )
                                }"""
content = content.replace(play_pause_code, new_play_pause_code)

# 4. Fix seeking logic
content = content.replace('exoPlayer.seekTo((exoPlayer.currentPosition - 10000).coerceAtLeast(0))', 'exoPlayer.seekTo(exoPlayer.currentPosition - 10000)')
content = content.replace('exoPlayer.seekTo((exoPlayer.currentPosition + 10000).coerceAtMost(exoPlayer.duration))', 'exoPlayer.seekTo(exoPlayer.currentPosition + 10000)')

# 5. Fix duplicate Loading text in showControls block
duplicate_loading = """                    if (uiState.currentVideoUrl == null) {
                        Column(
                            modifier = Modifier.align(Alignment.Center),
                            horizontalAlignment = Alignment.CenterHorizontally
                        ) {
                            CircularProgressIndicator(color = MaterialTheme.colorScheme.primary)
                            Spacer(modifier = Modifier.height(16.dp))
                            val serverText = if (uiState.currentServer.isNotEmpty()) " / ${uiState.currentServer}" else ""
                            Text(stringResource(R.string.loading_site, "${uiState.currentWebsite}$serverText"), color = MaterialTheme.colorScheme.onBackground, fontWeight = FontWeight.Bold)
                        }
                    } else {"""
# We just replace the text with nothing, or we can just remove the Text completely, since the main isLoading block shows the full text. Wait, if I just remove this Text, the spinner will still be there. But there's already a spinner in the main isLoading block! Let's just remove this entire if/else and ONLY show the controls if `uiState.currentVideoUrl != null`. Wait, no, we can keep the `else` contents.
content = content.replace(duplicate_loading, "                    if (uiState.currentVideoUrl != null) {")


with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
