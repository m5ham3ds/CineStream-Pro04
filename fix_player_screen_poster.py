import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_fun = """fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {"""
new_fun = """fun PlayerScreen(mediaId: String, isMovie: Boolean, title: String, posterUrl: String = "", url: String? = null, targetServer: String? = null, website: String? = null, onBack: () -> Unit, viewModel: PlayerViewModel = viewModel()) {"""
content = content.replace(old_fun, new_fun)

old_dl = """                            com.example.data.model.DownloadItem(
                                id = fileId,
                                mediaId = uiState.mediaId,
                                title = uiState.title,
                                posterUrl = "",
                                isMovie = uiState.isMovie,"""
new_dl = """                            com.example.data.model.DownloadItem(
                                id = fileId,
                                mediaId = uiState.mediaId,
                                title = uiState.title,
                                posterUrl = posterUrl,
                                isMovie = uiState.isMovie,"""
content = content.replace(old_dl, new_dl)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
