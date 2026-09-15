import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "r") as f:
    content = f.read()

old_logic = """        if (!directUrl.isNullOrEmpty() && (directUrl.contains(".mp4") || directUrl.contains(".m3u8") || directUrl.startsWith("local_offline_file"))) {
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = directUrl, 
                isLoading = false
            )
        } else if (!directUrl.isNullOrEmpty()) {"""

new_logic = """        if (!directUrl.isNullOrEmpty() && (directUrl.contains(".mp4") || directUrl.contains(".m3u8") || directUrl.startsWith("local_offline_file"))) {
            var finalDirectUrl = directUrl
            if (directUrl.startsWith("local_offline_file://")) {
                val fileId = directUrl.removePrefix("local_offline_file://")
                val file = java.io.File(android.os.Environment.getExternalStoragePublicDirectory(android.os.Environment.DIRECTORY_MOVIES), "CineStream/${fileId}.mp4")
                finalDirectUrl = android.net.Uri.fromFile(file).toString()
            }
            _uiState.value = _uiState.value.copy(
                currentVideoUrl = finalDirectUrl, 
                isLoading = false
            )
        } else if (!directUrl.isNullOrEmpty()) {"""

content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/player/PlayerViewModel.kt", "w") as f:
    f.write(content)
