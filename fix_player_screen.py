import re
with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "r") as f:
    content = f.read()

old_logic = """            val videoUrl = uiState.currentVideoUrl!!
            val isDirectVideo = videoUrl.contains(".mp4") || videoUrl.contains(".m3u8") || videoUrl.contains(".mkv")
            
            if (isDirectVideo && uiState.currentVideoUrl?.contains("embed") != true && uiState.currentVideoUrl?.contains("iframe") != true) {"""
new_logic = """            val videoUrl = uiState.currentVideoUrl!!
            val isDirectVideo = videoUrl.contains(".mp4") || videoUrl.contains(".m3u8") || videoUrl.contains(".mkv") || videoUrl.startsWith("local_offline_file")
            
            if (isDirectVideo && uiState.currentVideoUrl?.contains("embed") != true && uiState.currentVideoUrl?.contains("iframe") != true) {"""
content = content.replace(old_logic, new_logic)

with open("app/src/main/java/com/example/ui/screens/player/PlayerScreen.kt", "w") as f:
    f.write(content)
